---
name: -implement-spec
description: Implement a spec produced by /-to-spec-delegated. Orchestrates implementer subagents over the issue graph on one integration branch, then reviews and ships.
disable-model-invocation: true
user-invocable: true
argument-hint: "[spec dir: .scratch/specs/<feature>/ — default: the only or newest one]"
---

# Implement Spec

Input: a spec directory `.scratch/specs/<feature>/` containing `spec.md` and `issues/NN-<slug>.md`. If none is given, use the only spec dir; if several exist, use the newest and say so.

Goal: the entire spec implemented on a single **integration branch**, every issue `done`, reviewed, and shipped as a PR.

## The issue files are the tracker

- `**Status:**` is the state machine: `ready → in-progress → done | blocked`.
- `**Depends on:**` is the graph. The **frontier** is every issue with status `ready` whose dependencies are all `done`.
- Status and Deviations are written only to the issue file in the main checkout, never in a worktree. Worktrees do not see untracked `.scratch/`, so pass the **absolute path** of the spec dir to every subagent. One location holds all state.

## Communication

Sparse. Subagents get **context pointers** (absolute spec dir, issue file, integration branch name, relevant commit SHAs), never a restatement of their contents.

## Steps

1. Read `spec.md` and all issues. Build the graph and the initial frontier.

2. Create the integration branch `<feature>` from the current base branch. Record the base branch name.

3. For every issue on the frontier, set its status to `in-progress` and launch an **implementer subagent** in the background, mid-tier model, in its own worktree on branch `<feature>/NN-<slug>` cut from the integration branch tip. Brief it with the rules below.

4. When an implementer reports done:
   - `git merge --no-ff <feature>/NN-<slug>` into the integration branch. Merges should be trivial because parallel issues never share files; spawn a subagent to resolve a conflict only if one actually occurs.
   - Set the issue status to `done` (or `blocked` with the reason the implementer gave).
   - Recompute the frontier and launch implementers for any newly unblocked issues. Keep the loop going until no issue is `ready` or `in-progress`.

5. Run `-code-review` on the integration branch with fixed point = the base branch and the spec path as argument. Fix all findings in a single implementer subagent on the integration branch.

6. Run `-ship-it` with `branch` = the base branch and `context` = `spec.md` plus every non-empty Deviations section.

7. Clean up: remove every implementer worktree and delete every `<feature>/NN-*` branch.

8. Report: PR URL, blocked issues with reasons, and issues that recorded deviations.

## Implementer rules

Each implementer subagent:

- Reads `spec.md` and its issue file first. The spec binds the issue.
- Confirms its worktree is on a branch cut from the integration branch tip; resets onto it if not.
- Touches **only the files listed in the issue**. Anything else is out of bounds.
- Implements "What to build" end to end, including tests, until the Definition of Done passes.
- May diverge from the spec or issue when implementation shows it is necessary. Every divergence is appended to the issue's **Deviations** section with what changed and why. Divergence without a record is a failure.
- If the Definition of Done cannot be met, stops, reports why, and the orchestrator marks the issue `blocked`.
- Makes exactly **one commit**, subject `NN: <issue title>`. No body, no trailers, no AI attribution.
- Merges the integration branch tip into its own branch before reporting done.
- Reports in one or two lines: commit SHA, DoD result, whether deviations were recorded.
