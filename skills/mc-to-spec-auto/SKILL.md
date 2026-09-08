---
name: mc-to-spec-auto
description: >-
  Convert the current planning conversation into an autonomous-execution spec plus
  individual issue files under .scratch/specs/<feature>/, optimized for an orchestrated,
  strictly sequential run where an agent implements and a verifier checks — no human in
  the loop mid-run. Issues are large, milestone-sized vertical slices with fully
  machine-checkable Definitions of Done. Extract every decision from the conversation,
  verify references against the repository, resolve open decisions with the user BEFORE
  writing. A fresh session with zero conversation memory must be able to execute any
  issue from the spec + issue file alone.

disable-model-invocation: true
user-invocable: true
argument-hint: "[optional: feature slug; default: derived from the conversation]"
---

# mc-to-spec-autonomous — conversation → autonomous spec + issues
 
Create a plan for autonomous execution: an orchestrator runs issues strictly in
order, executors implement, verification is done by machine-checkable commands,
and the human only reviews the final result. No human sequencing, no mid-run
review, no parallelism.
 
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
test, type-check, and dependency checks. Record the exact verification command
in the spec — the run depends on it.
 
Determine the natural sequential milestones of the work.
 
### 3. Close gaps
 
Ask the user to resolve unresolved decisions before writing.
 
Autonomous runs cannot tolerate deferred decisions inside the planned issues:
anything unresolved must either be resolved now or cut from scope and recorded
under **Out of scope**. **Open questions** may only contain items that affect
work *after* this spec's issues.
 
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
 
## Verification
<The exact command(s) that must pass after every issue, e.g. `make verify`,
plus any environment preconditions the orchestrator must check before starting.>
 
## Reference map
<Verified pointers to relevant code and patterns.>
 
## Out of scope
<Feature-level exclusions, including decisions cut because they were unresolved.>
 
## Issues
<Number, title. Strictly ordered: issue N assumes N-1 is committed and green.>
 
## Open questions
<Only items affecting work beyond this spec. Never anything an executor needs.>
```
 
### `issues/NN-slug.md`
 
```markdown
# NN — <title>
 
Read `../spec.md` first. It binds this issue.
 
**Status:** ready
 
## What to build
<One coherent milestone, end to end. Assumes all prior issues are committed
and green.>
 
## Files
<Expected created/modified files or verified patterns. Everything else is
out of bounds; the verifier diffs against this list.>
 
## Out of scope
<Tempting adjacent work that must not be included.>
 
## Definition of Done
<Machine-checkable only: each criterion is a command with its expected
output or exit status. Includes the spec's verification command. No
criterion may require human judgment.>
 
## On failure
<What the executor does when blocked, including by a defect in a prior
issue: stop immediately, do not work around it, report file, line, and the
failing command's output. State assumptions instead of asking questions.>
```
 
## Issue design rules
 
- Use **vertical slices**: implementation and tests together; leave the repo green.
- Size issues as **milestones**: as large as can still be verified end to end
  with one coherent Definition of Done, and small enough that a failed run can
  be discarded and retried cheaply. Expect roughly 2–4 issues per spec.
- The ceiling is the **verification boundary**, not the context window: if the
  DoD needs two unrelated stories to explain, split; if two issues can only be
  verified together, merge them.
- Never split to ease implementation or to shorten diffs — no human reviews
  mid-run.
- Execution is **strictly sequential**: no `Blocked by` field, no parallelism,
  no worktrees. Issue order is execution order.
- Every issue must be executable by a fresh agent with only the spec, issue,
  repository docs, and codebase — sized for a mid-tier implementation model
  (e.g. Sonnet): explicit references over cleverness.

## Writing rules
- Never rely on the original conversation.
- Never copy secrets.
- Put shared knowledge in `spec.md`; do not repeat it across issues.
- Every Definition of Done criterion is a command, not a description.
- Keep every sentence useful: decision, invariant, reference, scope, work, or
  completion criterion.

# 5. Self-check, then hand off
Before finishing, verify for every issue that:
- it can be implemented without guessing;
- every DoD criterion is a command a verifier can run without judgment;
- it assumes nothing beyond prior issues, repo docs, and the codebase;
- it is a genuine milestone — not artificially small, not two milestones fused;
- a failed attempt at this issue can be discarded and retried without manual
  cleanup;
- no open question touches it.
Then report the artifact path, the ordered issue list, and anything cut to
Out of scope because it was unresolved.
