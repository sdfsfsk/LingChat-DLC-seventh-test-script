"""Prepare the generated oil-leaking ghost sprite as a transparent runtime WebP.

The image generator baked a light checkerboard into its RGB output. The dark
closed character outline lets us remove the exterior without keying away the
white hair, skin, clothes or tail. Requires Pillow and NumPy.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "generated" / "ghost-ql-oil.png"
TARGET = ROOT / "第七个测试剧本" / "Assets" / "Pics" / "ghost-ql-bw.webp"


def main():
    image = Image.open(SOURCE).convert("RGB")
    gray = image.convert("L")
    # Close one-pixel breaks in the outline before flooding the exterior.
    barrier = gray.point(lambda value: 255 if value > 170 else 0).filter(ImageFilter.MinFilter(3))
    ImageDraw.floodfill(barrier, (0, 0), 128)
    # Empty loop within the hair curl and the gap between the crossed legs.
    for point in [(430, 127), (514, 992)]:
        if barrier.getpixel(point) == 255:
            ImageDraw.floodfill(barrier, point, 128)
    mask = Image.fromarray(np.where(np.asarray(barrier) == 128, 0, 255).astype("uint8"))
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.35))
    # The source is monochrome line art; normalize light grid residue inside
    # enclosed white regions while retaining gray antialiasing and oil highlights.
    pixels = np.array(gray)
    pixels[pixels >= 205] = 255
    sprite = Image.fromarray(pixels).convert("RGBA")
    sprite.putalpha(mask)
    sprite.save(TARGET, "WEBP", lossless=True, method=6)
    print(f"Saved {TARGET}: {sprite.size}, RGBA, transparent pixels={(np.asarray(mask)==0).sum()}")


if __name__ == "__main__":
    main()
