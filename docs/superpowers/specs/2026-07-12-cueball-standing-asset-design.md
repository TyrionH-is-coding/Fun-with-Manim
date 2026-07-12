# Cueball Standing Asset Design

## Objective

Add one reusable standing Cueball-style character asset based on the approved demo proportions and the user's latest pose reference.

## Deliverables

- `assets/xkcd_cueball_standing.svg`: reusable vector source with named body-part groups.
- `outputs/xkcd_cueball_standing.png`: transparent-background PNG preview rendered from the SVG.

## Geometry and Style

- Match the supplied 126 × 242 reference by measured proportions rather than by eye: an elongated head, a high leg joint, hands ending just below that joint, and long legs.
- Use black strokes with a calibrated SVG source width of `17`, round caps, and round joins. At the 512 × 1024 preview size, this produces a visible median width of about 22–23 pixels, corresponding to the reference's roughly 6-pixel line at 4× scale.
- Head, torso, left arm, right arm, left leg, and right leg remain separate named SVG groups.
- Both arms begin at the shared joint immediately below the head and descend as straight, independent strokes.
- Arms may be slightly asymmetric in angle, but neither arm may contain a curved Bézier segment.
- The head has an opaque white fill; all other body parts are unfilled open paths.
- The SVG contains no embedded raster image.

## Preview

- Render a 512 × 1024 vertical transparent PNG with the complete character centered and fully visible.
- Keep the rendered dark-pixel bounds close to 300 × 876 pixels and the enclosed white head area close to 256 × 288 pixels. Small antialiasing tolerances are allowed.
- Include comfortable transparent padding without adding text, a speech leader, ground, or other props.
- Keep the existing dialogue demo and its asset unchanged.

## Verification

- Automated checks confirm the six named groups, vector-only content, calibrated source line width, straight arm segments, shared head-base joint, measured body ratios, transparent PNG output, and final pixel bounds.
- Visual inspection confirms that both arms hang naturally downward and do not bow or curve.

## Non-Goals

- No articulated animation or rigging.
- No parameterized character generator.
- No additional poses, facial features, hair, clothing, or props.
