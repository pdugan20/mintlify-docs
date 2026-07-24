#!/usr/bin/env python3
"""Quality evals: does a skill actually produce conforming output?

Each evals/quality/<skill>/ has a fixture docs tree with planted violations,
a prompt, and machine-checkable assertions in checks.json. The runner copies
the fixture to a scratch dir, runs a real headless session against it with
this repo as --plugin-dir, then grades:

- file_must_match / file_must_not_match: regex over a fixture file after the
  session (fix-grading; used where the skill applies edits).
- output_mentions_any: case-insensitive substring over everything the model
  said (detection-grading; used where the skill reports options-first and
  must not edit).

Local-only, like the trigger evals: each eval is a full agentic session.

    python3 evals/run_quality.py                  # all quality evals
    python3 evals/run_quality.py changelog-writer # one skill
    python3 evals/run_quality.py --baseline       # also run without the
                                                  # plugin and compare
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUALITY_DIR = pathlib.Path(__file__).resolve().parent / "quality"
TIMEOUT_S = 900


def run_session(
    prompt: str, cwd: pathlib.Path, max_turns: int, with_plugin: bool
) -> str:
    """Run one headless session; return everything the model said."""
    cmd = ["claude", "-p", prompt]
    if with_plugin:
        cmd += ["--plugin-dir", str(ROOT)]
    cmd += [
        "--permission-mode",
        "acceptEdits",
        "--max-turns",
        str(max_turns),
        "--output-format",
        "stream-json",
        "--verbose",
    ]
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_S,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return ""

    said = []
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result" and event.get("result"):
            said.append(event["result"])
        for block in (event.get("message") or {}).get("content") or []:
            if block.get("type") == "text":
                said.append(block.get("text", ""))
    return "\n".join(said)


def grade(check: dict, scratch: pathlib.Path, output: str) -> bool:
    kind = check["type"]
    if kind in ("file_must_match", "file_must_not_match"):
        target = scratch / check["path"]
        text = target.read_text() if target.exists() else ""
        found = re.search(check["pattern"], text) is not None
        return found if kind == "file_must_match" else not found
    if kind == "output_mentions_any":
        low = output.lower()
        return any(term.lower() in low for term in check["terms"])
    raise ValueError(f"unknown check type: {kind}")


def run_eval(eval_dir: pathlib.Path, with_plugin: bool) -> tuple[int, int, list]:
    config = json.loads((eval_dir / "checks.json").read_text())
    prompt = (eval_dir / "prompt.txt").read_text().strip()
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        scratch = pathlib.Path(tmp)
        shutil.copytree(eval_dir / "fixture", scratch, dirs_exist_ok=True)
        output = run_session(
            prompt, scratch, config.get("max_turns", 30), with_plugin
        )
        passed = 0
        for check in config["checks"]:
            if grade(check, scratch, output):
                passed += 1
            else:
                failures.append(check["name"])
    return passed, len(config["checks"]), failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", help="skill names; default all")
    parser.add_argument(
        "--baseline",
        action="store_true",
        help="also run each eval without the plugin and compare",
    )
    args = parser.parse_args()

    eval_dirs = sorted(d for d in QUALITY_DIR.iterdir() if d.is_dir())
    if args.skills:
        eval_dirs = [d for d in eval_dirs if d.name in args.skills]
    if not eval_dirs:
        print("no quality evals found for the requested skills", file=sys.stderr)
        return 2

    all_pass = True
    for eval_dir in eval_dirs:
        skill = eval_dir.name
        passed, total, failures = run_eval(eval_dir, with_plugin=True)
        all_pass &= passed == total
        line = f"{skill}: {passed}/{total} checks with skill"
        if args.baseline:
            base_passed, _, _ = run_eval(eval_dir, with_plugin=False)
            line += f" (baseline without plugin: {base_passed}/{total})"
        print(line)
        for name in failures:
            print(f"  FAIL  {name}")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
