# XKCD-Style Manim Still Demo Design

## Objective

Produce one 1920×1080 still image rendered by Manim Community v0.20.1 to prove that an xkcd-like character can be represented accurately without assembling a generic stick figure from circles and straight lines.

This is a private feasibility study. It is not the final original protagonist and is not intended to be published as a finished channel asset.

## Reference

- Pose and limb-overlap reference supplied by the user: `C:/Users/15694/AppData/Local/Temp/codex-clipboard-9569bc04-7de8-4471-aefd-110861323653.png`
- Overall composition, typography, and line-weight reference supplied by the user: `C:/Users/15694/AppData/Local/Temp/codex-clipboard-02e08f74-0c0b-4533-9770-1f423a900474.png`
- Font supplied by the user: `C:/Users/15694/Downloads/HYTianZhenTi.ttf`

## Composition

- Canvas: 1920×1080, pure white background.
- Character: a bald Cueball-style study placed in the lower-right area, large enough for line quality to be judged.
- Text: `所以……动量真的没丢？`, placed above the character without an enclosing speech bubble.
- Speaker indication: one short, open curved leader line may connect the text area to the character; it must not form a bubble.
- Text font: the internal family name read from `HYTianZhenTi.ttf`, not a guessed filename-derived name.

## Character Construction

- Rebuild the supplied pose as named open vector paths: head, torso, left arm, right arm, left leg, and right leg.
- Preserve the references' defining geometry: irregular large head, point-like neck/shoulder junction, asymmetric limbs, curved endpoints, and deliberate overlaps. The narrow triangular wedge in the first pose should arise from overlapping independent strokes rather than a filled body shape.
- Use approximately uniform black strokes with round caps and joins, visually equivalent to 5–7 px at 1080p. Do not add an artificial roughness filter; the hand-drawn effect comes from controlled Bézier geometry, not frame-by-frame noise.
- Give the head an opaque white fill so body strokes terminate cleanly behind it.
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

## Accepted Future Animation Fallback

If articulated character motion does not preserve the drawing style, the character may remain a static vector group and only translate, enter, pause, or exit as a whole. Limb rigging is not required for the first production workflow.
