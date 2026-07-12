# Cueball Standing Asset Implementation Plan

> **Status:** Completed. The code snippets and intermediate pass counts below document the initial implementation and must not be replayed as the current asset recipe. The calibrated source of truth is `docs/superpowers/specs/2026-07-12-cueball-standing-asset-design.md`: SVG stroke width 17, Manim height 6.78, seven standing-asset tests, and final 512 × 1024 PNG pixel checks.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable straight-arm standing Cueball SVG calibrated against the supplied reference and a transparent vertical PNG preview.

**Architecture:** Keep the pose independent from the existing dialogue asset. Define all six body parts as named SVG groups, load that SVG in a dedicated Manim scene, and render a transparent 512×1024 preview without text or props.

**Tech Stack:** SVG, Python 3.12, Manim Community 0.20.1, pytest, Pillow

---

## File Map

- `assets/xkcd_cueball_standing.svg`: reusable standing pose with named vector parts.
- `src/xkcd_standing_asset.py`: dedicated transparent-preview Manim scene.
- `tests/test_standing_asset.py`: SVG geometry and PNG transparency checks.
- `outputs/xkcd_cueball_standing.png`: user-facing transparent preview.

### Task 1: Add the Straight-Arm SVG Pose

**Files:**
- Create: `tests/test_standing_asset.py`
- Create: `assets/xkcd_cueball_standing.svg`

- [ ] **Step 1: Write the failing SVG tests**

Create `tests/test_standing_asset.py`:

```python
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image
from svgelements import Path as SVGPath


ROOT = Path(__file__).resolve().parents[1]
SVG_PATH = ROOT / "assets" / "xkcd_cueball_standing.svg"
PNG_PATH = ROOT / "outputs" / "xkcd_cueball_standing.png"
EXPECTED_IDS = {
    "head",
    "torso",
    "left-arm",
    "right-arm",
    "left-leg",
    "right-leg",
}


def _root() -> ET.Element:
    return ET.parse(SVG_PATH).getroot()


def _group_path(group_id: str) -> tuple[ET.Element, SVGPath]:
    group = next(element for element in _root().iter() if element.attrib.get("id") == group_id)
    path_element = next(element for element in group if element.tag.endswith("path"))
    return path_element, SVGPath(path_element.attrib["d"])


def test_standing_svg_exists_with_named_vector_parts() -> None:
    assert SVG_PATH.is_file()
    root = _root()
    ids = {element.attrib["id"] for element in root.iter() if "id" in element.attrib}
    assert EXPECTED_IDS <= ids
    assert all(not element.tag.endswith("image") for element in root.iter())


def test_standing_svg_uses_line_width_twelve() -> None:
    style_group = next(element for element in _root() if element.tag.endswith("g"))
    assert float(style_group.attrib["stroke-width"]) == 12


def test_standing_arms_are_straight_and_share_the_head_base_joint() -> None:
    left_element, left_path = _group_path("left-arm")
    right_element, right_path = _group_path("right-arm")
    assert "L" in left_element.attrib["d"] and "C" not in left_element.attrib["d"]
    assert "L" in right_element.attrib["d"] and "C" not in right_element.attrib["d"]
    assert left_path.first_point == right_path.first_point
    _, head_path = _group_path("head")
    assert abs(left_path.first_point.y - head_path.bbox()[3]) <= 4


def test_standing_png_is_vertical_and_transparent() -> None:
    assert PNG_PATH.is_file()
    with Image.open(PNG_PATH) as image:
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        assert rgba.size == (512, 1024)
        assert alpha.getextrema() == (0, 255)
        assert alpha.getpixel((0, 0)) == 0
```

- [ ] **Step 2: Run the SVG tests and verify the asset is missing**

Run:

```powershell
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_standing_asset.py -v
```

Expected: the three SVG tests fail because `assets/xkcd_cueball_standing.svg` is missing; the PNG test also fails because the preview is not rendered yet.

- [ ] **Step 3: Create the standing SVG**

Create `assets/xkcd_cueball_standing.svg`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 420">
  <g fill="none" stroke="#111111" stroke-width="12"
     stroke-linecap="round" stroke-linejoin="round">
    <g id="torso">
      <path d="M130 133 C128 158 131 188 132 214"/>
    </g>
    <g id="left-arm">
      <path d="M130 133 L88 218"/>
    </g>
    <g id="right-arm">
      <path d="M130 133 L169 218"/>
    </g>
    <g id="left-leg">
      <path d="M132 214 C122 246 112 292 102 344"/>
    </g>
    <g id="right-leg">
      <path d="M132 214 C143 246 157 294 171 343"/>
    </g>
    <g id="head" fill="#ffffff">
      <path d="M130 20 C104 18 86 35 83 66 C80 97 97 123 123 131 C150 136 171 116 176 84 C181 53 169 27 147 21 C141 19 135 19 130 20 Z"/>
    </g>
  </g>
</svg>
```

- [ ] **Step 4: Run only the SVG tests**

Run:

```powershell
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_standing_asset.py -v -k "not png"
```

Expected: `3 passed, 1 deselected`.

- [ ] **Step 5: Commit the vector asset**

```powershell
git add -- assets/xkcd_cueball_standing.svg tests/test_standing_asset.py
git commit -m "feat: add straight-arm Cueball pose"
```

### Task 2: Render the Transparent PNG Preview

**Files:**
- Create: `src/xkcd_standing_asset.py`
- Create: `outputs/xkcd_cueball_standing.png`

- [ ] **Step 1: Create the dedicated Manim preview scene**

Create `src/xkcd_standing_asset.py`:

```python
from pathlib import Path

from manim import ORIGIN, Scene, SVGMobject, config


ROOT = Path(__file__).resolve().parents[1]
ASSET_PATH = ROOT / "assets" / "xkcd_cueball_standing.svg"

config.frame_width = 4
config.frame_height = 8


class XKCDStandingAssetPreview(Scene):
    def construct(self) -> None:
        character = SVGMobject(ASSET_PATH, height=6.8).move_to(ORIGIN)
        self.add(character)
```

- [ ] **Step 2: Render the transparent vertical PNG**

Run:

```powershell
manim render -s --transparent -r 512,1024 --media_dir outputs -o xkcd_cueball_standing.png src/xkcd_standing_asset.py XKCDStandingAssetPreview
$rendered = Get-ChildItem -LiteralPath "outputs\images" -Recurse -Filter "xkcd_cueball_standing.png" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
if (-not $rendered) { throw "Standing asset preview not found" }
Copy-Item -LiteralPath $rendered.FullName -Destination "outputs\xkcd_cueball_standing.png" -Force
```

Expected: Manim renders one PNG and the normalized output path exists.

- [ ] **Step 3: Run all standing-asset tests**

Run:

```powershell
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_standing_asset.py -v
```

Expected: `4 passed`.

- [ ] **Step 4: Inspect the PNG at original resolution**

Confirm the figure is centered, fully visible, transparent around the character, and both arm paths are straight downward strokes without curvature. If alignment fails, edit only the two arm endpoints in `assets/xkcd_cueball_standing.svg`; if padding fails, edit only the `height=6.8` value in `src/xkcd_standing_asset.py`, then re-render and rerun the tests.

- [ ] **Step 5: Commit the verified preview**

```powershell
git add -- src/xkcd_standing_asset.py outputs/xkcd_cueball_standing.png
git commit -m "feat: render transparent standing Cueball preview"
```

### Task 3: Final Verification and PR Update

**Files:**
- Verify: `assets/xkcd_cueball_standing.svg`
- Verify: `outputs/xkcd_cueball_standing.png`

- [ ] **Step 1: Run the full test suite and verify repository state**

Run:

```powershell
& "C:\Users\15694\AppData\Local\Programs\Python\Python312\python.exe" -m pytest -q
git diff --check
git status --short
```

Expected: all tests pass, `git diff --check` reports nothing, and the worktree has no uncommitted implementation files.

- [ ] **Step 2: Push the existing PR branch**

```powershell
git push
```

Expected: `feature/xkcd-manim-demo` updates PR #1.

- [ ] **Step 3: Copy the verified preview to the main workspace output directory**

```powershell
$source = "C:\Users\15694\Documents\Codex\2026-07-11\https-www-manim-community\.worktrees\xkcd-manim-demo\outputs\xkcd_cueball_standing.png"
$target = "C:\Users\15694\Documents\Codex\2026-07-11\https-www-manim-community\outputs\xkcd_cueball_standing.png"
Copy-Item -LiteralPath $source -Destination $target -Force
if ((Get-FileHash -LiteralPath $source).Hash -ne (Get-FileHash -LiteralPath $target).Hash) {
    throw "Standing asset copy hash mismatch"
}
```

Expected: both files have identical hashes.
