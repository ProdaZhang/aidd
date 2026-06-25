# Phase · UI capture — screenshot → UI DSL

Turn a UI screenshot (a reference product or your own) into a structured **UI DSL** (`.md`): structure / type / hierarchy / geometry / interaction / state. The DSL is the input to the deterministic scripts `ui_render.py` (re-render to a wireframe) and `ui_slice.py` (per-element slices). **This playbook only orchestrates the flow — the grammar/recipe is canonical in [`../ui-dsl-spec.md`](../ui-dsl-spec.md)** (no need to edit this file when the spec changes).

## Step 0 — read the canonical source (every time, with Read, not from memory)
| File | What to take |
|------|--------|
| [`../ui-dsl-spec.md`](../ui-dsl-spec.md) | file skeleton + Layout-line grammar + type table + z-layering + shape + source semantics + **reading recipe** + **skin/theme** |
| [`../scripts/ui_render.py`](../scripts/ui_render.py) | re-render + missing-z reminder + calibration export |
| [`../scripts/ui_palette.py`](../scripts/ui_palette.py) | sample colors from the source → write a `## Skin` block |
| [`../scripts/ui_slice.py`](../scripts/ui_slice.py) | image + DSL → per-element slices + a contact-sheet index (optional) |
| [`../ui-dsl-example.md`](../ui-dsl-example.md) | what a compliant DSL looks like |

## Steps
1. **Inputs**: one screenshot + a `screenID` + the `source` (reference product / your own) + a one-line `purpose`. Ask for anything missing.
2. **Produce the DSL** per the spec's reading recipe: screen header → palette → Layout (outer→inner, container before leaf, each element typed with `@{x y w h} z=N`) → Events → design notes. A reference source is tagged `:observed` / `:inferred`, **never `:canonical`**.
3. **Run the renderer to verify (close the loop)**:
   ```
   python ../scripts/ui_render.py <screenID>.md <out>.html --svg <out>.svg
   python ../scripts/ui_palette.py <screenID>.md <source-image> --merge
   ```
   Open the html, **eyeball it against the original**: hierarchy / proportions / text / interaction. Off → use the html "calibrate" handles → "export DSL" → re-run. The check scope is **structure / proportion / hierarchy / text / interaction, not art**.
4. **File it** into the patterns knowledge base (`references/patterns/ui-paradigms/<product>/<screenID>.{md,html}`) with an INDEX line, for design-time retrieval.

## Hard constraints
- **Capture must tag `z=`** (renderer discipline, not enforced by render).
- **No guessing**: shape / hierarchy only from the md declaration; the renderer infers nothing from aspect ratio.
- **Reference source** uses `:observed` / `:inferred` only, never invents `:canonical`.
- Files are **UTF-8 without BOM**.
