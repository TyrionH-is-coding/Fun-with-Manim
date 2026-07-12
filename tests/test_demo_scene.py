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
