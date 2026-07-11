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
