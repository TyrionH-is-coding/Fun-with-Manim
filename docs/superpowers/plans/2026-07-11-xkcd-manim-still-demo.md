# XKCD-Style Manim Still Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Render a 1920×1080 Manim still that demonstrates a recognizable xkcd-like Cueball character, the licensed HYTianZhenTi font, and bubble-free dialogue layout.

**Architecture:** Store the character as a small SVG with named body-part groups, then import it as an `SVGMobject` in one focused Manim scene. Keep the font external and register it temporarily while constructing `Text`. Validate the asset structure, font registration, scene builders, and final PNG with pytest before visual inspection.

**Tech Stack:** Python 3.12, Manim Community 0.20.1, ManimPango, SVG, pytest, Pillow

---

## File Map

- `assets/xkcd_cueball_study.svg`: reusable vector character with named head, torso, arm, and leg groups.
- `src/__init__.py`: marks the scene source directory as an importable package.
- `src/xkcd_manim_demo.py`: font registration, SVG loading, composition, and the Manim scene.
- `tests/test_demo_assets.py`: verifies the SVG is vector-only and contains the required named parts.
- `tests/test_demo_scene.py`: verifies the supplied font registers under the expected family and scene builders produce valid Manim objects.
- `tests/test_render_output.py`: verifies the final deliverable exists at the required resolution and contains visible ink.
- `outputs/xkcd_manim_demo.png`: final user-facing still.

The font remains at `C:/Users/15694/Downloads/HYTianZhenTi.ttf`; it is never copied into the repository.

### Task 1: Create and Validate the Vector Character Asset

**Files:**
- Create: `tests/test_demo_assets.py`
- Create: `assets/xkcd_cueball_study.svg`

- [ ] **Step 1: Write the failing SVG structure tests**

Create `tests/test_demo_assets.py`:

```python
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SVG_PATH = ROOT / "assets" / "xkcd_cueball_study.svg"
EXPECTED_IDS = {
    "head",
    "torso",
    "left-arm",
    "right-arm",
    "left-leg",
    "right-leg",
}


def test_svg_exists() -> None:
    assert SVG_PATH.is_file(), f"Missing vector asset: {SVG_PATH}"


def test_svg_has_named_body_parts() -> None:
    root = ET.parse(SVG_PATH).getroot()
    ids = {element.attrib["id"] for element in root.iter() if "id" in element.attrib}
    assert EXPECTED_IDS <= ids


def test_svg_contains_no_embedded_raster_image() -> None:
    root = ET.parse(SVG_PATH).getroot()
    local_names = {element.tag.rsplit("}", 1)[-1] for element in root.iter()}
    assert "image" not in local_names
```

- [ ] **Step 2: Run the tests and verify the missing asset failure**

Run:

```powershell
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_demo_assets.py -v
```

Expected: `test_svg_exists` fails with `Missing vector asset`.

- [ ] **Step 3: Create the minimal named SVG asset**

Create `assets/xkcd_cueball_study.svg`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 420">
  <g fill="none" stroke="#111111" stroke-width="6"
     stroke-linecap="round" stroke-linejoin="round">
    <g id="torso">
      <path d="M131 126 C128 158 131 205 132 255"/>
    </g>
    <g id="left-arm">
      <path d="M130 154 C113 168 99 194 78 207 C68 213 58 212 48 216"/>
    </g>
    <g id="right-arm">
      <path d="M132 155 C145 172 153 194 164 221"/>
    </g>
    <g id="left-leg">
      <path d="M132 254 C122 281 112 317 102 365"/>
    </g>
    <g id="right-leg">
      <path d="M132 254 C143 282 157 318 171 360"/>
    </g>
    <g id="head" fill="#ffffff">
      <path d="M130 24 C101 22 82 38 79 66 C76 93 93 118 121 125 C150 131 174 113 181 85 C187 58 175 33 151 26 C143 24 136 23 130 24 Z"/>
    </g>
  </g>
</svg>
```

The torso and limbs are open Bézier paths. The head is last in paint order and has an opaque white fill, so body strokes terminate behind it.

- [ ] **Step 4: Run the asset tests**

Run:

```powershell
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_demo_assets.py -v
```

Expected: `3 passed`.

- [ ] **Step 5: Commit the tested asset**

```powershell
git add -- assets/xkcd_cueball_study.svg tests/test_demo_assets.py
git commit -m "feat: add named xkcd-style character asset"
```

### Task 2: Build and Test the Manim Scene

**Files:**
- Create: `src/__init__.py`
- Create: `tests/test_demo_scene.py`
- Create: `src/xkcd_manim_demo.py`

- [ ] **Step 1: Write the failing font and builder tests**

Create `src/__init__.py`:

```python
"""Manim demo source package."""
```

Create `tests/test_demo_scene.py`:

```python
from pathlib import Path

import manimpango
from manim import SVGMobject, Text, register_font


ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = Path(r"C:\Users\15694\Downloads\HYTianZhenTi.ttf")
FONT_FAMILY = "HYTianZhenTi"


def test_supplied_font_registers_with_expected_family() -> None:
    assert FONT_PATH.is_file()
    with register_font(FONT_PATH):
        assert FONT_FAMILY in manimpango.list_fonts()


def test_scene_builders_create_vector_character_and_caption() -> None:
    from src.xkcd_manim_demo import CAPTION, build_caption, build_character

    character = build_character()
    caption = build_caption()

    assert isinstance(character, SVGMobject)
    assert len(character.submobjects) >= 6
    assert isinstance(caption, Text)
    assert caption.text == CAPTION
    assert character.height > caption.height
```

- [ ] **Step 2: Run the scene tests and verify the missing module failure**

Run:

```powershell
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_demo_scene.py -v
```

Expected: the font test passes and the builder test fails with `ModuleNotFoundError: No module named 'src.xkcd_manim_demo'`.

- [ ] **Step 3: Implement the focused Manim scene**

Create `src/xkcd_manim_demo.py`:

```python
from pathlib import Path

from manim import (
    BLACK,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    CubicBezier,
    Scene,
    SVGMobject,
    Text,
    register_font,
)


ROOT = Path(__file__).resolve().parents[1]
ASSET_PATH = ROOT / "assets" / "xkcd_cueball_study.svg"
FONT_PATH = Path(r"C:\Users\15694\Downloads\HYTianZhenTi.ttf")
FONT_FAMILY = "HYTianZhenTi"
CAPTION = "所以……动量真的没丢？"


def build_character() -> SVGMobject:
    character = SVGMobject(ASSET_PATH, height=4.7)
    return character


def build_caption() -> Text:
    with register_font(FONT_PATH):
        caption = Text(
            CAPTION,
            font=FONT_FAMILY,
            font_size=72,
            color=BLACK,
            disable_ligatures=True,
        )
    return caption


class XKCDManimStill(Scene):
    def construct(self) -> None:
        self.camera.background_color = WHITE

        character = build_character().move_to(3.9 * RIGHT + 1.25 * DOWN)
        caption = build_caption().move_to(1.55 * LEFT + 2.35 * UP)

        leader = CubicBezier(
            caption.get_bottom() + 1.9 * RIGHT + 0.08 * DOWN,
            caption.get_bottom() + 2.0 * RIGHT + 0.45 * DOWN,
            character.get_top() + 0.75 * LEFT + 0.35 * UP,
            character.get_top() + 0.35 * LEFT + 0.04 * UP,
        ).set_stroke(BLACK, width=6)

        self.add(caption, leader, character)
```

- [ ] **Step 4: Run the scene tests**

Run:

```powershell
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_demo_scene.py -v
```

Expected: `2 passed`.

- [ ] **Step 5: Commit the tested scene**

```powershell
git add -- src/__init__.py src/xkcd_manim_demo.py tests/test_demo_scene.py
git commit -m "feat: compose xkcd-style Manim still"
```

### Task 3: Render and Validate the 1080p Deliverable

**Files:**
- Create: `tests/test_render_output.py`
- Create: `outputs/xkcd_manim_demo.png`
- Modify if visual QA requires it: `assets/xkcd_cueball_study.svg`
- Modify if visual QA requires it: `src/xkcd_manim_demo.py`

- [ ] **Step 1: Write the failing output test**

Create `tests/test_render_output.py`:

```python
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "outputs" / "xkcd_manim_demo.png"


def test_rendered_demo_is_full_hd_and_contains_ink() -> None:
    assert OUTPUT_PATH.is_file(), f"Missing rendered demo: {OUTPUT_PATH}"
    with Image.open(OUTPUT_PATH) as image:
        rgb = image.convert("RGB")
        assert rgb.size == (1920, 1080)
        dark_pixels = sum(
            1 for red, green, blue in rgb.getdata() if max(red, green, blue) < 96
        )
    assert dark_pixels > 3_000
```

- [ ] **Step 2: Run the output test and verify it fails**

Run:

```powershell
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_render_output.py -v
```

Expected: failure with `Missing rendered demo`.

- [ ] **Step 3: Render the scene to Manim's image output**

Run:

```powershell
manim render -qh -s --media_dir outputs -o xkcd_manim_demo.png src/xkcd_manim_demo.py XKCDManimStill
```

Expected: Manim reports a successful still render.

- [ ] **Step 4: Normalize the rendered file to the deliverable path**

Run:

```powershell
$target = (Resolve-Path "outputs").Path + "\xkcd_manim_demo.png"
if (-not (Test-Path -LiteralPath $target)) {
    $rendered = Get-ChildItem -LiteralPath "outputs" -Recurse -Filter "xkcd_manim_demo.png" |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if (-not $rendered) { throw "Manim render not found under outputs" }
    Copy-Item -LiteralPath $rendered.FullName -Destination $target -Force
}
```

Expected: `outputs/xkcd_manim_demo.png` exists.

- [ ] **Step 5: Run all automated checks**

Run:

```powershell
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest -v
```

Expected: `6 passed`.

- [ ] **Step 6: Perform original-resolution visual QA**

Open `outputs/xkcd_manim_demo.png` at original resolution and confirm all of the following:

- The head occupies roughly one quarter of the character height and is visibly asymmetric rather than a perfect circle.
- The body parts are curved open strokes with round endpoints; they do not read as a geometric `Circle + Line` construction.
- The character is fully inside the frame in the lower-right area.
- The caption uses HYTianZhenTi, is not enclosed by a bubble, and has one open curved leader.
- The background is pure white and there is no raster reference image in the deliverable.

If the head/body ratio fails, edit only the SVG head path or limb endpoints. If placement fails, edit only the two `move_to(...)` calls. If the leader collides with text or the head, edit only its four Bézier control points. Re-render and repeat Steps 4–6 until every item passes.

- [ ] **Step 7: Commit the verified deliverable**

```powershell
git add -- assets/xkcd_cueball_study.svg src/xkcd_manim_demo.py tests/test_render_output.py outputs/xkcd_manim_demo.png
git commit -m "test: verify xkcd Manim demo render"
```

### Task 4: Final Verification and Handoff

**Files:**
- Verify: `outputs/xkcd_manim_demo.png`
- Verify: `docs/superpowers/specs/2026-07-11-xkcd-manim-demo-design.md`

- [ ] **Step 1: Confirm repository state and test evidence**

Run:

```powershell
git status --short
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest -q
Get-Item -LiteralPath "outputs\xkcd_manim_demo.png" | Select-Object FullName, Length, LastWriteTime
```

Expected: no uncommitted files from this implementation, `6 passed`, and a non-empty PNG at the deliverable path. Pre-existing `.superpowers/` files may remain untracked and must not be added.

- [ ] **Step 2: Present the final PNG for user review**

Return a clickable link and inline preview for `outputs/xkcd_manim_demo.png`. State that the character remains a static vector group and that rigid whole-character entrance/exit motion is the accepted next fallback; do not claim limb animation has been validated.
