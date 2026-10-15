---
name: -to-task
description: Capture a current conversation into a task for another agent to pick up.
disable-model-invocation: true
user-invocable: true
---

# To Task
Distill this conversation into a handoff file a fresh agent session can execute.
The reader has full repo access but zero conversation context — capture only what
it cannot rediscover: decisions made, reasons behind them, dead ends explored.

## Output
Write to `.scratch/to-task/<task-slug>.md` at the repo root. **Task** and
**Approach** are mandatory; every other section is optional, omit it if empty. 

```markdown
# Handoff: <short task title>

## Task
1–4 sentences, phrased as an instruction: what to change, what outcome it produces.

## Relevant files
- `path/to/file.py:42` — one clause on why it matters. Pointers only, no code.

## Approach
The agreed solution as numbered, imperative steps. Settled decisions —
"Use X", not "we discussed maybe using X".

## Rejected alternatives
- <alternative> — rejected because <one line>. Only ones genuinely considered,
so the fresh agent doesn't re-propose them.

## Constraints & gotchas
Non-obvious facts: edge cases, "don't touch X", environment quirks, conventions.

## Out of scope
What NOT to do. Fresh agents expand small tasks; an explicit fence beats a
longer description.

## Verification
Command to run, behavior to observe.

## Open questions
Anything unresolved — and whether the implementer should decide or ask the user.
```

Rules:
- **Resolve every reference.** "The function we looked at" → `parse_entries() in scraper.py:88`. Any dangling "it/that" is a broken link.
- **Keep it short.** ~30–60 lines for a small change. Longer means it's smuggling transcript, not context.

Afterwards, report the file path and give a ready-to-paste kickoff prompt:

> Read .scratch/to-task/<task-slug>.md and implement it.

<instructions>$ARGUMENTS</instructions>