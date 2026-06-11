# Skill trigger evals

Checks that each skill's `description` fires for the prompts it should and
stays quiet for the near-misses it should not. The runner spawns real
headless Claude Code sessions, so it costs tokens and runs locally only; it
is deliberately not part of CI.

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
