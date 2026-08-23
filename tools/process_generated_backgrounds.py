"""Convert project-owned generated scene art into runtime WebP backgrounds."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
TARGET = ROOT / "第七个测试剧本" / "Assets" / "Backgrounds"
SIZE = (1672, 941)


def fit(source: Path) -> Image.Image:
    image = Image.open(source).convert("RGB")
    if image.size != SIZE:
        image = image.resize(SIZE, Image.Resampling.LANCZOS)
    return image


def save(image: Image.Image, name: str) -> None:
    destination = TARGET / name
    image.save(destination, "WEBP", quality=91, method=6)
    print(f"{name}: {image.size}")


def main() -> None:
    save(fit(GENERATED / "a3-impossible-classroom.png"), "无星教室.webp")
    save(fit(GENERATED / "a2-night-classroom.png"), "夜班教室.webp")

    terminal = fit(GENERATED / "terminal-main-classroom.png")
    save(terminal, "终末教室.webp")
    # A deliberate camera push-in toward the recognizable ghost at the board.
    crop = terminal.crop((205, 75, 1467, 815)).resize(SIZE, Image.Resampling.LANCZOS)
    save(crop, "终末教室-zoom.webp")


if __name__ == "__main__":
    main()
