"""EDA mask geometry for LViT-style medical segmentation datasets.

Expected dataset layout:

    DatasetRoot/
      Train_Folder/
        img/
        labelcol/
        Train_text.xlsx
      Val_Folder/
      Test_Folder/

The script is intentionally tolerant: it can analyze masks even when images or
text annotations are missing. It writes a figure, per-sample CSV, and JSON
summary that can be used in the report.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from scipy import ndimage


IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")
SPLIT_SPECS = (
    ("Train", "Train_Folder", "Train_text.xlsx"),
    ("Validation", "Val_Folder", "Val_text.xlsx"),
    ("Test", "Test_Folder", "Test_text.xlsx"),
)
NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}


@dataclass
class SampleGeometry:
    split: str
    image_name: str
    mask_name: str
    height: int
    width: int
    mask_area: int
    mask_area_ratio: float
    bbox_area_ratio: float
    centroid_x: float
    centroid_y: float
    component_count: int
    largest_component_ratio: float
    text_laterality: str
    text_area_count: float | None
    description: str


def read_table(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in {".tsv", ".txt"}:
        return pd.read_csv(path, sep="\t")
    return None


def infer_columns(df: pd.DataFrame) -> tuple[str, str]:
    image_candidates = ("Image", "image", "Filename", "filename", "file", "name", "img")
    text_candidates = ("Description", "description", "Text", "text", "caption", "sentence")
    image_col = next((col for col in image_candidates if col in df.columns), df.columns[0])
    text_col = next((col for col in text_candidates if col in df.columns), df.columns[min(1, len(df.columns) - 1)])
    return image_col, text_col


def load_text_map(split_root: Path, text_file: str) -> dict[str, str]:
    df = read_table(split_root / text_file)
    if df is None or df.empty:
        return {}
    image_col, text_col = infer_columns(df)
    mapping: dict[str, str] = {}
    for _, row in df.iterrows():
        image_name = str(row.get(image_col, "")).strip()
        if not image_name:
            continue
        mapping[image_name] = str(row.get(text_col, "")).strip()
        mapping[Path(image_name).stem] = str(row.get(text_col, "")).strip()
    return mapping


def find_by_stem(folder: Path, stem: str) -> Path | None:
    for suffix in IMAGE_SUFFIXES:
        candidate = folder / f"{stem}{suffix}"
        if candidate.exists():
            return candidate
    matches = list(folder.glob(f"{stem}.*"))
    return matches[0] if matches else None


def list_mask_records(root: Path) -> list[tuple[str, Path, Path | None, str]]:
    records: list[tuple[str, Path, Path | None, str]] = []
    for split_name, split_dir, text_file in SPLIT_SPECS:
        split_root = root / split_dir
        mask_dir = split_root / "labelcol"
        image_dir = split_root / "img"
        if not mask_dir.exists():
            continue

        text_map = load_text_map(split_root, text_file)
        for mask_path in sorted(p for p in mask_dir.rglob("*") if p.suffix.lower() in IMAGE_SUFFIXES):
            image_path = find_by_stem(image_dir, mask_path.stem) if image_dir.exists() else None
            description = text_map.get(mask_path.name, text_map.get(mask_path.stem, ""))
            records.append((split_name, mask_path, image_path, description))
    return records


def parse_laterality(text: str) -> str:
    lower = text.lower()
    if re.search(r"\bbilateral\b|\bboth lungs?\b", lower):
        return "Bilateral"
    if re.search(r"\bunilateral\b", lower):
        return "Unilateral"
    if "left" in lower and "right" in lower:
        return "Bilateral"
    if "left" in lower or "right" in lower:
        return "Unilateral"
    return "Unknown"


def parse_area_count(text: str) -> float | None:
    lower = text.lower()
    match = re.search(r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+infected areas?\b", lower)
    if match:
        return float(NUMBER_WORDS[match.group(1)])
    digit = re.search(r"\b(\d+)\s+infected areas?\b", lower)
    return float(digit.group(1)) if digit else None


def load_mask(path: Path) -> np.ndarray:
    mask = Image.open(path).convert("L")
    array = np.asarray(mask)
    return array > 0


def load_image(path: Path, size: int) -> np.ndarray:
    image = Image.open(path).convert("L").resize((size, size), Image.Resampling.BILINEAR)
    return np.asarray(image, dtype=np.float32) / 255.0


def mask_geometry(
    split: str,
    mask_path: Path,
    image_path: Path | None,
    description: str,
) -> SampleGeometry:
    mask = load_mask(mask_path)
    height, width = mask.shape
    area = int(mask.sum())
    total = max(height * width, 1)

    if area > 0:
        ys, xs = np.nonzero(mask)
        centroid_x = float(xs.mean() / max(width - 1, 1))
        centroid_y = float(ys.mean() / max(height - 1, 1))
        bbox_h = int(ys.max() - ys.min() + 1)
        bbox_w = int(xs.max() - xs.min() + 1)
        bbox_area_ratio = float((bbox_h * bbox_w) / total)
        labeled, component_count = ndimage.label(mask)
        component_sizes = np.bincount(labeled.ravel())[1:]
        largest_component_ratio = float(component_sizes.max() / area) if len(component_sizes) else 0.0
    else:
        centroid_x = math.nan
        centroid_y = math.nan
        bbox_area_ratio = 0.0
        component_count = 0
        largest_component_ratio = 0.0

    return SampleGeometry(
        split=split,
        image_name=image_path.name if image_path else "",
        mask_name=mask_path.name,
        height=height,
        width=width,
        mask_area=area,
        mask_area_ratio=float(area / total),
        bbox_area_ratio=bbox_area_ratio,
        centroid_x=centroid_x,
        centroid_y=centroid_y,
        component_count=int(component_count),
        largest_component_ratio=largest_component_ratio,
        text_laterality=parse_laterality(description),
        text_area_count=parse_area_count(description),
        description=description,
    )


def resized_mask(path: Path, size: int) -> np.ndarray:
    mask = Image.open(path).convert("L").resize((size, size), Image.Resampling.NEAREST)
    return (np.asarray(mask) > 0).astype(np.float32)


def summarize(df: pd.DataFrame) -> dict[str, object]:
    nonempty = df[df["mask_area"] > 0]
    return {
        "samples": int(len(df)),
        "nonempty_masks": int(len(nonempty)),
        "empty_masks": int((df["mask_area"] == 0).sum()),
        "median_mask_area_ratio": float(nonempty["mask_area_ratio"].median()) if len(nonempty) else 0.0,
        "mean_mask_area_ratio": float(nonempty["mask_area_ratio"].mean()) if len(nonempty) else 0.0,
        "small_mask_ratio_lt_1pct": float((nonempty["mask_area_ratio"] < 0.01).mean()) if len(nonempty) else 0.0,
        "median_component_count": float(nonempty["component_count"].median()) if len(nonempty) else 0.0,
        "split_counts": {k: int(v) for k, v in df["split"].value_counts().to_dict().items()},
        "text_laterality_counts": {k: int(v) for k, v in df["text_laterality"].value_counts().to_dict().items()},
    }


def plot_geometry(
    df: pd.DataFrame,
    records: list[tuple[str, Path, Path | None, str]],
    output: Path,
    title: str,
    heatmap_size: int,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    mean_mask = np.zeros((heatmap_size, heatmap_size), dtype=np.float32)
    mean_image = np.zeros((heatmap_size, heatmap_size), dtype=np.float32)
    image_count = 0
    for _, mask_path, image_path, _ in records:
        mean_mask += resized_mask(mask_path, heatmap_size)
        if image_path and image_path.exists():
            mean_image += load_image(image_path, heatmap_size)
            image_count += 1
    mean_mask /= max(len(records), 1)
    if image_count:
        mean_image /= image_count

    fig, axes = plt.subplots(2, 3, figsize=(16, 9.5))
    fig.suptitle(title, fontsize=18, fontweight="bold")

    axes[0, 0].imshow(mean_image if image_count else np.zeros_like(mean_mask), cmap="gray")
    axes[0, 0].set_title("Ảnh trung bình" if image_count else "Ảnh trung bình (không có ảnh)")
    axes[0, 0].axis("off")

    heat = axes[0, 1].imshow(mean_mask, cmap="magma")
    axes[0, 1].set_title("Heatmap trung bình của mask")
    axes[0, 1].axis("off")
    fig.colorbar(heat, ax=axes[0, 1], fraction=0.046, pad=0.04)

    nonempty = df[df["mask_area"] > 0].copy()
    axes[0, 2].hist(nonempty["mask_area_ratio"] * 100, bins=30, color="#0f4c81", alpha=0.88)
    axes[0, 2].set_title("Phân bố diện tích mask")
    axes[0, 2].set_xlabel("Diện tích mask / ảnh (%)")
    axes[0, 2].set_ylabel("Số mẫu")

    axes[1, 0].scatter(nonempty["centroid_x"], nonempty["centroid_y"], s=14, alpha=0.45, color="#0b8f86")
    axes[1, 0].invert_yaxis()
    axes[1, 0].set_xlim(0, 1)
    axes[1, 0].set_ylim(1, 0)
    axes[1, 0].set_title("Tâm hình học của mask")
    axes[1, 0].set_xlabel("Trục ngang chuẩn hóa")
    axes[1, 0].set_ylabel("Trục dọc chuẩn hóa")
    axes[1, 0].axvline(0.5, color="#1d3557", linestyle="--", linewidth=1)
    axes[1, 0].axhline(1 / 3, color="#9aa7b2", linestyle="--", linewidth=1)
    axes[1, 0].axhline(2 / 3, color="#9aa7b2", linestyle="--", linewidth=1)

    clipped_components = nonempty["component_count"].clip(upper=8)
    axes[1, 1].hist(clipped_components, bins=np.arange(0.5, 9.6, 1), color="#e76f51", alpha=0.88)
    axes[1, 1].set_title("Số thành phần liên thông")
    axes[1, 1].set_xlabel("Số component (>=8 được gộp)")
    axes[1, 1].set_ylabel("Số mẫu")

    groups = []
    labels = []
    for label in ("Unilateral", "Bilateral", "Unknown"):
        values = nonempty.loc[nonempty["text_laterality"] == label, "mask_area_ratio"] * 100
        if len(values):
            groups.append(values)
            labels.append(label)
    if groups:
        axes[1, 2].boxplot(groups, labels=labels, showfliers=False)
    axes[1, 2].set_title("Diện tích mask theo text laterality")
    axes[1, 2].set_ylabel("Diện tích mask / ảnh (%)")

    for ax in axes.flat:
        if ax.has_data():
            ax.grid(alpha=0.25, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path)
    parser.add_argument("--samples-csv", type=Path)
    parser.add_argument("--title", default="EDA hình học mask")
    parser.add_argument("--heatmap-size", type=int, default=224)
    args = parser.parse_args()

    records = list_mask_records(args.dataset_root)
    if not records:
        raise SystemExit(f"No LViT-style masks found under {args.dataset_root}")

    geometries = [mask_geometry(*record) for record in records]
    df = pd.DataFrame(asdict(item) for item in geometries)

    plot_geometry(df, records, args.output, args.title, args.heatmap_size)

    summary_path = args.summary_json or args.output.with_suffix(".summary.json")
    csv_path = args.samples_csv or args.output.with_suffix(".samples.csv")
    summary_path.write_text(json.dumps(summarize(df), ensure_ascii=False, indent=2), encoding="utf-8")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(json.dumps({"figure": str(args.output), "summary": str(summary_path), "samples": str(csv_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
