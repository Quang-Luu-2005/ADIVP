"""Analyze alignment between LViT text annotations and segmentation masks.

This script answers whether structured text fields such as unilateral/bilateral
or upper/middle/lower are reflected in the pixel-level ground-truth masks.
It produces a compact figure plus CSV/JSON outputs for report writing.
"""

from __future__ import annotations

import argparse
import json
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
REGIONS = ("upper", "middle", "lower", "all")
LATERALITY_LABELS = ("Left", "Right", "Bilateral", "Unknown")
VERTICAL_LABELS = ("Upper", "Middle", "Lower", "Diffuse", "Unknown")


@dataclass
class AlignmentRecord:
    split: str
    sample_name: str
    description: str
    text_laterality: str
    mask_laterality: str
    text_vertical: str
    mask_vertical: str
    text_area_count: float | None
    mask_component_count: int
    mask_area_ratio: float
    laterality_match: bool
    vertical_match: bool


def read_table(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".tsv", ".txt"}:
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
        if image_name:
            description = str(row.get(text_col, "")).strip()
            mapping[image_name] = description
            mapping[Path(image_name).stem] = description
    return mapping


def list_records(root: Path) -> list[tuple[str, Path, str]]:
    records: list[tuple[str, Path, str]] = []
    for split_name, split_dir, text_file in SPLIT_SPECS:
        split_root = root / split_dir
        mask_dir = split_root / "labelcol"
        if not mask_dir.exists():
            continue
        text_map = load_text_map(split_root, text_file)
        for mask_path in sorted(p for p in mask_dir.rglob("*") if p.suffix.lower() in IMAGE_SUFFIXES):
            description = text_map.get(mask_path.name, text_map.get(mask_path.stem, ""))
            if description:
                records.append((split_name, mask_path, description))
    return records


def parse_text_laterality(text: str) -> str:
    lower = text.lower()
    if re.search(r"\bbilateral\b|\bboth lungs?\b", lower):
        return "Bilateral"
    has_left = "left" in lower
    has_right = "right" in lower
    if has_left and has_right:
        return "Bilateral"
    if has_left:
        return "Left"
    if has_right:
        return "Right"
    if re.search(r"\bunilateral\b", lower):
        return "Unknown"
    return "Unknown"


def parse_text_vertical(text: str) -> str:
    lower = text.lower()
    regions = {region for region in REGIONS if re.search(rf"\b{region}\b", lower)}
    if "all" in regions or len(regions.intersection({"upper", "middle", "lower"})) >= 2:
        return "Diffuse"
    if "upper" in regions:
        return "Upper"
    if "middle" in regions:
        return "Middle"
    if "lower" in regions:
        return "Lower"
    return "Unknown"


def parse_area_count(text: str) -> float | None:
    lower = text.lower()
    match = re.search(r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+infected areas?\b", lower)
    if match:
        return float(NUMBER_WORDS[match.group(1)])
    digit = re.search(r"\b(\d+)\s+infected areas?\b", lower)
    return float(digit.group(1)) if digit else None


def load_mask(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("L")) > 0


def mask_laterality(mask: np.ndarray, side_mass_threshold: float = 0.15) -> str:
    area = float(mask.sum())
    if area == 0:
        return "Unknown"
    mid = mask.shape[1] // 2
    left_mass = float(mask[:, :mid].sum()) / area
    right_mass = float(mask[:, mid:].sum()) / area
    if left_mass >= side_mass_threshold and right_mass >= side_mass_threshold:
        return "Bilateral"
    if left_mass > right_mass:
        return "Left"
    if right_mass > left_mass:
        return "Right"
    return "Unknown"


def mask_vertical(mask: np.ndarray, band_mass_threshold: float = 0.25) -> str:
    area = float(mask.sum())
    if area == 0:
        return "Unknown"
    height = mask.shape[0]
    b1 = height // 3
    b2 = 2 * height // 3
    masses = np.array(
        [
            mask[:b1, :].sum(),
            mask[b1:b2, :].sum(),
            mask[b2:, :].sum(),
        ],
        dtype=np.float64,
    )
    fractions = masses / area
    active = fractions >= band_mass_threshold
    if active.sum() >= 2:
        return "Diffuse"
    return ("Upper", "Middle", "Lower")[int(fractions.argmax())]


def component_count(mask: np.ndarray) -> int:
    _, count = ndimage.label(mask)
    return int(count)


def laterality_compatible(text_label: str, mask_label: str) -> bool:
    if text_label == "Unknown" or mask_label == "Unknown":
        return False
    if text_label == mask_label:
        return True
    if text_label == "Bilateral" and mask_label in {"Left", "Right"}:
        return False
    return False


def vertical_compatible(text_label: str, mask_label: str) -> bool:
    if text_label == "Unknown" or mask_label == "Unknown":
        return False
    if text_label == mask_label:
        return True
    if text_label == "Diffuse" and mask_label in {"Upper", "Middle", "Lower", "Diffuse"}:
        return True
    return False


def analyze_record(split: str, mask_path: Path, description: str) -> AlignmentRecord:
    mask = load_mask(mask_path)
    text_lat = parse_text_laterality(description)
    mask_lat = mask_laterality(mask)
    text_vert = parse_text_vertical(description)
    mask_vert = mask_vertical(mask)
    area = float(mask.sum()) / max(mask.size, 1)
    comps = component_count(mask)
    return AlignmentRecord(
        split=split,
        sample_name=mask_path.name,
        description=description,
        text_laterality=text_lat,
        mask_laterality=mask_lat,
        text_vertical=text_vert,
        mask_vertical=mask_vert,
        text_area_count=parse_area_count(description),
        mask_component_count=comps,
        mask_area_ratio=area,
        laterality_match=laterality_compatible(text_lat, mask_lat),
        vertical_match=vertical_compatible(text_vert, mask_vert),
    )


def crosstab(df: pd.DataFrame, row: str, col: str, row_labels: tuple[str, ...], col_labels: tuple[str, ...]) -> pd.DataFrame:
    table = pd.crosstab(df[row], df[col])
    return table.reindex(index=row_labels, columns=col_labels, fill_value=0)


def plot_heatmap(ax, table: pd.DataFrame, title: str) -> None:
    image = ax.imshow(table.values, cmap="Blues")
    ax.set_title(title)
    ax.set_xticks(range(len(table.columns)), table.columns, rotation=30, ha="right")
    ax.set_yticks(range(len(table.index)), table.index)
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            value = int(table.values[i, j])
            if value:
                ax.text(j, i, str(value), ha="center", va="center", fontsize=9)
    plt.colorbar(image, ax=ax, fraction=0.046, pad=0.04)


def plot_alignment(df: pd.DataFrame, output: Path, title: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 3, figsize=(16, 9.2))
    fig.suptitle(title, fontsize=18, fontweight="bold")

    lat_table = crosstab(df, "text_laterality", "mask_laterality", LATERALITY_LABELS, LATERALITY_LABELS)
    vert_table = crosstab(df, "text_vertical", "mask_vertical", VERTICAL_LABELS, VERTICAL_LABELS)
    plot_heatmap(axes[0, 0], lat_table, "Text laterality vs mask laterality")
    plot_heatmap(axes[0, 1], vert_table, "Text vertical region vs mask vertical region")

    agreement_values = [
        float(df["laterality_match"].mean()) if len(df) else 0.0,
        float(df["vertical_match"].mean()) if len(df) else 0.0,
        float((df["laterality_match"] & df["vertical_match"]).mean()) if len(df) else 0.0,
    ]
    axes[0, 2].bar(["Laterality", "Vertical", "Both"], agreement_values, color=["#0f4c81", "#0b8f86", "#e76f51"])
    axes[0, 2].set_ylim(0, 1)
    axes[0, 2].set_title("Tỉ lệ khớp text--mask")
    axes[0, 2].set_ylabel("Tỉ lệ")
    for idx, value in enumerate(agreement_values):
        axes[0, 2].text(idx, value + 0.02, f"{value:.2f}", ha="center")

    groups = []
    labels = []
    for label in ("Left", "Right", "Bilateral", "Unknown"):
        values = df.loc[df["text_laterality"] == label, "mask_area_ratio"] * 100
        if len(values):
            groups.append(values)
            labels.append(label)
    if groups:
        axes[1, 0].boxplot(groups, labels=labels, showfliers=False)
    axes[1, 0].set_title("Diện tích mask theo text laterality")
    axes[1, 0].set_ylabel("Diện tích mask / ảnh (%)")

    area_count_df = df.dropna(subset=["text_area_count"]).copy()
    if len(area_count_df):
        area_count_df["text_area_count_clipped"] = area_count_df["text_area_count"].clip(upper=5)
        box_data = []
        box_labels = []
        for count in sorted(area_count_df["text_area_count_clipped"].unique()):
            values = area_count_df.loc[area_count_df["text_area_count_clipped"] == count, "mask_component_count"].clip(upper=10)
            box_data.append(values)
            box_labels.append("5+" if count >= 5 else str(int(count)))
        axes[1, 1].boxplot(box_data, labels=box_labels, showfliers=False)
    axes[1, 1].set_title("Số component mask theo số vùng trong text")
    axes[1, 1].set_xlabel("Số vùng nhiễm trong text")
    axes[1, 1].set_ylabel("Số component mask")

    split_agreement = df.groupby("split")[["laterality_match", "vertical_match"]].mean()
    split_agreement.plot(kind="bar", ax=axes[1, 2], color=["#0f4c81", "#0b8f86"])
    axes[1, 2].set_ylim(0, 1)
    axes[1, 2].set_title("Tỉ lệ khớp theo split")
    axes[1, 2].set_ylabel("Tỉ lệ")
    axes[1, 2].legend(["Laterality", "Vertical"])
    axes[1, 2].tick_params(axis="x", rotation=0)

    for ax in axes.flat:
        ax.grid(alpha=0.23, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output, dpi=180)
    plt.close(fig)


def summarize(df: pd.DataFrame) -> dict[str, object]:
    return {
        "samples_with_text_and_mask": int(len(df)),
        "laterality_match_rate": float(df["laterality_match"].mean()) if len(df) else 0.0,
        "vertical_match_rate": float(df["vertical_match"].mean()) if len(df) else 0.0,
        "both_match_rate": float((df["laterality_match"] & df["vertical_match"]).mean()) if len(df) else 0.0,
        "text_laterality_counts": {k: int(v) for k, v in df["text_laterality"].value_counts().to_dict().items()},
        "mask_laterality_counts": {k: int(v) for k, v in df["mask_laterality"].value_counts().to_dict().items()},
        "text_vertical_counts": {k: int(v) for k, v in df["text_vertical"].value_counts().to_dict().items()},
        "mask_vertical_counts": {k: int(v) for k, v in df["mask_vertical"].value_counts().to_dict().items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path)
    parser.add_argument("--samples-csv", type=Path)
    parser.add_argument("--title", default="EDA khớp text annotation và mask")
    args = parser.parse_args()

    records = list_records(args.dataset_root)
    if not records:
        raise SystemExit(f"No masks with text annotations found under {args.dataset_root}")

    df = pd.DataFrame(asdict(analyze_record(*record)) for record in records)
    plot_alignment(df, args.output, args.title)

    summary_path = args.summary_json or args.output.with_suffix(".summary.json")
    csv_path = args.samples_csv or args.output.with_suffix(".samples.csv")
    summary_path.write_text(json.dumps(summarize(df), ensure_ascii=False, indent=2), encoding="utf-8")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(json.dumps({"figure": str(args.output), "summary": str(summary_path), "samples": str(csv_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
