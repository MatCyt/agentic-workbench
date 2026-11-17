---
name: -to-issues-walkthrough
description: >-
  Cut a spec written by /-to-spec into a strictly sequential chain of runnable issues under
  .scratch/specs/<feature>/issues-walkthrough/, for building something in a domain the user
  does not yet understand (new service, new API, new protocol). Every issue ends with
  something the user runs and observes against the real system. Abstractions and models arrive
  only after the real data they describe has been seen. Earlier work is rewritten as
  understanding grows. Use when the goal is the user's understanding, not fast delegation.
disable-model-invocation: true
user-invocable: true
argument-hint: "[spec dir: .scratch/specs/<feature>/ — default: the only or newest one]"
---

# -to-issues-walkthrough — spec → runnable issues

Input: a spec directory `.scratch/specs/<feature>/` containing `spec.md`. If none is given, use
the only spec dir; if several exist, use the newest and say so. If there is no `spec.md`, stop
and tell the user to run `/-to-spec` first.

The user will own the result in production but does not yet understand the domain. The issues
must mimic how they would build it by hand: a hello-world against the real system first, then
one observable increment at a time, rewriting earlier work as the picture sharpens.

Success test: **after every issue the user can run one command, see real output, and explain
what the code did to get it.** An issue the user cannot observe is a failed issue.

The destination is the spec's **Target end state**: the complete, production-shaped feature
following every repo convention, with tests, docs, and deployment. Only the path differs:
longer, strictly sequential, and it rewrites early work.

The spec is the intent record and the single source. This skill decides only the path. It adds
no decision of its own.

Produce the issues only. Do not implement anything.

## Process

### 1. Read the spec

Read `spec.md` in full. Read `AGENTS.md` and `ARCHITECTURE.md` if present. Verification
commands come from there; do not restate them.

Take from the spec:

- **Concepts**, with the `(new to user)` marks. New concepts drive the issue order; known ones
  can be batched.
- **External systems**: how each one is exercised safely, where its effects are observed, and
  which assumptions are still unchecked.

The spec is the only source of intent. When the conversation holds something that the spec
does not, the spec has a gap: handle it in step 3.

### 2. Verify against the repository

Every existing file path or symbol written into an issue must have been opened during this
session. Never infer an existing path from naming.

### 3. Close the gaps, spec first

Ask the user, one round, all questions together. Write every answer into `spec.md` before
writing an issue.

- Each open question that blocks a part of **Target end state**. A part that stays blocked is
  not cut.
- Which concepts are new to the user, where the spec does not say.
- The **observation channel** for each external effect, where the spec does not name it:
  where will they see a connection, a message, a record? An issue whose result cannot be
  observed must be re-cut until it can.
- Anything in the spec that reading or verification showed to be wrong. Correct a stale path
  or reference directly, without a question.

An issue never holds a correction that the spec does not hold.

### 4. Write `.scratch/specs/<feature-slug>/issues-walkthrough/NN-<slug>.md`

```text
.scratch/specs/<feature-slug>/
  spec.md
  issues-walkthrough/
    01-<slug>.md      # strictly sequential; each blocked by the previous
    02-<slug>.md
```

```markdown
# NN — <title>

Read `../spec.md` first. Decisions, invariants, and references there bind this issue. If
building or running this issue shows that the spec is wrong, stop and tell the user. The spec
is corrected first; do not build around it.

**Blocked by:** <NN-1, or "none — ready">
**Status:** ready

## What to build
<One observable increment, end to end.>

## Concepts introduced
<One or two domain ideas this issue makes visible, in plain sentences for a reader who has
never met them. Omit when nothing is new.>

## Files
<Created / modified / rewritten. "Rewritten" is explicit: name what from an earlier issue
is replaced and why the earlier shape is no longer adequate.>

## Run it
<The exact command, what the terminal should show, and where else to look. Include one
thing to deliberately break or vary and the expected reaction. This is the point of the issue.>

## Out of scope
<Tempting adjacent work to leave alone, especially abstractions "for later".>

## Definition of Done
<"Run it" observed as described, plus the verification command. List as a checkbox each
unchecked assumption from the spec's **External systems** that this issue can check. When one
is confirmed, tick it in `spec.md` too.>

## Review focus [understanding]
<Questions the user should be able to answer after reading the diff and running it.>
```

### 5. Self-check, then hand off

- Can a fresh reader execute each issue from `spec.md` plus the issue file alone?
- Does every `Run it` name a command and an observable result?
- Does any model or abstraction appear before the data or duplication that justifies it?
- Is every concept marked `(new to user)` in the spec introduced by one issue?
- Is every unchecked assumption in the spec listed in the earliest issue that can check it?
- Does the last issue land on **Target end state** with every shortcut retired, except the
  parts that an open question blocks?

Fix the issues until every answer is right.

Then report: the issues directory path, the issue list, the concepts map (concept → the issue
that first makes it observable), changes made to `spec.md`, parts not cut because an open
question blocks them, and how to start: execute `issues-walkthrough/01-….md` in a fresh
session, run it, then move to the next.

## Issue design rules

- **Issue 1 touches the real system.** Authenticate, fetch or receive one thing, log it raw,
  exit cleanly. No classes, no models, no retries, no tests. A single file is fine.
- **Raw before typed.** Parse with the stdlib and log full payloads until an issue has shown
  the real data. Models or dataclasses for a message come after the issue that logged it.
- **Two copies before one abstraction.** A class or helper appears in the issue where the
  second copy of the same loop or call would otherwise be written. Name the duplication removed.
- **One entry point, always runnable.** Every issue keeps a single command the user runs. The
  module-split issue is the first allowed to replace the script entry point with the
  production one, and must say what command replaces it.
- **One new concept per issue.** Batch only what the user already knows.
- **Rewriting is expected.** A later issue may replace an earlier file wholesale. The earlier
  issue was still correct: its job was to make something observable.
- **Riskiest external assumption first.** If the spec relies on a fact about the external
  system, the issue that can check it comes as early as the dependency chain allows.
- **Hardening last.** Reconnect, backoff, alerts, README, deploy come after the happy path is
  observable end to end. Each still gets its own `Run it` with a deliberate failure.
- **Strictly sequential.** No parallel edges. The chain is the curriculum.
- **Size by comprehension.** An issue is small enough when the user can explain every line of
  its diff. Prefer more, smaller issues.
- **Converge on the target.** Every module, interface, test, and document in the spec's
  **Target end state** is owned by some issue. Temporary shortcuts (single file, dict access,
  `print`) are named in the issue that takes them and retired in a named later issue.

## Writing rules

- Write for an executor with zero conversation memory.
- Plain words first, then the protocol or API term. Never assume the reader knows a term
  until an issue has introduced it.
- Never copy secret values.
- Shared knowledge lives in `spec.md`; issues do not repeat it.
