---
name: -to-spec-hands-on
description: >-
  Convert the current planning conversation into a spec plus a strictly sequential chain of
  runnable steps under .scratch/walkthroughs/<feature>/, for building something in a domain the
  user does not yet understand (new service, new API, new protocol). Every step ends with
  something the user runs and observes against the real system. Abstractions and models arrive
  only after the real data they describe has been seen. Earlier steps are rewritten as
  understanding grows. Use when the goal is the user's understanding, not fast delegation.
disable-model-invocation: true
user-invocable: true
argument-hint: "[optional: feature slug; default: derived from the conversation]"
---

# -to-spec-hands-on — conversation → spec + runnable steps

The user will own the result in production but does not yet understand the domain. The plan
must mimic how they would build it by hand: a hello-world against the real system first, then
one observable increment at a time, rewriting earlier work as the picture sharpens.

Success test: **after every step the user can run one command, see real output, and explain
what the code did to get it.** A step the user cannot observe is a failed step.

The destination is the complete, production-shaped feature following every repo convention,
with tests, docs, and deployment. Only the path differs: longer, strictly sequential, and it
rewrites early work.

This skill produces the plan only. Do not implement anything.

## Process

### 1. Harvest the conversation

Extract locked decisions with rationale, rejected alternatives, invariants, referenced files
and docs, and unresolved decisions. Additionally:

- What the user already understands versus what is new to them (ask if unclear). New
  concepts drive the step order; known ones can be batched.
- Which external system the code talks to and how it can be exercised safely (sandbox,
  read-only endpoints, a UI that shows the effect of a write).

### 2. Verify against the repository

Verify every referenced path and symbol. Read `AGENTS.md` and `ARCHITECTURE.md` if present.
Use `make verify` when available, otherwise the repository's normal lint, test, type-check,
and dependency checks.

### 3. Close the gaps

Ask the user to resolve every unresolved decision now. Confirm the **observation channel**
for each external effect: where will they see a connection, a message, a record? A step
whose result cannot be observed must be re-cut until it can.

### 4. Write the artifacts

```text
.scratch/walkthroughs/<feature-slug>/
  spec.md
  steps/01-<slug>.md      # strictly sequential; each blocked by the previous
  steps/02-<slug>.md
```

**spec.md** sections:

- **Decisions** (locked, with why), **Invariants**, **Reference map**, **Out of scope**,
  **Open questions**.
- **Target end state**: the finished product. Every module and its responsibility, the API
  contract, tests, README, deploy. The last step must land exactly here.
- **Concepts**: the domain concepts the steps introduce, one line each, in order, naming the
  step that first makes each observable.
- **Steps**: one line each: number, title, what becomes runnable.

Locked decisions stay locked, but a step that first touches the real system may reveal one
was wrong. The executor stops and surfaces the conflict rather than building around it.

**steps/NN-slug.md** skeleton:

```markdown
# NN — <title>

Read `../spec.md` first. Decisions, invariants, and references there bind this step.

**Blocked by:** <NN-1, or "none — ready">
**Status:** ready

## What to build
<One observable increment, end to end.>

## Concepts introduced
<One or two domain ideas this step makes visible, in plain sentences for a reader who has
never met them. Omit when nothing is new.>

## Files
<Created / modified / rewritten. "Rewritten" is explicit: name what from an earlier step
is replaced and why the earlier shape is no longer adequate.>

## Run it
<The exact command, what the terminal should show, and where else to look. Include one
thing to deliberately break or vary and the expected reaction. This is the point of the step.>

## Out of scope
<Tempting adjacent work to leave alone, especially abstractions "for later".>

## Definition of Done
<"Run it" observed as described, plus the verification command. For the first step that
touches the external system, list every checkable assumption the spec makes as a checkbox.>

## Review focus [understanding]
<Questions the user should be able to answer after reading the diff and running it.>
```

## Step design rules

- **Step 1 touches the real system.** Authenticate, fetch or receive one thing, log it raw,
  exit cleanly. No classes, no models, no retries, no tests. A single file is fine.
- **Raw before typed.** Parse with the stdlib and log full payloads until a step has shown the
  real data. Models or dataclasses for a message come after the step that logged it.
- **Two copies before one abstraction.** A class or helper appears in the step where the
  second copy of the same loop or call would otherwise be written. Name the duplication removed.
- **One entry point, always runnable.** Every step keeps a single command the user runs. The
  module-split step is the first allowed to replace the script entry point with the production
  one, and must say what command replaces it.
- **One new concept per step.** Batch only what the user already knows.
- **Rewriting is expected.** A later step may replace an earlier file wholesale. The earlier
  step was still correct: its job was to make something observable.
- **Riskiest external assumption first.** If the spec relies on a fact about the external
  system, the step that can check it comes as early as the dependency chain allows.
- **Hardening last.** Reconnect, backoff, alerts, README, deploy come after the happy path is
  observable end to end. Each still gets its own `Run it` with a deliberate failure.
- **Strictly sequential.** No parallel edges. The chain is the curriculum.
- **Size by comprehension.** A step is small enough when the user can explain every line of
  its diff. Prefer more, smaller steps.
- **Converge on the target.** Every module, test, and document in `Target end state` is owned
  by some step. Temporary shortcuts (single file, dict access, `print`) are named in the step
  that takes them and retired in a named later step.

## Writing rules

- Write for an executor with zero conversation memory.
- Plain words first, then the protocol or API term. Never assume the reader knows a term
  until a step has introduced it.
- Never copy secret values.

## 5. Self-check, then hand off

For each step: can a fresh reader execute it from `spec.md` plus the step file alone? Does
`Run it` name a command and an observable result? Does any model or abstraction appear before
the data or duplication that justifies it? Does the last step land on `Target end state` with
every shortcut retired? Fix the plan until every answer is yes.

Then report: the directory path, the step list, the concepts map, open questions, and how to
start: execute `steps/01-….md` in a fresh session, run it, then move to the next.
