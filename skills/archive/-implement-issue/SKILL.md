---
name: -implement-issue
description: >-
  Implement exactly one issue, then stop at the review gate without committing. 
disable-model-invocation: true
user-invocable: true
argument-hint: "[mandatory: path to the issue file]"
---

This skill's job is to be a disciplined executor: exactly one
increment, exactly its scope, then hand control back for a 
manual review of a small diff.

## Process

### 1. Read

- No issue path given → ask; don't guess.
- Read `spec.md` in the issue's feature directory **and** the issue file, fully. The
  spec's Decisions, Invariants, and Reference map bind this issue; you have no other
  context.
- Issue status `done` → say so and stop. Blockers not all `done` → say so and stop.

### 2. Pre-flight

- Uncommitted changes touching plan-related files → stop and ask: the previous gate
  probably wasn't closed. Unrelated dirt is fine; mention it.
- Open questions in the spec blocking this issue → ask the user now; never implement
  on a guess.

### 3. Execute

- Touch only the issue's listed files, plus mechanical side effects a change forces
  (lock file) — flag those in the summary.
- Out of scope means out of scope, even for obvious cheap improvements — note those in
  the summary instead.
- If the plan is wrong or infeasible as written (missing file, a locked decision can't
  work, definition of done unreachable in scope): **stop and surface it** with a proposed amendment.
  Never silently adapt — unrecorded deviations make every later issue unsafe.

### 4. Verify

`make verify` if the Makefile defines it, else:
`uv run ruff check && uv run pytest && uv run mypy && uv run deptry`

### 5. Close the gate

- Set the issue's `Status:` to `done` — the only plan edit you may make.
- Do **not** commit, do **not** start the next issue or pre-implement parts of it.

## Summary — the review handoff

- **Changed**: each file, one line.
- **Verification**: commands run, result, stated plainly.
- **Deviations**: anything not exactly as written, incl. forced extra files — or "none".
- **Review focus**: echo the issue's review-focus line.