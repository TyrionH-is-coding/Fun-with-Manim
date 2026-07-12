from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image
from scipy import ndimage
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


def test_standing_svg_uses_calibrated_source_stroke_width() -> None:
    style_group = next(element for element in _root() if element.tag.endswith("g"))
    assert float(style_group.attrib["stroke-width"]) == 17


def test_standing_arms_are_straight_and_share_the_head_base_joint() -> None:
    left_element, left_path = _group_path("left-arm")
    right_element, right_path = _group_path("right-arm")
    assert "L" in left_element.attrib["d"] and "C" not in left_element.attrib["d"]
    assert "L" in right_element.attrib["d"] and "C" not in right_element.attrib["d"]
    assert left_path.first_point == right_path.first_point
    _, head_path = _group_path("head")
    assert abs(left_path.first_point.y - head_path.bbox()[3]) <= 4


def test_standing_hands_end_below_the_leg_joint() -> None:
    _, head_path = _group_path("head")
    head_height = head_path.bbox()[3] - head_path.bbox()[1]
    _, left_arm = _group_path("left-arm")
    _, right_arm = _group_path("right-arm")
    _, left_leg = _group_path("left-leg")
    leg_joint_y = left_leg.first_point.y
    hand_offsets = [
        arm_path.bbox()[3] - leg_joint_y for arm_path in (left_arm, right_arm)
    ]
    assert all(0 < offset <= 0.10 * head_height for offset in hand_offsets)


def test_standing_svg_matches_measured_reference_proportions() -> None:
    _, head = _group_path("head")
    head_left, head_top, head_right, head_bottom = head.bbox()
    head_width = head_right - head_left
    head_height = head_bottom - head_top
    _, torso = _group_path("torso")
    _, left_arm = _group_path("left-arm")
    _, right_arm = _group_path("right-arm")
    _, left_leg = _group_path("left-leg")
    _, right_leg = _group_path("right-leg")

    def segment_ratio(path: SVGPath) -> float:
        end = path[-1].end
        return abs(end - path.first_point) / head_height

    assert 1.10 <= head_height / head_width <= 1.14
    assert 0.82 <= segment_ratio(left_arm) <= 0.87
    assert 0.82 <= segment_ratio(right_arm) <= 0.87
    assert 0.70 <= segment_ratio(torso) <= 0.75
    assert 0.95 <= segment_ratio(left_leg) <= 1.04
    assert 0.95 <= segment_ratio(right_leg) <= 1.04


def test_standing_png_is_vertical_and_transparent() -> None:
    assert PNG_PATH.is_file()
    with Image.open(PNG_PATH) as image:
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        assert rgba.size == (512, 1024)
        assert alpha.getextrema() == (0, 255)
        assert alpha.getpixel((0, 0)) == 0


def test_standing_png_matches_four_x_reference_pixels() -> None:
    with Image.open(PNG_PATH) as image:
        rgba = np.array(image.convert("RGBA"))
    dark = (
        (rgba[:, :, 0] < 80)
        & (rgba[:, :, 1] < 80)
        & (rgba[:, :, 2] < 80)
        & (rgba[:, :, 3] > 0)
    )
    rows, columns = np.where(dark)
    figure_width = int(columns.max() - columns.min() + 1)
    figure_height = int(rows.max() - rows.min() + 1)
    assert 292 <= figure_width <= 308
    assert 870 <= figure_height <= 882

    distances = ndimage.distance_transform_edt(dark)
    stroke_ridge = dark & (distances == ndimage.maximum_filter(distances, size=3))
    visible_widths = 2 * distances[stroke_ridge]
    assert 22 <= float(np.median(visible_widths)) <= 25

    white = (
        (rgba[:, :, 0] > 240)
        & (rgba[:, :, 1] > 240)
        & (rgba[:, :, 2] > 240)
        & (rgba[:, :, 3] > 0)
    )
    white_rows, white_columns = np.where(white)
    assert 252 <= int(white_columns.max() - white_columns.min() + 1) <= 260
    assert 284 <= int(white_rows.max() - white_rows.min() + 1) <= 292
