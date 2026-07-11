# XKCD-Style Manim Still Demo Design

## Objective

Produce one 1920×1080 still image rendered by Manim Community v0.20.1 to prove that an xkcd-like character can be represented accurately without assembling a generic stick figure from circles and straight lines.

This is a private feasibility study. It is not the final original protagonist and is not intended to be published as a finished channel asset.

## Reference

- Pose reference supplied by the user: `C:/Users/15694/AppData/Local/Temp/codex-clipboard-9569bc04-7de8-4471-aefd-110861323653.png`
- Font supplied by the user: `C:/Users/15694/Downloads/HYTianZhenTi.ttf`

## Composition

- Canvas: 1920×1080, warm white background.
- Character: placed slightly left of center, large enough for line quality to be judged.
- Text: `所以……动量真的没丢？`, placed above and to the right without a speech bubble.
- Text font: the internal family name read from `HYTianZhenTi.ttf`, not a guessed filename-derived name.

## Character Construction

- Rebuild the supplied pose as named vector paths: head, torso, left arm, right arm, left leg, and right leg.
- Preserve the reference's defining geometry: irregular large head, point-like neck/shoulder junction, narrow triangular torso, asymmetric limbs, curved endpoints, and deliberate overlaps.
- Use black strokes with no artificial roughness filter. The hand-drawn effect comes from controlled Bézier geometry, not frame-by-frame noise.
- Import the paths into Manim as SVG/VMobject content. The final image must not contain the raster reference.

## Deliverables

- Manim source scene.
- Reusable SVG character asset with named parts.
- Final 1920×1080 PNG in `outputs/`.

The licensed font file itself will remain outside the project and will not be copied into the deliverables.

## Verification

- Confirm Manim can load the supplied font using its actual internal family name.
- Render the scene successfully at 1920×1080.
- Inspect the output at original resolution for line smoothness, proportions, overlaps, and font fallback.
- Compare the rendered silhouette against the supplied reference; reject the result if it reads as a generic geometric stick figure.

## Non-Goals

- No motion or rigging in this first demo.
- No collision animation, formulas, or physics explanation.
- No final original character design.
- No HTML recording or mixed rendering pipeline.
