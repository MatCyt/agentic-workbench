---
name: -audit-tests
description: Deep, adversarial audit of pytest unit tests. Audits test adequacy and depth — which behaviors are actually verified vs merely executed — and produces a TEST_AUDIT.md report. Strictly read-only with respect to the repository; never modifies, repairs, or adds code or tests.
disable-model-invocation: true
user-invocable: true
argument-hint: "[mandatory: unit test directory or file path]"
---


Deep, adversarial audit of pytest unit tests. Invoked ONLY by explicit user request (never proactively) with a mandatory argument pointing to a test directory or file. Audits test adequacy and depth — which behaviors are actually verified vs merely executed — and produces a TEST_AUDIT.md report. Strictly read-only with respect to the repository; never modifies, repairs, or adds code or tests.

Test Audit

Adversarial audit of a pytest test suite. The question is never "how many tests pass?" but "if a realistic bug were introduced into the code under test, would this suite catch it?"

Invocation contract
User-invoked only. Never trigger this skill proactively.
Mandatory argument: path to a test directory or test file. If missing, ask for it — do not guess.
Scope: Python repositories using pytest.
Output: a single TEST_AUDIT.md written into the same directory as the audited tests. This is the ONLY file the skill may create or overwrite in the repository. If a TEST_AUDIT.md already exists, overwrite it (note the previous audit date if one is present).
The prime rule: audit only
Do not modify, repair, refactor, delete, skip, or add any code or tests — even trivially, even if a test is obviously broken, even if a one-line fix would make the suite green.
Do not fix failing tests. Failures are findings, not tasks.
No persistent modifications to the working tree. Tools that need to mutate source (mutmut) must run against a temporary copy of the repository (/tmp copy or a throwaway git worktree), never the live checkout. Verify with git status at the end that the tree is clean except for TEST_AUDIT.md.
Audit phases

Run the phases in order. Each phase feeds evidence into the findings; no phase's raw output is a finding by itself.

### Phase 1 — Contract discovery

The audit compares tests against a behavioral contract, so first establish what that contract is:

Map the test directory to the code under test (imports in test files, conftest.py, package layout).
Derive the contract for each function/class under test from: docstrings, type hints and signatures, README/docs, and reading the implementation itself.
Write down the contract as a list of behaviors: inputs → expected outputs, error conditions, boundaries, invariants, side effects.

This behavior list is the yardstick for everything that follows. List untested behaviors (edge cases, error paths, boundaries) — never untested lines.

### Phase 2 — Hermeticity & safety scan (before running anything)

Statically scan the tests and their fixtures for:

Real network calls, database connections, external service dependencies
File writes outside tmp/tmpdir fixtures
Environment-variable-gated integration tests
Anything destructive or slow

Report non-hermetic tests as findings (they are a reliability defect in their own right). If tests are unsafe to run (e.g., hit production services), skip execution of those tests and record that in the limitations section — do not "fix" them to make them runnable.

### Phase 3 — Test execution

Use the repository's own invocation (tox / make / pytest config in pyproject.toml or setup.cfg), not a bare pytest, to avoid environment-mismatch false failures.

Run the suite once. Record passed / failed / skipped / xfailed / xpassed counts and names. Collection errors are reported distinctly from test failures.
Run it a second time (and, if pytest-randomly or -p no:cacheprovider shuffling is available, once with randomized order). Divergence between runs = flaky or order-dependent tests → findings.
Audit skips: stale skip reasons, permanently-skipped tests, xfails that now pass.
Do not repair any failure. Ever.

### Phase 4 — Coverage as evidence (not verdict)

Run with --cov --cov-branch (and --cov-context=test if available) against the modules under test:

Uncovered branches and error paths become evidence for "missing tests" findings.
The test→lines mapping identifies redundant tests (multiple tests exercising identical paths with identical assertions) — evidence for the "tests that might be deleted" list.
Coverage percentage itself never appears in the verdict rationale.

### Phase 5 — Mutation testing (mutmut)

Point mutmut at the source modules under test (not the test files), running inside the temporary copy:

Budget it: cap mutant count / restrict to the mapped modules, set a per-mutant timeout, and set an overall time budget. Partial results are acceptable and must be labeled as partial.
If mutmut fails on the codebase (v3 compatibility issues, dynamic imports), fall back to manual mutation reasoning: for each function under test, reason about specific assertion deletions, operator inversions, boundary shifts, and whether any test would fail.
Map every surviving mutant back to a named finding ("mutant at pricing.py:42 — >= → > survives → no test pins the boundary at exactly 100"). Never dump a raw mutant list.

### Phase 6 — Adversarial interrogation (all evaluated tests)

For every test covering the evaluated functions — not a sampled subset — determine:

Which plausible defects it would catch
Which plausible defects would survive it
Whether it can pass without exercising the intended behavior
Whether assertions are overly broad, tautological, or coupled to internals
Whether mocks reproduce implementation logic (test mirrors the code, verifies nothing)
Whether the test verifies outcomes or merely that a mock was called

Apply the assertion-smell taxonomy with named smells so findings are consistent:

Smell	Description
assertion-free	Calls code, asserts nothing ("call and pray")
truthy-assert	assert result instead of asserting the value
broad-raises	pytest.raises(Exception) or overly wide exception catches
tautology	Assertion true by construction (compares value to itself / to the mock's own return)
mock-mirror	Mock re-implements the logic under test
interaction-only	Asserts the mock was called, not what the outcome was
no-autospec	Non-autospec mocks / patch on wrong namespace — silently accepts any signature
snapshot-blind	Golden/snapshot files regenerated wholesale without review
happy-parametrize	Parametrization lists only cheerful values, no boundaries

### Phase 7 — Missing-test recommendations

For each contract behavior with no adequate test, recommend a test in one of two shapes:

Boundary/example tests — when coverage exists at happy-path values only: recommend concrete cases (empty, None, zero, negative, huge, unicode, whitespace, off-by-one at documented limits).
Property tests — when the contract is algebraic: recommend a hypothesis-style property (round-trip deserialize(serialize(x)) == x, invariants, idempotence) instead of more hand-picked examples.

Name which shape fits and why.

### TEST_AUDIT.md structure

The report must follow this order:

1. Verdict (first, always)

A judgment of the suite's adequacy and depth, never derived from test count, pass rate, or coverage percentage. Use this rubric — the question for each level is "would this suite catch a realistic regression in each core behavior?":

STRONG — core behaviors pinned by meaningful assertions; realistic regressions would fail the suite
ADEQUATE — most core behaviors verified; specific named gaps exist
WEAK — tests execute code but many core behaviors are unverified; significant classes of bugs would pass
INADEQUATE — suite provides false confidence; a green run says little about correctness

The verdict must cite the specific findings that justify it (2–4 sentences).

2. Test run summary

Passed / failed / skipped / xfailed / xpassed counts; collection errors listed separately; flaky/order-dependent tests noted; commands, tool versions, and timestamp recorded for reproducibility.

3. Findings, ordered by impact

Grouped Critical / High / Medium / Low. Every finding has:

A stable ID (TA-001, TA-002, …)
A path/to/test_file.py::test_name reference (or module reference for missing-test findings)
Attached evidence: surviving mutant, uncovered branch, smell name, run divergence — something checkable
Its recommendation category:
Category	Required content
Tests to add	The behavior left unverified, why it matters, and the recommended shape (boundary cases listed concretely, or the property to assert)
Tests to delete	Why the test adds no protection (redundant path+assertions, tautological, permanently skipped) — evidence attached
Tests to modify	Why the current form is inadequate + a short, specific recommended change (e.g., "replace assert result with equality against the expected dict; add the None input case")

Recommendations are written down only — never applied.

4. Limitations

What the audit could not verify and why: mutmut timeout or incompatibility, tests skipped for hermeticity, collection errors blocking parts of the suite, partial mutation results. An audit that hides its own blind spots commits the sin it is auditing for.

Explicitly out of scope
Git history forensics — no analysis of commit history, assertion weakening over time, or test/code co-changes.
Fixing anything.
Auditing non-pytest or non-Python suites (state this and stop if encountered).