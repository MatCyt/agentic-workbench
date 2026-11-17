---
name: -to-issues-agentic
description: >-
  Cut a spec written by /-to-spec into issue files under
  .scratch/specs/<feature>/issues-agentic/, for implementation by agents. Issues are execution
  units sized to fit one context window, with explicit dependencies so independent ones can
  run in parallel. A fresh agent with no conversation memory must be able to implement any
  issue from the spec, the issue file, and repository docs alone. Use when the goal is fast
  delegation. /-implement-spec runs the result.
disable-model-invocation: true
user-invocable: true
argument-hint: "[spec dir: .scratch/specs/<feature>/ — default: the only or newest one]"
---

# -to-issues-agentic — spec → issues for agents

Input: a spec directory `.scratch/specs/<feature>/` containing `spec.md`. If none is given, use
the only spec dir; if several exist, use the newest and say so. If there is no `spec.md`, stop
and tell the user to run `/-to-spec` first.

The spec is the intent record and the single source. This skill decides only how the work is
cut: which pieces, which dependencies, what can run in parallel. It adds no decision of its
own.

Success test: **a fresh agent with only `spec.md`, one issue file, repository docs, and the
codebase can implement that issue without guessing or asking. When every issue is done, the
repository is at the spec's Target end state.**

Produce the issues only. Do not implement anything.

## Process

### 1. Read the spec

Read `spec.md` in full. Read `AGENTS.md` and `ARCHITECTURE.md` if present. Verification
commands come from there; do not restate them.

The spec is the only source of intent. When the conversation holds something that the spec
does not, the spec has a gap: handle it in step 3.

### 2. Verify against the repository

Every existing file path written into an issue must have been opened during this session.
Never infer an existing path from naming.

### 3. Correct the spec first

When reading or verification shows that the spec is wrong or incomplete:

- Stale path or reference: correct it in `spec.md`.
- Anything that changes a decision, an invariant, or **Target end state**: ask the user. One
  round, all questions together. Then correct `spec.md`.

An issue never holds a correction that the spec does not hold.

A part of **Target end state** that an open question blocks is not cut. Executors state
assumptions, never ask, so a blocked part cannot be delegated.

### 4. Write `.scratch/specs/<feature-slug>/issues-agentic/NN-<slug>.md`

```text
.scratch/specs/<feature-slug>/
  spec.md
  issues-agentic/
    01-<slug>.md
    02-<slug>.md
```

```markdown
# NN — <title>

Read `../spec.md` first. It binds this issue.

**Status:** ready
**Depends on:** <none | NN, NN>

## What to build
<One coherent unit of work, end to end, including tests. Assumes its dependencies are
committed and green.>

## Files
<Files expected to be created or modified. Everything else is out of bounds. Must not overlap
with any issue this one does not depend on.>

## Assumptions
<Unchecked assumptions from the spec's **External systems** that this issue relies on. Omit
the section when there is none. An implementer who finds one false stops and reports; it does
not build around it.>

## Out of scope
<Tempting adjacent work that must not be included.>

## Definition of Done
<Criteria a verifier can check. Prefer commands with expected output; a precise observable
statement is acceptable when no command fits.>

## Deviations
<Empty at planning time. The implementer appends every divergence from the spec or this
issue, with the reason. Read when building the PR.>
```

### 5. Self-check, then report

- Can every issue be implemented without guessing, from the spec, its dependencies, repository
  docs, and the codebase alone?
- Is every module, interface, test, and document in **Target end state** owned by an issue,
  except the parts that an open question blocks?
- Is every **Done when** check in the spec covered by the Definition of Done of an issue?
- Do two issues with no dependency between them list the same file? Merge them or add a
  dependency.
- Does any issue hold a decision that the spec does not hold? Move it to the spec.

Fix the issues until every answer is right.

Then report: the issues directory path, the issue list with dependencies, corrections made to
`spec.md`, parts not cut because an open question blocks them, unchecked assumptions with the
issue that relies on each, and how to start: `/-implement-spec <spec dir>`.

## Issue design rules

- **Vertical slices**: implementation and tests together; the repo stays green.
- **Sizing**: an issue must fit comfortably in one context window of a mid-tier model,
  including reading the spec and the relevant code. Larger than a task, smaller than the
  feature. A failed attempt should be cheap to discard and retry.
- **Parallelism is preferred, not required.** Split along disjoint file sets where it falls
  out naturally. Do not contort the work to force independence; a dependency is better than
  an artificial boundary.
- **Files are the contract.** Two issues without a dependency between them must not list the
  same file. If they must, merge them or add a dependency.
- **Explicit over clever.** Every issue is written for a fresh agent with only the spec, the
  issue, repository docs, and the codebase.

## Writing rules

- Never copy secrets.
- Shared knowledge lives in `spec.md`; issues do not repeat it.
- Every sentence is a reference, scope, work item, or completion criterion.
