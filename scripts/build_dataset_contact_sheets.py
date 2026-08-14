"""Build 4x7 image-text contact sheets for the LViT report.

The default layout is compatible with common LViT splits:

    Train_Folder/
      img/
      labelcol/
      Train_text.xlsx
"""

from __future__ import annotations

import argparse
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")
IMAGE_COLUMNS = ("Image", "image", "Filename", "filename", "file", "name", "img")
TEXT_COLUMNS = ("Description", "description", "Text", "text", "caption", "sentence")


def read_table(path: Path):
    try:
        import pandas as pd
    except ImportError as exc:
        raise SystemExit("Missing dependency: install pandas and openpyxl to read text tables.") from exc

    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".tsv", ".txt"}:
        return pd.read_csv(path, sep="\t")
    raise SystemExit(f"Unsupported table type: {path}")


def pick_column(columns, candidates, fallback_index):
    for name in candidates:
        if name in columns:
            return name
    if len(columns) > fallback_index:
        return columns[fallback_index]
    raise SystemExit(f"Cannot infer a usable column from: {list(columns)}")


def find_image(image_dir: Path, name: str) -> Path | None:
    raw = Path(str(name).strip())
    candidates = []
    if raw.suffix:
        candidates.append(image_dir / raw.name)
    else:
        candidates.extend(image_dir / f"{raw.name}{suffix}" for suffix in IMAGE_SUFFIXES)

    for candidate in candidates:
        if candidate.exists():
            return candidate

    stem = raw.stem or raw.name
    matches = list(image_dir.rglob(f"{stem}.*"))
    return matches[0] if matches else None


def find_mask(mask_dir: Path | None, image_path: Path) -> Path | None:
    if not mask_dir or not mask_dir.exists():
        return None
    for suffix in IMAGE_SUFFIXES:
        candidate = mask_dir / f"{image_path.stem}{suffix}"
        if candidate.exists():
            return candidate
    matches = list(mask_dir.rglob(f"{image_path.stem}.*"))
    return matches[0] if matches else None


def load_font(size: int):
    for candidate in (
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def render_tile(image_path: Path, mask_path: Path | None, text: str, size: tuple[int, int]) -> Image.Image:
    tile_w, tile_h = size
    pad = 14
    text_h = 92
    image_h = tile_h - text_h - pad * 3

    tile = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(tile)

    image = Image.open(image_path).convert("RGB")
    image.thumbnail((tile_w - 2 * pad, image_h), Image.Resampling.LANCZOS)
    image_box = Image.new("RGB", (tile_w - 2 * pad, image_h), (245, 247, 250))
    image_x = (image_box.width - image.width) // 2
    image_y = (image_box.height - image.height) // 2
    image_box.paste(image, (image_x, image_y))

    if mask_path:
        mask = Image.open(mask_path).convert("L")
        mask.thumbnail((image.width, image.height), Image.Resampling.NEAREST)
        overlay = Image.new("RGBA", image.size, (20, 140, 110, 0))
        mask_alpha = mask.point(lambda p: 90 if p > 10 else 0)
        overlay.putalpha(mask_alpha)
        framed = image.convert("RGBA")
        framed.alpha_composite(overlay)
        image_box.paste(framed.convert("RGB"), (image_x, image_y))

    tile.paste(image_box, (pad, pad))
    draw.rounded_rectangle((pad, pad, tile_w - pad, pad + image_h), radius=8, outline=(40, 83, 140), width=2)

    font = load_font(18)
    y = pad * 2 + image_h
    for line in textwrap.wrap(str(text).replace("\n", " "), width=28)[:4]:
        draw.text((pad, y), line, fill=(20, 35, 55), font=font)
        y += 22

    draw.rounded_rectangle((1, 1, tile_w - 2, tile_h - 2), radius=10, outline=(205, 216, 230), width=2)
    return tile


def default_text_file(split_root: Path) -> Path:
    for name in ("Train_text.xlsx", "Val_text.xlsx", "Test_text.xlsx", "train_text.xlsx", "val_text.xlsx"):
        candidate = split_root / name
        if candidate.exists():
            return candidate
    matches = list(split_root.glob("*text*.xlsx")) + list(split_root.glob("*text*.csv"))
    if matches:
        return matches[0]
    raise SystemExit(f"Cannot find a text table under {split_root}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--split", default="", help="Optional split folder, for example Train_Folder.")
    parser.add_argument(
        "--all-splits",
        action="store_true",
        help="Collect Train_Folder, Val_Folder, and Test_Folder under dataset-root.",
    )
    parser.add_argument("--image-dir", type=Path)
    parser.add_argument("--mask-dir", type=Path)
    parser.add_argument("--text-file", type=Path)
    parser.add_argument("--rows", type=int, default=4)
    parser.add_argument("--cols", type=int, default=7)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    records = []
    if args.all_splits:
        split_roots = [args.dataset_root / name for name in ("Train_Folder", "Val_Folder", "Test_Folder")]
        split_roots = [path for path in split_roots if path.exists()]
        if not split_roots:
            raise SystemExit(f"No Train_Folder/Val_Folder/Test_Folder found under {args.dataset_root}")
    else:
        split_roots = [args.dataset_root / args.split if args.split else args.dataset_root]

    for split_root in split_roots:
        image_dir = args.image_dir or split_root / "img"
        mask_dir = args.mask_dir or split_root / "labelcol"
        text_file = args.text_file or default_text_file(split_root)

        table = read_table(text_file).dropna(how="all")
        image_col = pick_column(table.columns, IMAGE_COLUMNS, 0)
        text_col = pick_column(table.columns, TEXT_COLUMNS, 1)

        for _, row in table.iterrows():
            image_path = find_image(image_dir, row[image_col])
            if image_path:
                records.append((image_path, find_mask(mask_dir, image_path), row[text_col]))

    if not records:
        raise SystemExit(f"No matching images found in {image_dir}")

    random.Random(args.seed).shuffle(records)
    records = records[: args.rows * args.cols]

    tile_size = (260, 300)
    gutter = 12
    sheet_w = args.cols * tile_size[0] + (args.cols + 1) * gutter
    sheet_h = args.rows * tile_size[1] + (args.rows + 1) * gutter
    sheet = Image.new("RGB", (sheet_w, sheet_h), (247, 250, 252))

    for idx, record in enumerate(records):
        row = idx // args.cols
        col = idx % args.cols
        x = gutter + col * (tile_size[0] + gutter)
        y = gutter + row * (tile_size[1] + gutter)
        sheet.paste(render_tile(*record, size=tile_size), (x, y))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(f"Saved {len(records)} examples to {args.output}")


if __name__ == "__main__":
    main()
