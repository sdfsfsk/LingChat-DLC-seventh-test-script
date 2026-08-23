"""Turn generated checkerboard previews into transparent runtime WebP sprites.

The image generator intentionally produced new project-owned facial expressions,
but returned a baked light checkerboard instead of alpha.  This helper flood-
fills only the border-connected near-white background, preserving the white hair
behind its blue outline, pads each result to the shipped 1071x1600 canvas, and
writes lossless WebP files.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
TARGET = ROOT / "第七个测试剧本" / "characters" / "钦灵" / "avatar"
CANVAS = (1071, 1600)

FILES = {
    "ql-happy.png": "高兴.webp",
    "ql-resigned.png": "无奈.webp",
    "ql-lovestruck.png": "心动.webp",
    "ql-ashamed.png": "羞耻.webp",
    "ql-puzzled.png": "疑惑.webp",
    "ql-surprised.png": "惊讶.webp",
}


def border_background_mask(rgb: np.ndarray) -> np.ndarray:
    """Return pixels in the bright neutral region connected to the image edge."""

    height, width, _ = rgb.shape
    minimum = rgb.min(axis=2)
    maximum = rgb.max(axis=2)
    candidate = (minimum >= 218) & ((maximum - minimum) <= 26)
    visited = np.zeros((height, width), dtype=np.bool_)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        if candidate[0, x]:
            visited[0, x] = True
            queue.append((0, x))
        if candidate[height - 1, x]:
            visited[height - 1, x] = True
            queue.append((height - 1, x))
    for y in range(height):
        if candidate[y, 0]:
            visited[y, 0] = True
            queue.append((y, 0))
        if candidate[y, width - 1]:
            visited[y, width - 1] = True
            queue.append((y, width - 1))

    while queue:
        y, x = queue.popleft()
        for next_y, next_x in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if (
                0 <= next_y < height
                and 0 <= next_x < width
                and candidate[next_y, next_x]
                and not visited[next_y, next_x]
            ):
                visited[next_y, next_x] = True
                queue.append((next_y, next_x))
    return visited


def process(source: Path, target: Path) -> None:
    generated = Image.open(source).convert("RGB")
    generated_rgb = np.asarray(generated)
    generated_alpha = Image.fromarray(
        np.where(border_background_mask(generated_rgb), 0, 255).astype(np.uint8),
        mode="L",
    )
    generated_bbox = generated_alpha.getbbox()
    if generated_bbox is None:
        raise RuntimeError(f"generated sprite has no foreground: {source}")

    # Keep the production sprite's exact silhouette/body and transplant only
    # the generated facial performance.  This avoids checkerboard artifacts and
    # guarantees every emotion has the same transparent 1071x1600 geometry.
    base = Image.open(TARGET / "正常.webp").convert("RGBA")
    base_bbox = base.getchannel("A").getbbox()
    if base_bbox is None:
        raise RuntimeError("base sprite has no alpha silhouette")

    generated_subject = generated.crop(generated_bbox).resize(
        (base_bbox[2] - base_bbox[0], base_bbox[3] - base_bbox[1]),
        Image.Resampling.LANCZOS,
    )
    aligned = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    aligned.paste(generated_subject.convert("RGBA"), base_bbox[:2])

    face_mask = Image.new("L", CANVAS, 0)
    draw = ImageDraw.Draw(face_mask)
    draw.ellipse((385, 270, 690, 515), fill=255)
    face_mask = face_mask.filter(ImageFilter.GaussianBlur(18))
    result = Image.composite(aligned, base, face_mask)
    result.putalpha(base.getchannel("A"))
    # Clear hidden RGB outside alpha so WebP thumbnailers that mishandle
    # unassociated alpha cannot reveal the aligned source canvas.
    clean = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    clean.alpha_composite(result)
    result = clean

    target.parent.mkdir(parents=True, exist_ok=True)
    result.save(target, "WEBP", lossless=True, method=6)
    print(f"{source.name} -> {target.name} ({result.size}, alpha={result.getextrema()[3]})")


def main() -> None:
    for source_name, target_name in FILES.items():
        process(GENERATED / source_name, TARGET / target_name)


if __name__ == "__main__":
    main()
