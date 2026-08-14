from __future__ import annotations

from pathlib import Path
from textwrap import wrap

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
LVLOSS_DIR = ROOT / "data" / "external" / "lvit_official_lvloss"
OUT_DIR = ROOT / "manuscript" / "figures"
CSV_OUT = OUT_DIR / "lvit_lvloss_prior_pairs.csv"


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "arial.ttf",
        "Arial.ttf",
        "DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/ARIAL.TTF",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def build_page(
    records: list[dict[str, str]],
    start_index: int,
    end_index: int,
    out_path: Path,
) -> None:
    page_records = records[start_index:end_index]
    cols = 2
    rows = len(page_records)
    margin_x = 40
    margin_y = 36
    cell_w = 840
    cell_h = 460
    gutter_x = 28
    gutter_y = 24
    page_w = cols * cell_w + (cols - 1) * gutter_x + 2 * margin_x
    page_h = rows * cell_h + (rows - 1) * gutter_y + 2 * margin_y

    canvas = Image.new("RGB", (page_w, page_h), "white")
    draw = ImageDraw.Draw(canvas)
    title_font = load_font(28)
    body_font = load_font(22)
    small_font = load_font(20)

    for idx, record in enumerate(page_records):
        row = idx // cols
        col = idx % cols
        x0 = margin_x + col * (cell_w + gutter_x)
        y0 = margin_y + row * (cell_h + gutter_y)
        x1 = x0 + cell_w
        y1 = y0 + cell_h

        draw.rounded_rectangle((x0, y0, x1, y1), radius=18, outline="#1f4e79", width=3, fill="white")

        img = Image.open(LVLOSS_DIR / record["Image"]).convert("RGB").resize((300, 300), Image.NEAREST)
        canvas.paste(img, (x0 + 26, y0 + 72))

        draw.text((x0 + 26, y0 + 22), f"Mẫu {start_index + idx + 1}: {record['Image']}", font=title_font, fill="#0b2e59")
        draw.text((x0 + 360, y0 + 74), "Text annotation:", font=body_font, fill="#0f766e")

        wrapped = wrap(record["Description"], width=34)
        current_y = y0 + 114
        for line in wrapped:
            draw.text((x0 + 360, current_y), line, font=body_font, fill="#111827")
            current_y += 34

        draw.text(
            (x0 + 360, y1 - 64),
            "Nguồn: thư mục LV_loss chính thức của repo LViT.",
            font=small_font,
            fill="#374151",
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, quality=95)


def main() -> None:
    df = pd.read_excel(LVLOSS_DIR / "LV_loss.xlsx")
    df.to_csv(CSV_OUT, index=False, encoding="utf-8-sig")
    records = df.to_dict(orient="records")
    build_page(records, 0, 8, OUT_DIR / "lvit_lvloss_prior_gallery_page1.png")
    build_page(records, 8, 14, OUT_DIR / "lvit_lvloss_prior_gallery_page2.png")


if __name__ == "__main__":
    main()
