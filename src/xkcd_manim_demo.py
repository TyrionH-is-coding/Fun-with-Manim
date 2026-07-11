from pathlib import Path

from manim import (
    BLACK,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    CubicBezier,
    Scene,
    SVGMobject,
    Text,
    register_font,
)


ROOT = Path(__file__).resolve().parents[1]
ASSET_PATH = ROOT / "assets" / "xkcd_cueball_study.svg"
FONT_PATH = Path(r"C:\Users\15694\Downloads\HYTianZhenTi.ttf")
FONT_FAMILY = "HYTianZhenTi"
CAPTION = "所以……动量真的没丢？"


def build_character() -> SVGMobject:
    character = SVGMobject(ASSET_PATH, height=4.7)
    return character


def build_caption() -> Text:
    with register_font(FONT_PATH):
        caption = Text(
            CAPTION,
            font=FONT_FAMILY,
            font_size=72,
            color=BLACK,
            disable_ligatures=True,
        )
    return caption


class XKCDManimStill(Scene):
    def construct(self) -> None:
        self.camera.background_color = WHITE

        character = build_character().move_to(3.9 * RIGHT + 1.25 * DOWN)
        caption = build_caption().move_to(1.55 * LEFT + 2.35 * UP)

        leader = CubicBezier(
            caption.get_bottom() + 1.9 * RIGHT + 0.08 * DOWN,
            caption.get_bottom() + 2.0 * RIGHT + 0.45 * DOWN,
            character.get_top() + 0.75 * LEFT + 0.35 * UP,
            character.get_top() + 0.35 * LEFT + 0.04 * UP,
        ).set_stroke(BLACK, width=6)

        self.add(caption, leader, character)
