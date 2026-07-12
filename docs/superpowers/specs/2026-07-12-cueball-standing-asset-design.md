# Cueball Standing Asset Design

## Objective

Add one reusable standing Cueball-style character asset based on the approved demo proportions and the user's latest pose reference.

## Deliverables

- `assets/xkcd_cueball_standing.svg`: reusable vector source with named body-part groups.
- `outputs/xkcd_cueball_standing.png`: transparent-background PNG preview rendered from the SVG.

## Geometry and Style

- Reuse the current approved elongated head, high leg joint, and extended leg proportions.
- Use black strokes with `stroke-width="12"`, round caps, and round joins.
- Head, torso, left arm, right arm, left leg, and right leg remain separate named SVG groups.
- Both arms begin at the shared joint immediately below the head and descend as straight, independent strokes.
- Arms may be slightly asymmetric in angle, but neither arm may contain a curved Bézier segment.
- The head has an opaque white fill; all other body parts are unfilled open paths.
- The SVG contains no embedded raster image.

## Preview

- Render a vertical transparent PNG with the complete character centered and fully visible.
- Include comfortable transparent padding without adding text, a speech leader, ground, or other props.
- Keep the existing dialogue demo and its asset unchanged.

## Verification

- Automated checks confirm the six named groups, vector-only content, line width 12, straight arm segments, shared head-base joint, and transparent PNG output.
- Visual inspection confirms that both arms hang naturally downward and do not bow or curve.

## Non-Goals

- No articulated animation or rigging.
- No parameterized character generator.
- No additional poses, facial features, hair, clothing, or props.
