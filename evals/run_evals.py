#!/usr/bin/env python3
"""Trigger evals for the plugin's skills.

For each evals/<skill>/evals.json, runs `claude -p` headless with this repo
as --plugin-dir and checks whether the skill fires (a Skill tool_use in the
stream-json output). A query is correct when the observed trigger matches its
should_trigger flag. Near-miss queries (should_trigger: false) catch
descriptions that fire too eagerly.

Each query is a real model call, so this is local-only and deliberately not
wired into CI.

    python3 evals/run_evals.py                     # all skills, 1 run/query
    python3 evals/run_evals.py review-docs         # one skill
    python3 evals/run_evals.py --runs 3            # repeat for flake checking
    python3 evals/run_evals.py --max-queries 2     # smoke test the harness

A skill passes a query when the majority of its runs agree with
should_trigger (the anthropics/skills convention: 0.5 trigger-rate
threshold).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
EVALS_DIR = pathlib.Path(__file__).resolve().parent
TIMEOUT_S = 240


def run_query(prompt: str, model: str | None) -> tuple[set[str], str]:
    """Run one headless query; return (skills that fired, raw note on failure)."""
    cmd = [
        "claude",
        "-p",
        prompt,
        "--plugin-dir",
        str(ROOT),
        "--max-turns",
        "3",
        "--output-format",
        "stream-json",
        "--verbose",
    ]
    if model:
        cmd += ["--model", model]

    # Fresh empty cwd so the model neither reads nor mutates this repo while
    # deciding whether a skill applies.
    with tempfile.TemporaryDirectory() as scratch:
        try:
            proc = subprocess.run(
                cmd,
                cwd=scratch,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_S,
            )
        except subprocess.TimeoutExpired:
            return set(), "timeout"

    fired: set[str] = set()
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = event.get("message") or {}
        for block in message.get("content") or []:
            if block.get("type") == "tool_use" and block.get("name") == "Skill":
                fired.add(json.dumps(block.get("input", {})))
    # Nonzero exit is routine when --max-turns truncates a session, so only
    # surface it when the skill never fired (e.g. exit 127, CLI missing).
    note = ""
    if proc.returncode != 0 and not fired:
        note = f"claude exited {proc.returncode}"
    return fired, note


def skill_fired(fired_inputs: set[str], skill: str) -> bool:
    return any(skill in raw for raw in fired_inputs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", help="skill names; default all")
    parser.add_argument("--runs", type=int, default=1, help="runs per query")
    parser.add_argument("--max-queries", type=int, help="cap queries per skill")
    parser.add_argument("--model", help="model override passed to claude")
    args = parser.parse_args()

    eval_files = sorted(EVALS_DIR.glob("*/evals.json"))
    if args.skills:
        eval_files = [f for f in eval_files if f.parent.name in args.skills]
    if not eval_files:
        print("no evals.json found for the requested skills", file=sys.stderr)
        return 2

    total_correct = total_queries = 0
    for eval_file in eval_files:
        skill = eval_file.parent.name
        queries = json.loads(eval_file.read_text())["queries"]
        if args.max_queries:
            queries = queries[: args.max_queries]
        print(f"\n{skill} ({len(queries)} queries, {args.runs} run(s) each)")

        correct = 0
        for query in queries:
            prompt, expected = query["prompt"], query["should_trigger"]
            hits = 0
            notes = []
            for _ in range(args.runs):
                fired, note = run_query(prompt, args.model)
                hits += skill_fired(fired, skill)
                if note:
                    notes.append(note)
            triggered = hits / args.runs >= 0.5
            ok = triggered == expected
            correct += ok
            marker = "pass" if ok else "FAIL"
            detail = f" [{'; '.join(notes)}]" if notes else ""
            print(
                f"  {marker}  expected={'fire' if expected else 'skip'} "
                f"got {hits}/{args.runs}  {prompt[:70]}{detail}"
            )
        total_correct += correct
        total_queries += len(queries)
        print(f"  {skill}: {correct}/{len(queries)} correct")

    print(f"\noverall: {total_correct}/{total_queries} correct")
    return 0 if total_correct == total_queries else 1


if __name__ == "__main__":
    sys.exit(main())
