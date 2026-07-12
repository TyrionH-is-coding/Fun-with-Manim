from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "outputs" / "xkcd_manim_demo.png"


def test_rendered_demo_is_full_hd_and_contains_ink() -> None:
    assert OUTPUT_PATH.is_file(), f"Missing rendered demo: {OUTPUT_PATH}"
    with Image.open(OUTPUT_PATH) as image:
        rgb = image.convert("RGB")
        assert rgb.size == (1920, 1080)
        dark_pixels = sum(
            1
            for red, green, blue in rgb.get_flattened_data()
            if max(red, green, blue) < 96
        )
    assert dark_pixels > 3_000
