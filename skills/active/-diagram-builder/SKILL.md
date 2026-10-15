---
name: -diagram-builder
description: "Draw a draw.io (.drawio) diagram in the house 'Linear light' style, with page-link drill-down to detail pages, using the draw.io MCP."
user-invocable: true
disable-model-invocation: true
argument-hint: "<what to diagram, and where to save it>"
---

# -diagram-builder

This skill defines **how** to draw: the visual style, the drill-down convention, and the tooling. The user's prompt decides **what** to draw. If it doesn't name a view, pick (or propose) one from `reference/diagram-types.md` and follow its notes.

References: open the renders relevant to the requested view before your first diagram and match them. Read the `.drawio` XML only when you need exact cell styles.
- `reference/orders-api.drawio`: full multi-page technical flow (overview, drill-down pages, outcome column, failure-state table). Renders: `reference/orders-api-overview.png`, `-auth.png`, `-validation.png`, `-failures.png`.
- `reference/business-logic.png`: business execution flow in plain English (start pill, gates, loop groups, skip/fail/ok outcomes).
- `reference/infra.png`: infrastructure view (resource icons, nested groups, trust boundary, protocol + auth edge labels).
- `reference/overview.png`: horizontal-row layout with a drillable card.
## 1. Style: Linear light

Calm, low-contrast, mostly white. One accent color (dark blue). Status colors appear only on outcome cards and their arrows.

### Tokens

| Token | Value | Use |
|---|---|---|
| `BG` | `#FCFCFD` | page `background` + label backgrounds on edges |
| `TITLE` | `#1B1B1F` | titles, card titles |
| `SUB` | `#6B6F76` | subtitles, card secondary line, edge labels |
| `ACCENT` | `#004791` | icons, drillable border, links, start pill |
| `BORDER` | `#E4E5E9` | default card stroke |
| `EDGE` | `#C9CAD1` | normal connectors |
| `FAIL` / border | `#D93F4C` / `#F2D4D7` | error outcomes |
| `SKIP` / border | `#C28A00` / `#F0E2BC` | skip / warning outcomes |
| `OK` / border | `#2E9E6A` / `#CBE8D9` | success outcomes |
| `TILE` | fill `#EEF3F8`, stroke `#D3E0EE` | icon tile behind every icon |
| `GROUP` | fill `#F6F6F8`, stroke `#E4E5E9`, dashed `4 4` | loop / grouping container |
| Font | `Helvetica` | everywhere. Do not use Inter or Geist: they aren't installed, and both draw.io and its export fall back to a serif font. |

### Building blocks (copy these styles exactly)

- **Card** (64 high, 260–420 wide):
  `fillColor=#FFFFFF;strokeColor=#E4E5E9;rounded=1;arcSize=14;html=1;whiteSpace=wrap;align=left;verticalAlign=middle;spacingLeft=60;spacingRight=12;fontSize=14;fontFamily=Helvetica;`
  - Label HTML: `<b style="color:#1B1B1F">Title</b><br><span style="font-size:13px;color:#6B6F76;font-weight:normal">one-line detail</span>`. Object text: title 14px, line below 13px. Keep it to one title line plus at most one short sub line.
  - Outcome cards: the same card with only `strokeColor` swapped to the status border (`#F2D4D7` / `#F0E2BC` / `#CBE8D9`). The fill stays white.
- **Icon tile + icon**: add both as **children of the card** (`parent="<card id>"`, coordinates relative to the card) so they move with it.
  - Tile: 36×36 at (12, 14), style `fillColor=#EEF3F8;strokeColor=#D3E0EE;rounded=1;arcSize=24;html=1;`
  - Icon: 18×18 at (21, 23), style from `python scripts/icon.py <Name> <color>`. Use `ACCENT` for steps and the status color for outcome cards.
- **Start / entry pill**: `fillColor=#004791;strokeColor=none;rounded=1;arcSize=50;` with white text and a white icon, and no tile.
- **Decision**: a card with `dashed=1;dashPattern=4 3;` and the icon `Call_Split`. Don't use diamonds.
- **Edges**:
  `edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=blockThin;endFill=1;endSize=6;strokeColor=#C9CAD1;strokeWidth=1.5;fontColor=#6B6F76;fontSize=11;fontFamily=Helvetica;labelBackgroundColor=#FCFCFD;`
  - For failure, skip and other side paths, set `strokeColor` and `fontColor` to the status color and add `dashed=1;dashPattern=4 3;`. Edge (line) labels are 11px. Use short lowercase labels (`fail`, `skip`, `yes`, `no`).
  - When several sources feed one target, give them all `exitX=1;exitY=0.5;entryX=0;entryY=0.5;` so they merge into one trunk instead of crossing cards.
- **Group / loop container**: `fillColor=#F6F6F8;strokeColor=#E4E5E9;dashed=1;dashPattern=4 4;rounded=1;arcSize=3;html=1;`. Put an uppercase caption at fontSize 11 with `letter-spacing:1px` in `SUB` color, **right-aligned** in the top-right corner so it never collides with the vertical trunk edge.
- **Page header**: the title is a `text` cell at fontSize 22, bold, `TITLE` color, at (60, 30). The subtitle is fontSize 12 in `SUB` color, directly below it. It says one thing about the system (scope, source, a key fact), never how the diagram is drawn or how to read it (no "in plain English", "notes on the left…", "blocks with Details › open…").
- **Background**: set `background="#FCFCFD"` on the `mxGraphModel`. Don't add a background rectangle.

### Icons

Use Material Symbols from `https://icons.diagrams.net/assets/material-symbols/1/<Name>.svg`, recolored and embedded with `scripts/icon.py`. Embedded icons work offline and in exports.
- Find names with the MCP's `search_shapes` (for example `"material symbols lock"`), or try a name directly.
- Names that are confirmed to exist: `Play_Circle Lock Data_Object Folder_Open Download Schedule Table Send Check_Circle Skip_Next Error Mail Call_Split Rule Cloud Description`.
- Use one icon per card. Never use emoji as icons.

### Layout

- **Main flow**: one vertical column on the left (x=60–80), 100 px row pitch (64 card + 36 gap). A horizontal row also works for 3–5 blocks.
- **Outcomes**: a second column on the right (about 140 px gap), each card on the same row as the step that produces it.
- Leave plenty of whitespace and keep the grid off (`grid="0"`).
- Step titles are numbered `1 · Name`, with a middle dot (`·`).

## 2. Drill-down: page link + detail page (default)

Give a block a detail page when it hides real complexity (several sub-steps, branching, or details worth showing); simple blocks stay plain. Don't use collapsible containers, toggle actions, tooltips or layers unless the user asks for them.

- **Drillable block**: wrap the card in a `UserObject` that carries the link:
  ```xml
  <UserObject id="auth" label="..." link="data:page/id,auth-detail">
    <mxCell style="...card...;strokeColor=#004791;spacingRight=84;" vertex="1" parent="1">...</mxCell>
  </UserObject>
  ```
  Mark it visibly:
  - the border is `ACCENT` instead of `BORDER`
  - a **`Details ›` pill** is a child of the card, 64×20, right-aligned at (cardW−74, 22), style `fillColor=#EEF3F8;strokeColor=none;rounded=1;arcSize=50;html=1;fontSize=10;fontColor=#004791;fontStyle=1;fontFamily=Helvetica;`
  - `spacingRight=84` keeps the label clear of the pill. Make drillable cards at least 320 wide so the 13px sub line doesn't wrap.

  Blocks without a detail page keep the plain border, so drillable blocks stand out.
- **Detail page**: a separate `<diagram id="auth-detail" name="1 · Authenticate">`.
  - Top-left breadcrumb: an `Overview` link (a `UserObject` text cell with `link="data:page/id,<overview id>"`, `fontColor=#004791`, fontSize 12), followed by `› <b>1 · Authenticate</b>` in `SUB` color.
  - Under the breadcrumb: the page title (fontSize 22), then a one-line subtitle that says where this lives (function / module).
  - Body: the same card and edge styles, showing sub-steps vertically and their outcomes in the right column.
  - Detail pages may link further down, using the same pattern and a breadcrumb that grows (`Overview › Step › Sub-step`).
- **Page ids**: use short, stable, kebab-case ids (`overview`, `auth-detail`). Name pages the way they appear in the breadcrumb.
- Links work in the draw.io desktop app, the web app and HTML export. In the editor you select the block and then click the link hint (or Ctrl+click). Static PNG exports won't navigate, so say so when you hand over PNGs.

## 3. Tooling

- **Write the `.drawio` file yourself**, as one `<mxfile>` with one `<diagram>` per page. The file is the deliverable, because page links need multiple pages.
  - For anything beyond about 10 cells, generate it with a small Python script (style constants plus `card()`, `edge()` and `page()` helpers). Keep the script next to the output so it can be re-run.
  - XML rules: no XML comments. Escape label HTML (`html.escape`). Write newlines inside attributes as `&#10;`. Every cell id is unique within its page.
- **The draw.io MCP** (`create_diagram`, `search_shapes`):
  - Use `search_shapes` to find icon names and stencil styles.
  - Use `create_diagram` with `xml` for a quick inline preview of a single page. It shows one page only, so it can't demonstrate page links. Use Mermaid only for throwaway sketches, because Mermaid output does not follow this style.
- **Verify before handing over**: export every page with the desktop CLI and look at the PNGs.
  ```bash
  "/c/Program Files/draw.io/draw.io.exe" -x -f png -p <N> -s 1 -o previews/page-<N>.png diagram.drawio
  ```
  - `-p` is **1-based**.
  - Check that no edge crosses a card or caption, no pill overlaps a label, and fonts aren't serif.
  - Fix what you find and re-export.
- Validate the XML with `python -c "import xml.dom.minidom as m; m.parse('diagram.drawio')"`.
- Send the PNG previews to the user with SendUserFile, along with a link to the `.drawio` file.
