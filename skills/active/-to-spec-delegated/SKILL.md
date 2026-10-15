---
name: -to-spec-delegated
description: >-
  Convert the current planning conversation into a spec plus issue files under
  .scratch/specs/<feature>/. The spec is the intent record: what is built and
  why, decisions, invariants, scope. Issues are execution units sized to fit one
  context window, with explicit dependencies so independent ones can run in
  parallel. A fresh agent
  with no conversation memory must be able to implement any issue from the spec,
  the issue file, and repository docs alone. The spec is later used for code
  review and for building the PR description once all issues are implemented.

disable-model-invocation: true
user-invocable: true
argument-hint: "[optional: feature slug; default: derived from the conversation]"
---

# -to-spec-delegated — conversation → spec + issues

Produce the plan only. Do not implement anything.

## Process

### 1. Harvest the conversation

Extract: what is being built, where, and why; locked decisions and their rationale, rejected alternatives worth recording,
constraints and invariants, referenced files and patterns. Unresolved decisions are cut to
**Out of scope**; executors state assumptions, never ask.

### 2. Verify against the repository

Read `AGENTS.md` and `ARCHITECTURE.md` if present. Verification commands come
from there; do not restate them.

Every file path written into the spec or an issue must have been opened during
this planning session. Never infer a path from naming. Correct stale references.

### 3. Write artifacts

```text
.scratch/specs/<feature-slug>/
  spec.md
  issues/
    01-<slug>.md
    02-<slug>.md
```

### 4. Self-check

For every issue confirm: it can be implemented without guessing; ; it assumes nothing beyond the spec, its dependencies, repository docs, and the codebase.

Report the artifact path, the issue list with dependencies, and anything cut
because it was unresolved.

## `spec.md`

```markdown
# <Feature> — spec

<What is being built, where, and why.>

## Decisions
<One line per decision, stated in architectural terms so it still holds if
files move. Rationale only when non-obvious. Rejected alternatives only when
an implementer might plausibly pick them. Each decision may carry a verified
pointer to current code:>

- <Decision.>
  Now: `<path>`, pattern in `<path>`

## Invariants
<Rules that must stay true across all issues: what must not break, what must
not be introduced, which boundaries must be respected.>

## Out of scope
<Feature-level exclusions, including decisions cut because unresolved.>

## Issues
<Number, title, depends on. Issues with no dependency between them may run
in parallel.>

## Open questions
<Only items affecting work beyond this spec. Never anything an executor needs.>
```

## `issues/NN-slug.md`

```markdown
# NN — <title>

Read `../spec.md` first. It binds this issue.

**Status:** ready
**Depends on:** <none | NN, NN>

## What to build
<One coherent unit of work, end to end, including tests. Assumes its
dependencies are committed and green.>

## Files
<Files expected to be created or modified. Everything else is out of bounds.
Must not overlap with any issue this one does not depend on.>

## Out of scope
<Tempting adjacent work that must not be included.>

## Definition of Done
<Criteria a verifier can check. Prefer commands with expected output; a
precise observable statement is acceptable when no command fits.>

## Deviations
<Empty at planning time. The implementer appends every divergence from the
spec or this issue, with the reason. Read when building the PR.>
```

## Issue design rules

- **Vertical slices**: implementation and tests together; the repo stays green.
- **Sizing**: an issue must fit comfortably in one context window of a
  mid-tier model, including reading the spec and the relevant code. Larger
  than a task, smaller than the feature. A failed attempt should be cheap to
  discard and retry.
- **Parallelism is preferred, not required.** Split along disjoint file sets
  where it falls out naturally. Do not contort the work to force independence;
  a dependency is better than an artificial boundary.
- **Files are the contract.** Two issues without a dependency between them
  must not list the same file. If they must, merge them or add a dependency.
- **Explicit over clever.** Every issue is written for a fresh agent with only
  the spec, the issue, repository docs, and the codebase.

## Writing rules

- Never copy secrets.
- Shared knowledge lives in `spec.md`; issues do not repeat it.
- Every sentence is a decision, invariant, reference, scope, work item, or
  completion criterion.
