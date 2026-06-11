# Skill evals

Two layers, both local-only (every run spawns real headless Claude Code
sessions, so they cost tokens and are deliberately not part of CI):

- **Trigger evals** (`run_evals.py`): does each skill's `description` fire
  for the prompts it should, and stay quiet for the near-misses?
- **Quality evals** (`run_quality.py`): given a fixture docs tree with
  planted violations, does the skill actually produce conforming output?

## Trigger evals

## Run

```bash
python3 evals/run_evals.py                  # everything
python3 evals/run_evals.py review-docs      # one skill
python3 evals/run_evals.py --runs 3         # 3 runs per query (flake check)
python3 evals/run_evals.py --max-queries 2  # quick harness smoke test
```

Requirements: the Claude Code CLI on PATH and an authenticated session.
Python is stdlib-only.

## How it works

For each `evals/<skill>/evals.json`, every query runs as
`claude -p <prompt> --plugin-dir <repo> --max-turns 3` in an empty scratch
directory, and the stream-json output is scanned for a `Skill` tool_use
naming that skill. With `--runs N`, a query counts as triggered when at
least half its runs fire (the anthropics/skills convention).

## Eval set format

```json
{
  "queries": [
    { "prompt": "Review the docs site before we launch", "should_trigger": true },
    { "prompt": "Review this pull request", "should_trigger": false }
  ]
}
```

Guidelines for new queries, from the skill-creator methodology:

- Make prompts substantive. Claude only consults skills for tasks it cannot
  trivially answer, so one-liners that need no tools tend to under-trigger.
- Near-misses should be genuinely near: same verbs, different scope. The
  cross-skill ones ("review the changelog" against `review-docs`) are the
  most valuable, since they catch descriptions stealing each other's work.
- When a skill under- or over-triggers, fix the `description` in its
  SKILL.md, not the eval.

## Quality evals

```bash
python3 evals/run_quality.py                  # all quality evals
python3 evals/run_quality.py changelog-writer # one skill
python3 evals/run_quality.py --baseline       # compare against no-plugin runs
```

Each `quality/<skill>/` holds:

- `fixture/` — a small docs tree with planted violations. Fixtures
  intentionally break house style (em dashes, `<Tip>` callouts, vanity
  metrics); that is the test data, do not "fix" them.
- `prompt.txt` — the task given to the headless session.
- `checks.json` — assertions, one per planted violation:
  - `file_must_match` / `file_must_not_match`: regex over a fixture file
    after the session. Fix-grading, for skills that apply edits
    (changelog-writer audits apply in one pass).
  - `output_mentions_any`: case-insensitive substring over everything the
    model said. Detection-grading, for skills that report options-first and
    must not edit (review-docs).

`--baseline` reruns each eval without `--plugin-dir` and prints both scores;
the gap is the measured value of the skill. A failing check means the skill
content needs work (or the planted violation is genuinely ambiguous); as with
trigger evals, fix the skill, not the assertion.
