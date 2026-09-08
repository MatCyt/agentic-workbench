---
name: mc-to-spec-guided
description: >-
  Convert the current planning conversation into a guided-development spec plus individual
  issue files under .scratch/specs/<feature>/, optimized for human-controlled sequencing,
  parallel execution where useful, and human diff review. Extract every decision from the
  conversation, verify references against the repository, resolve open decisions with the
  user BEFORE writing. A fresh session with zero conversation memory must be able to execute
  any ready issue from the spec + issue file alone.
disable-model-invocation: true
user-invocable: true
argument-hint: "[optional: feature slug; default: derived from the conversation]"
---

# mc-to-guided-spec — conversation → guided spec + issues

Create a plan for guided development: the human controls sequencing, review,
commits, and final integration. Ready independent issues may run concurrently in
separate worktrees.

This skill produces the plan only — do not implement anything.

## Process

### 1. Harvest the conversation

Extract:

- locked decisions and their rationale;
- non-obvious rejected alternatives;
- constraints and invariants;
- referenced files, patterns, and docs;
- unresolved decisions.

### 2. Verify against the repository

Verify referenced paths and symbols and correct stale references.

Read repository conventions such as `AGENTS.md` and `ARCHITECTURE.md`.

Use `make verify` when available; otherwise use the repository's normal lint,
test, type-check, and dependency checks.

Determine real dependencies between planned issues.

### 3. Close gaps

Ask the user to resolve unresolved decisions before writing.

If something is deliberately deferred, record it under **Open questions** and
name the issues it blocks.

### 4. Write artifacts

Write:

```text
.scratch/specs/<feature-slug>/
  spec.md
  issues/
    01-<slug>.md
    02-<slug>.md
```

### `spec.md`

```markdown
# <Feature> — spec

<What is being built, where, and why.>

## Decisions
<Locked decisions and relevant rejected alternatives.>

## Invariants
<Rules that bind all issues.>

## Reference map
<Verified pointers to relevant code and patterns.>

## Out of scope
<Feature-level exclusions.>

## Issues
<Number, title, blocked-by.>

## Open questions
<Only deferred decisions, with affected issues.>
```

### `issues/NN-slug.md`

```markdown
# NN — <title>

Read `../spec.md` first. It binds this issue.

**Blocked by:** <numbers or "none — ready">
**Status:** ready

## What to build
<One coherent behavior, end to end.>

## Files
<Expected created/modified files or verified patterns.>

## Out of scope
<Tempting adjacent work that must not be included.>

## Definition of Done
<Objectively checkable outcomes, including verification.>

## Review focus [mechanical|new-logic]
<What deserves human scrutiny or what evidence makes skimming safe.>
```

## Issue design rules

- Use **vertical slices**: implementation and tests together; leave the repo green.
- Size issues for **human review**, roughly a 10–15 minute diff review.
- Do not split work merely to make implementation easier for an agent.
- Split when there is a meaningful **review, dependency, risk, parallelism, or
  rollback boundary**.
- Batch repetitive mechanical changes when they follow one established pattern.
- Isolate substantial new logic when that materially improves review.
- Add `Blocked by` edges only for real dependencies. Sequential numbering does
  not imply sequential execution.
- Every ready issue must be executable by a fresh agent with only the spec,
  issue, repository docs, and codebase.

## Writing rules
- Never rely on the original conversation.
- Never copy secrets.
- Put shared knowledge in `spec.md`; do not repeat it across issues.
- Keep every sentence useful: decision, invariant, reference, dependency, scope,
  work, or completion criterion.


# 5. Self-check, then hand off
## Self-check

Before finishing, verify for every issue:

- it can be implemented without guessing;
- completion is objectively testable;
- dependencies are necessary;
- it is not artificially small;
- independent work is not unnecessarily serialized.

Then report the artifact path, issue list with dependencies, open questions, and
which issues are initially ready.