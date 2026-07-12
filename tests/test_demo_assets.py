from pathlib import Path
from xml.etree import ElementTree as ET

from svgelements import Path as SVGPath


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


def _group_path(root: ET.Element, group_id: str) -> SVGPath:
    group = next(element for element in root.iter() if element.attrib.get("id") == group_id)
    path_element = next(element for element in group if element.tag.endswith("path"))
    return SVGPath(path_element.attrib["d"])


def test_character_uses_bold_strokes() -> None:
    root = ET.parse(SVG_PATH).getroot()
    style_group = next(element for element in root if element.tag.endswith("g"))
    assert float(style_group.attrib["stroke-width"]) >= 10


def test_head_is_visibly_taller_than_wide() -> None:
    root = ET.parse(SVG_PATH).getroot()
    left, top, right, bottom = _group_path(root, "head").bbox()
    assert (bottom - top) / (right - left) >= 1.12


def test_arms_and_torso_share_the_head_base_joint() -> None:
    root = ET.parse(SVG_PATH).getroot()
    _, _, _, head_bottom = _group_path(root, "head").bbox()
    joint_points = [
        _group_path(root, group_id).first_point
        for group_id in ("torso", "left-arm", "right-arm")
    ]
    assert max(point.x for point in joint_points) - min(point.x for point in joint_points) <= 2
    assert all(abs(point.y - head_bottom) <= 4 for point in joint_points)


def test_leg_joint_matches_reference_vertical_proportion() -> None:
    root = ET.parse(SVG_PATH).getroot()
    _, head_top, _, head_bottom = _group_path(root, "head").bbox()
    head_height = head_bottom - head_top
    leg_points = [
        _group_path(root, group_id).first_point
        for group_id in ("left-leg", "right-leg")
    ]
    ratios = [(point.y - head_bottom) / head_height for point in leg_points]
    assert all(0.65 <= ratio <= 0.80 for ratio in ratios)
