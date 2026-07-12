from pathlib import Path

from manim import ORIGIN, Scene, SVGMobject, config


ROOT = Path(__file__).resolve().parents[1]
ASSET_PATH = ROOT / "assets" / "xkcd_cueball_standing.svg"

config.frame_width = 4
config.frame_height = 8


class XKCDStandingAssetPreview(Scene):
    def construct(self) -> None:
        character = SVGMobject(ASSET_PATH, height=6.78).move_to(ORIGIN)
        self.add(character)
