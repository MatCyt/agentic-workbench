# AGENTS.md

Project-specific context and requirements lives in ./ARCHITECTURE.md

## Communication 
- Answer shortly by default, talk in ASD-STE100 Simplified Technical English.
- When asked for a recommended solution, shortly list pros and cons plus alternative approaches.
- For conceptual or feasibility questions, answer in chat first; wait for my go-ahead before implementing.
- If a requirement is ambiguous and the choice is hard to reverse, ask; otherwise pick the simplest option and say so.

## Stack & tooling
- **Python** with **uv**. Use `uv run <cmd>` rather than activating a venv.
- **Makefile** wrappers for the standard commands
- **ruff** as the only linter/formatter, strict template, configured once at repo root (`ruff.toml`).
- **mypy** for type-checking. **deptry** for unused/missing dependency checks.
- **pre-commit** running ruff, uv-lock, gitleaks. Fix hook failures, never bypass.

## Commands
Run from the directory that contains the `pyproject.toml` you are working in.
- `make verify` — full check: lint, typecheck, deps, tests. Must pass before a change is done.
- `uv add <pkg>` / `uv add --group dev <pkg>` — add dependencies; never edit `pyproject.toml` by hand


## General Rules
- Never commit unless explicitly instructed.
- Change only what the task requires. Don't refactor, rename, or reformat unrelated code; mention it instead.
- Read/search freely, but confirm before destructive operations (deleting data, force-pushing, sending messages, modifying shared infra) unless durably authorized.
- Apply YAGNI principles, no unrequested abstractions, config options.
- Prefer simple, local code over abstract code. Readability at the call site beats DRY. Extract only when the logic is non-obvious, protects a real invariant, or must change in exactly one place. 
- Keep the entrypoint an orchestration layer only; separate modules by concrete responsibility.
- Keep small applications flat: one module per concern, no `src/` nesting or sub-packages until size or reuse justifies them.
- Inject external dependencies (DB, storage, HTTP, cloud clients) so business logic is testable without real infrastructure.
- Docstrings: one line stating purpose. Add `Args:`/`Returns:`/`Raises:` only when the signature alone doesn't explain behavior.
- Comments explain why an invariant or ordering matters; they never restate the code.


## Constants, configuration, secrets
- Read required configuration with `os.environ["X"]` so missing config fails fast. Use `os.getenv` only for genuinely optional lookups.
- Ship a `.env.example`. When adding or renaming an env var, update .env.example.

## Logging
- One `logger = logging.getLogger(__name__)` per module. Configure `logging.basicConfig(...)` only in the entrypoint.
- Use `%s` lazy placeholders, never f-strings, in log calls.
- Levels: `info` for main execution steps; `warning` for expected rejections; `logger.exception(...)` inside `except` blocks.

## Data & input validation
- Use plain types, no schema for simple local values
- Dataclass for internal data validated at the boundary
- Pydantic for External API responses, request/response bodies, webhooks, LLM output, loaded config
- Do not use pydantic for batch, dataframes, columnar data
- When a batch must succeed or fail as a whole, validate every item first; start writing only after all pass.
- Two layers: shape and format validation in Pydantic at the boundary; business rules as plain `validate_*` functions, guard-clause style, raising a domain error. No business logic in Pydantic validators.

## Testing
- pytest + `pytest-mock` (`MockerFixture`). Test functions fully type-annotated.
- Mock external boundaries, not the business rule being tested. Cover boundary values explicitly.
- Test names read as specifications: `test_<unit>_<expected_behavior>_<condition>`. One behavior per test; group tests per unit under a `# --- unit_name ---` comment.
- Shared fixtures carry a docstring stating what is real and what is mocked.

## Stack-specific coding conventions

### FastAPI services
- All errors use one body: `{"detail": {"error_code": "...", "message": "..."}}`. Reformat `RequestValidationError` into it (`PAYLOAD_INVALID`). A catch-all `Exception` handler returns `INTERNAL_ERROR` 500 with no internal detail — specifics go to logs and alerts only. Register all handlers in one `register_exception_handlers(app)`.
- Constrain fields, not just type them: ranges, patterns, `max_length` on collections.
- Expensive shared clients (DB, HTTP) are created in lifespan and stored on `app.state`; never module-level globals.
- OpenAPI metadata describes the public contract only. Internal flows, failure modes and recovery go in the README. Infrastructure, secrets and deployment details appear in neither.