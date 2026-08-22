from __future__ import annotations

from collections import deque
from pathlib import Path
import random

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SHEET = Path(__file__).resolve().parent / "source" / "q-sprites-unified-sheet-magenta.png"
OUT_DIR = ROOT / "generated-q-sprites"

SPRITES = (
    ("写诗Q版-她.png", (0, 0)),
    ("写诗Q版-钦灵.png", (1, 0)),
    ("写诗Q版-她-跳.png", (0, 1)),
    ("写诗Q版-钦灵-跳.png", (1, 1)),
)

CANVAS_SIZE = 1024
TARGET_HEIGHT = 900
BOTTOM_MARGIN = 62


def remove_magenta(image: Image.Image) -> Image.Image:
    """Chroma-key the generated magenta sheet and suppress edge color spill."""
    rgb = np.asarray(image.convert("RGB"), dtype=np.float32)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    # The generator's background is a slightly shaded #ff00ff field.  This
    # predicate intentionally stays far away from the characters' pale pink
    # ear interiors and cyan/blue clothing.
    background = (
        (r > 100)
        & (b > 100)
        & (g < 140)
        & ((r - g) > 55)
        & ((b - g) > 55)
    )

    # A tiny feather restores antialiased silhouette edges after chroma keying.
    hard_alpha = Image.fromarray((~background).astype(np.uint8) * 255, mode="L")
    alpha = hard_alpha.filter(ImageFilter.GaussianBlur(0.5))
    alpha_array = np.asarray(alpha, dtype=np.float32) / 255.0

    # Remove magenta contamination from partially transparent edge pixels.
    key = np.array([245.0, 4.0, 237.0], dtype=np.float32)
    safe_alpha = np.maximum(alpha_array[..., None], 1.0 / 255.0)
    clean = (rgb - (1.0 - alpha_array[..., None]) * key) / safe_alpha
    clean = np.clip(clean, 0, 255).astype(np.uint8)

    rgba = np.dstack((clean, np.asarray(alpha, dtype=np.uint8)))
    rgba[np.asarray(alpha) == 0, :3] = 0
    return Image.fromarray(rgba, mode="RGBA")


def keep_largest_component(sprite: Image.Image) -> Image.Image:
    """Discard detached generation speckles while retaining antialiased edges."""
    alpha = np.asarray(sprite.getchannel("A"))
    mask = alpha > 24
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    largest: list[tuple[int, int]] = []

    for y, x in zip(*np.nonzero(mask & ~visited)):
        if visited[y, x]:
            continue
        queue = deque([(int(y), int(x))])
        visited[y, x] = True
        component: list[tuple[int, int]] = []
        while queue:
            cy, cx = queue.popleft()
            component.append((cy, cx))
            for ny in range(max(0, cy - 1), min(height, cy + 2)):
                for nx in range(max(0, cx - 1), min(width, cx + 2)):
                    if mask[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        queue.append((ny, nx))
        if len(component) > len(largest):
            largest = component

    keep = np.zeros_like(mask, dtype=np.uint8)
    for y, x in largest:
        keep[y, x] = 255
    keep = np.asarray(
        Image.fromarray(keep, mode="L").filter(ImageFilter.MaxFilter(5)),
        dtype=np.uint8,
    )

    rgba = np.asarray(sprite).copy()
    rgba[keep == 0] = 0
    return Image.fromarray(rgba, mode="RGBA")


def normalize_sprite(sprite: Image.Image) -> Image.Image:
    sprite = keep_largest_component(sprite)
    alpha = np.asarray(sprite.getchannel("A"))
    ys, xs = np.nonzero(alpha > 24)
    if not len(xs):
        raise RuntimeError("Sprite quadrant contains no visible pixels")

    padding = 4
    left = max(0, int(xs.min()) - padding)
    top = max(0, int(ys.min()) - padding)
    right = min(sprite.width, int(xs.max()) + padding + 1)
    bottom = min(sprite.height, int(ys.max()) + padding + 1)
    sprite = sprite.crop((left, top, right, bottom))

    scale = min(TARGET_HEIGHT / sprite.height, (CANVAS_SIZE - 80) / sprite.width)
    size = (max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale)))
    sprite = sprite.resize(size, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
    x = (CANVAS_SIZE - sprite.width) // 2
    y = CANVAS_SIZE - BOTTOM_MARGIN - sprite.height
    canvas.alpha_composite(sprite, (x, y))
    return canvas


def create_glitch_sprite(normal: Image.Image) -> Image.Image:
    """Build a deterministic DDLC-style corruption from the matching base art."""
    rng = random.Random(707)
    dark = ImageEnhance.Color(normal).enhance(0.68)
    dark = ImageEnhance.Brightness(dark).enhance(0.72)

    # Hollow eyes and short ink tears keep the horror cue readable at UI scale.
    eye_layer = Image.new("RGBA", normal.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(eye_layer)
    for box in ((447, 296, 522, 390), (559, 296, 634, 390)):
        draw.ellipse(box, fill=(2, 1, 12, 250), outline=(35, 3, 48, 255), width=5)
        cx = (box[0] + box[2]) // 2
        draw.line((cx - 11, box[3] - 4, cx - 15, box[3] + 35), fill=(3, 1, 12, 210), width=7)
    eye_layer = eye_layer.filter(ImageFilter.GaussianBlur(1.1))
    dark.alpha_composite(eye_layer)

    # Horizontal displaced slices mimic DDLC's tear/static language.
    torn = dark.copy()
    for _ in range(34):
        y = rng.randrange(75, 940)
        height = rng.randrange(3, 15)
        shift = rng.choice((-1, 1)) * rng.randrange(8, 48)
        strip = dark.crop((0, y, CANVAS_SIZE, min(CANVAS_SIZE, y + height)))
        torn.alpha_composite(strip, (shift, y))

    # Digital blocks are clipped mostly around the silhouette but may protrude,
    # as intentional corruption fragments rather than accidental background.
    glitch = Image.new("RGBA", normal.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glitch)
    palette = ((0, 220, 255, 155), (233, 0, 255, 150), (20, 10, 45, 210))
    for _ in range(76):
        x = rng.randrange(205, 810)
        y = rng.randrange(90, 910)
        width = rng.randrange(8, 70)
        height = rng.randrange(2, 10)
        gdraw.rectangle((x, y, x + width, y + height), fill=rng.choice(palette))
    torn.alpha_composite(glitch)
    return torn


def main() -> None:
    sheet = remove_magenta(Image.open(SHEET))
    half_w, half_h = sheet.width // 2, sheet.height // 2
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, Image.Image] = {}
    for filename, (column, row) in SPRITES:
        box = (
            column * half_w,
            row * half_h,
            sheet.width if column else half_w,
            sheet.height if row else half_h,
        )
        output = normalize_sprite(sheet.crop(box))
        outputs[filename] = output
        output.save(OUT_DIR / filename, optimize=True)
        print(OUT_DIR / filename)

    glitch = create_glitch_sprite(outputs["写诗Q版-她.png"])
    glitch_path = OUT_DIR / "写诗Q版-崩坏.png"
    glitch.save(glitch_path, optimize=True)
    print(glitch_path)


if __name__ == "__main__":
    main()
