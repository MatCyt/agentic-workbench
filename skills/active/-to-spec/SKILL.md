---
name: -to-spec
description: >-
  Convert the current planning conversation into one spec file at
  .scratch/specs/<feature>/spec.md. The spec records intent only: what is built and why,
  decisions, invariants, target end state, external assumptions, done criteria, scope. It holds
  no issues and no order, so the same spec can later be cut by /-to-issues-agentic or
  /-to-issues-walkthrough.
disable-model-invocation: true
user-invocable: true
argument-hint: "[optional: feature slug; default: derived from the conversation]"
---

# -to-spec — conversation → spec

The spec is the intent record: what must be true when the work is done, and why. It never says
in what order or in what pieces the work happens. That is decided later, when the spec is cut
into issues by `/-to-issues-agentic` or `/-to-issues-walkthrough`. Code review and the PR
description read the same file.

Success test: **a fresh reader with only `spec.md` and the repository can cut the work into
pieces without asking, judge whether a diff conforms, and tell when the feature is done.** The
only exception is a part that an open question blocks; the spec names each such part.

Produce the spec only. Do not write issues. Do not implement anything.

## Process

### 1. Harvest the conversation

Extract: what is being built, where, and why; locked decisions with rationale; rejected
alternatives; constraints and invariants; referenced files, docs, and patterns; every external
system the code talks to and every fact about it the plan relies on; domain terms, and which
of them are new to the user; unresolved decisions.

### 2. Verify against the repository

Read `AGENTS.md` and `ARCHITECTURE.md` if present. Verification commands live there; do not
restate them.

Every existing file path written into the spec must have been opened during this session.
Never infer an existing path from naming. Correct stale references. This rule does not apply
to files marked new in **Target end state**.

### 3. Close the gaps

For each unresolved decision:

- Hard to reverse, or it changes **Target end state** or an invariant: ask the user. One
  round, all questions together.
- Anything else: pick the simplest option and record it as a decision marked `(assumed)`.
- The user defers it: **Open questions**, with what it blocks. The blocked part cannot be cut
  into pieces until the question is answered.

For each external system, confirm how it can be exercised safely and where its effects can be
observed. Ask in the same round when the conversation does not say.

### 4. Write `.scratch/specs/<feature-slug>/spec.md`

```markdown
# <Feature> — spec

<What is being built, where, and why. A few sentences.>

## Decisions
<One line per decision, stated in architectural terms so it still holds if files move. Add
the why when it is not obvious. Add a rejected alternative only when an implementer might
plausibly pick it. Mark `(assumed)` when the user did not decide it. Each decision may carry
a verified pointer to current code:>

- <Decision.> *Why:* <reason.>
  Now: `<path>`, pattern in `<path>`

## Invariants
<Rules that must stay true in every piece of the work and after it: what must not break, what
must not be introduced, which boundaries must be respected.>

## Target end state
<The finished product, not the path to it. Whatever way the work is cut, it lands exactly here.>

- **Modules:** every file or module, marked new or changed, with one line of responsibility.
- **Interfaces:** signatures, contracts, schemas, commands, and endpoints that other code or
  people rely on.
- **Tests, docs, deployment:** what must exist at the end.

## External systems
<One block per system the code talks to. Omit the section when there is none.>

- **<System>:** <what the code does with it.>
  - Exercise safely: <sandbox, read-only endpoint, dry-run flag.>
  - Observe: <where an effect shows: terminal, UI, table, bucket.>
  - Assumptions:
    - [ ] <Fact about the system that the design relies on.> If false: <what changes.>

<`[x]` only when the fact was checked against the real system in this session.>

## Done when
<Feature-level checks that a verifier can run or observe once every piece is in. Prefer
commands with expected output. Not a restatement of the repository's standard checks.>

## Concepts
<Domain terms the spec uses that a fresh reader may not know, one line each, in plain words.
Mark `(new to user)` where the conversation showed it. Omit the section when there is none.>

## Out of scope
<Feature-level exclusions and deferred work.>

## Open questions
<Unresolved items, each with the part of **Target end state** it blocks. A blocked part is
not cut into pieces until its question is answered. A question that blocks nothing in this
spec says so.>
```

### 5. Self-check, then report

- Can the work be cut into pieces from this file and the repository alone, except the parts
  that an open question blocks?
- Does every module, interface, test, and document in **Target end state** follow from a
  decision, and does every decision show up in **Target end state** or **Invariants**?
- Is every external fact the design relies on listed as an assumption?
- Does **Done when** fail if a part of the feature is missing?
- Does the file name any order, issue, or dependency between pieces? Remove it.

Fix the spec until every answer is right.

Then report: the file path, decisions marked `(assumed)`, unchecked assumptions, and open
questions with what they block.

## Style

- Write for a reader with zero conversation memory.
- Plain words first, then the protocol or API term.
- Never copy secret values.
- Every sentence is a decision, invariant, reference, assumption, scope, or completion
  criterion.
