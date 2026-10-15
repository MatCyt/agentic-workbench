---
name: -ship-it
description: Commit all changes and raise a PR. Only run when the user explicitly invokes /-ship-it.
disable-model-invocation: true
user-invocable: true
argument-hint: "[branch: target branch / mandatory; context: spec/ticket/intent for / optional]"

---

# Ship It

Arguments: `branch` (required — if missing, ask and stop), `context` (optional — intent/spec/ticket).

1. If `pre-commit` is available, run it on all files and fix issues until clean.
2. If uncommitted changes exist: `git add -A`, then commit with a one-line conventional-commit subject describing what changed. No body, no trailers, no `Co-Authored-By`, no AI attribution anywhere.
3. Write the PR description (see below).
4. Push `branch` and open a PR with `gh pr create` (title = commit subject, body = the description). No AI attribution in the PR.
5. Report the PR URL.

## PR description

Two sections, in this order.

### Intent — only if `context` was given

2–4 sentences summarizing the intent from the spec/ticket: the problem and the chosen approach. Link the ticket if there is one. Never guess intent from the diff; if no `context`, omit this section entirely.

### Changes — always

Read the diff against `branch` (`git diff <branch>...HEAD`) and show what changed using the `-show-me` skill's visual vocabulary. Pick the smallest view that makes the change clear, usually one, at most two:

- **File tree with responsibility comments** — when the change is where things live or a broad refactor.
- **Call tree / control-flow diff** — when the change is in how code runs (`+`/`-` on a sketched call tree or pseudocode).
- **Mermaid sequence or flow diagram** — when the change is in how components interact.
- **Component tree diff** — for UI structure changes.

Rules:
- Markdown and Mermaid only; GitHub renders both. No HTML artifacts, no screenshots.
- One line of plain text above each visual saying what it shows. No preamble, no restating the diff file by file.
- Keep only the files, calls, and boundaries a reviewer needs to orient; omit the rest.
- If the change is trivial (a few lines, one file), a single sentence is enough; skip the visual.
