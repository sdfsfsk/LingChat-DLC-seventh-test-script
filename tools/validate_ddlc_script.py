#!/usr/bin/env python3
"""Validate the DDLC-style LingChat script graph, media contract, and poem pool."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

EVENT_TYPES = {
    "achievement",
    "ai_dialogue",
    "ambient",
    "background",
    "background_effect",
    "chapter_end",
    "choices",
    "dialogue",
    "force_choice",
    "free_dialogue",
    "horror_log",
    "input",
    "jumpscare",
    "modify_character",
    "music",
    "narration",
    "player",
    "poem_game",
    "present_pic",
    "random_var",
    "set_variable",
    "sound",
    "voice_shift",
    "wait",
}
MEDIA_FIELDS = {
    "imagePath",
    "musicPath",
    "glitchMusicPath",
    "soundPath",
    "ambientPath",
    "backgroundPath",
    "warmStickerPath",
    "scriptStickerPath",
    "voidStickerPath",
}
POEM_MODES = {"normal", "act2", "act2_final"}
COMPATIBILITY_CHAPTERS = {"special_poem_a2b"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("root must be a mapping")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "script_root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "第七个测试剧本",
    )
    parser.add_argument("--global-data", type=Path)
    args = parser.parse_args()

    root = args.script_root.resolve()
    chapters_dir = root / "Chapters"
    errors: list[str] = []
    warnings: list[str] = []

    try:
        config = load_yaml(root / "story_config.yaml")
        word_data = load_yaml(root / "poem_words.yaml")
    except Exception as exc:
        print(f"configuration parse failed: {exc}", file=sys.stderr)
        return 1

    chapters: dict[str, dict[str, Any]] = {}
    for path in sorted(chapters_dir.glob("*.yaml")):
        try:
            chapters[path.stem] = load_yaml(path)
        except Exception as exc:
            errors.append(f"{path.name}: YAML parse failed: {exc}")

    intro = config.get("intro_chapter")
    if intro not in chapters:
        errors.append(f"intro_chapter does not exist: {intro!r}")

    available_media = {
        path.name
        for path in (root / "Assets").rglob("*")
        if path.is_file()
    }
    if args.global_data and args.global_data.exists():
        available_media.update(
            path.name for path in args.global_data.rglob("*") if path.is_file()
        )

    references: list[tuple[str, str]] = []
    poem_events: list[tuple[str, dict[str, Any]]] = []
    for chapter_id, chapter in chapters.items():
        events = chapter.get("events")
        if not isinstance(events, list):
            errors.append(f"{chapter_id}: events must be a list")
            continue
        for index, event in enumerate(events, start=1):
            if not isinstance(event, dict):
                errors.append(f"{chapter_id} event {index}: event must be a mapping")
                continue
            event_type = event.get("type")
            if event_type not in EVENT_TYPES:
                errors.append(f"{chapter_id} event {index}: unknown type {event_type!r}")
            condition = event.get("condition")
            if isinstance(condition, str) and any(
                token in condition for token in ("&&", "||", ">=", "<=")
            ):
                errors.append(
                    f"{chapter_id} event {index}: unsupported compound condition {condition!r}"
                )
            direct_next = event.get("next_chapter")
            if isinstance(direct_next, str) and direct_next != "end":
                references.append((chapter_id, direct_next))
            options = event.get("options")
            if event_type == "chapter_end" and isinstance(options, list):
                for option in options:
                    target = option.get("next") if isinstance(option, dict) else None
                    if isinstance(target, str) and target != "end":
                        references.append((chapter_id, target))
            for field in MEDIA_FIELDS:
                value = event.get(field)
                if not isinstance(value, str) or value in {"", "none", "None"}:
                    continue
                if Path(value).name not in available_media:
                    errors.append(
                        f"{chapter_id} event {index}: missing media {field}={value!r}"
                    )
            if event_type == "poem_game":
                poem_events.append((chapter_id, event))

    for source, target in references:
        if target not in chapters:
            errors.append(f"{source}: missing chapter target {target!r}")

    words = word_data.get("words")
    if not isinstance(words, list):
        errors.append("poem_words.yaml: words must be a list")
        words = []
    texts = [entry.get("text") for entry in words if isinstance(entry, dict)]
    if len(texts) != len(set(texts)):
        errors.append("poem_words.yaml: normal words contain duplicates")
    required_words = max(
        (int(event.get("rounds", 20)) * 10 for _, event in poem_events), default=0
    )
    if len(words) < required_words:
        errors.append(
            f"poem_words.yaml: need {required_words} unique normal words, found {len(words)}"
        )

    for chapter_id, event in poem_events:
        mode = event.get("mode")
        if mode not in POEM_MODES:
            errors.append(f"{chapter_id}: poem_game has invalid mode {mode!r}")
        if not isinstance(event.get("glitch"), bool):
            errors.append(f"{chapter_id}: poem_game must set glitch explicitly")
        for field in ("warmStickerPath", "scriptStickerPath"):
            sticker = event.get(field)
            if isinstance(sticker, str) and sticker.lower().endswith(".png"):
                hop = f"{sticker[:-4]}-跳.png"
                if Path(hop).name not in available_media:
                    errors.append(f"{chapter_id}: missing derived hop sticker {hop!r}")
        void_sticker = event.get("voidStickerPath")
        if isinstance(void_sticker, str):
            broken = "写诗Q版-崩坏.png"
            if broken not in available_media:
                errors.append(f"{chapter_id}: missing broken sticker {broken!r}")

    incoming = {target for _, target in references}
    for chapter_id in sorted(chapters):
        if (
            chapter_id != intro
            and chapter_id not in incoming
            and chapter_id not in COMPATIBILITY_CHAPTERS
        ):
            warnings.append(f"unreferenced chapter: {chapter_id}")

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARN: {warning}")
        return 1

    print(
        "VALIDATION OK: "
        f"chapters={len(chapters)} refs={len(references)} "
        f"poem_words={len(words)} poem_games={len(poem_events)}"
    )
    for warning in warnings:
        print(f"WARN: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
