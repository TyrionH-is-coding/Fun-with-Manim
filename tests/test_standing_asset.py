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
