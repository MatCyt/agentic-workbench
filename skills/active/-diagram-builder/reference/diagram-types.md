# Diagram types

Pick one type per page.

## 1. Infrastructure
- **For:** developers, ops.
- **Shows:** cloud resources and how they relate, secrets/config. No deployment.
- **Notes:** use resource icons when possible. Resources that belong together (same environment, resource group, tenant) sit on a light background `GROUP` box drawn under them. Draw one stack, not one per environment, unless asked. Example: `reference/infra.png` (resource icons keep their own colors, the trust boundary is a dashed `ACCENT` line, edges carry protocol + auth labels).

## 2. External dependencies & actors
- **For:** developers, architects, new joiners.
- **Shows:** the system in the middle, everything it depends on or serves around it (systems, groups, users).
- **Notes:** a side note per dependency: what it's for, what data goes in/out, how often.

## 3. Data flow
- **For:** data-heavy processes, pipelines.
- **Shows:** each location where data is stored and main steps that data goes through
- **Notes:** animated (moving) arrows.

## 4. Data validation / quality gates
- **For:** processes with important checks before side effects.
- **Shows:** each check in order: what it verifies, what happens on failure.
- **Notes:**
  - Gate sub line states the rule in plain words, as what must be true (`no gaps between consecutive hours`), not how the code checks it (`exact end_datetime match`, `constant-time compare`).
  - Outcome card: error code as title, sub line says what the input got wrong in user terms (`same hour submitted twice`), not the consequence (`file failed`, `request rejected`).
  - Add one concrete failing example only when the rule isn't obvious from its wording. No valid/invalid pair per gate.

## 5. Business execution flow
- **For:** business team, external users.
- **Shows:** what happens, in plain English, start to outcome, including failure paths.
- **Notes:** no function/table names; outcomes in user terms. Complex parts of the logic can link to a domain concept explainer (see 9). Example: `reference/business-logic.png`.

## 6. Technical execution flow
- **For:** developers, on-call.
- **Shows:** execution steps end to end.
- **Notes:** descriptions beside steps (outside boxes). Add drill-down pages only for complex stages with several steps; name functions/tables there.
- **Suggested subpage:** failure & recovery matrix (see 8).
- **Example:** `reference/orders-api.drawio` (renders `reference/orders-api-*.png`).

## 7. Lifecycle / state
- **For:** entities with a status field changed by several actors or events.
- **Shows:** states as boxes, events as arrows, legal transitions only.
- **Notes:** trigger on every arrow; terminal states marked.

## 8. Failure & recovery matrix
- **For:** on-call, developers. Usually a subpage of 6, standalone for multi-system writes.
- **Shows:** table: failure point × what's stored where × what the client sees × alert × recovery.

## 9. Domain concept explainer
- **For:** a complex business rule or one with edge cases.
- **Shows:** the rule on a timeline/scale with worked examples (pass vs fail).
