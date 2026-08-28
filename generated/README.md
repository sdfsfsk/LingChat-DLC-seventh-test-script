# Generated source images

These PNG files are AI-generated **source intermediates** for v2.1, retained so the shipped WebP assets can be reproduced and audited. They are not copied into the DLC package.

- `ql-*.png` are expression references. `tools/process_generated_sprites.py` aligns each face to the original transparent `正常.webp` sprite, transplants only the facial region, and preserves the original body silhouette and alpha channel.
- `a2-night-classroom.png`, `a3-impossible-classroom.png`, and `terminal-main-classroom.png` are converted/cropped by `tools/process_generated_backgrounds.py` to the 1672×941 backgrounds used by the script.
- `jumpscare-half-ql.png` (v2.12) is the DDLC "yuri half" equivalent: left half normal ql, right half corrupted, split by a glitch seam. Generated via codex CLI with `Assets/Pics/jumpscare-face-ql.webp` and ql's `正常.webp` as references; shipped as `Assets/Pics/jumpscare-half-ql.webp` (quality 88).

Run both processors from the repository root after installing Pillow. Review all output visually before release.
