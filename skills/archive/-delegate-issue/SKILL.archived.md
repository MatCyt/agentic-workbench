---
name: -delegate-issue
description: >-
  Autonomously execute one issue from a .scratch/<feature>/ plan: fresh worktree,
  implement within scope, verify, self-review, commit, push, open a PR. User-invoked
  only. Usage: /auto-issue <path-to-issue-file>.
disable-model-invocation: true
user-invocable: true
argument-hint: "[mandatory: path to the issue file]"
---

# mc-delegate-issue — one issue → one PR

## Process

### 1. Read

- No issue path given → ask; don't guess.
- Read `spec.md` in the issue's feature directory **and** the issue file, fully — you
  have no other context.
- Issue status `done` or `in-progress` → say so and stop. Blockers not all `done` →
  say so and stop.

### 2. Pre-flight — resolve everything now

- Open questions in the spec blocking this issue → ask the user **before starting**;
  there is no mid-run gate to catch a guess.
- Set the issue's `Status:` to `in-progress` and commit that flip on the base branch —
  it must be visible to parallel runs.
- Create a fresh worktree and branch (`issue/NN-<slug>`) from the base branch. All
  work happens there — never in the main checkout.

### 3. Execute — inside the fence

- Touch only the issue's listed files, plus mechanical side effects a change forces
  (lock file) — flag those in the PR description.
- Out of scope means out of scope — note temptations in the PR description instead.
- If the plan is wrong or infeasible as written: **stop, report, clean up the
  worktree** — do not open a best-guess PR. Unrecorded deviations poison later issues.

### 4. Verify

`make verify` if the Makefile defines it, else:
`uv run ruff check && uv run pytest && uv run mypy && uv run deptry`
Does not pass → fix within scope, or stop and report. Never PR red.

### 5. Self-review

Run the mc-code-review skill on the diff. Address its findings within the issue's scope;
findings out of scope go in the PR description, not the code.

### 6. Deliver

- Set the issue's `Status:` to `done`, commit everything on the branch, push.
- Open a PR titled `NN: <issue title>`, body:
  - **Issue**: path to the issue file
  - **Changed**: each file, one line
  - **Verification**: commands run, result
  - **Review findings addressed / deferred**
  - **Deviations**: or "none"
  - **Review focus**: echoed from the issue
- Remove the worktree. Report the PR URL and which issues are now unblocked.