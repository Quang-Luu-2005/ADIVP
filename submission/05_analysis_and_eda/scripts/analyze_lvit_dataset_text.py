"""Analyze LViT-style text annotations and generate report figures."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


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
SPLITS = (
    ("Train", "Train_Folder", "Train_text.xlsx"),
    ("Validation", "Val_Folder", "Val_text.xlsx"),
    ("Test", "Test_Folder", "Test_text.xlsx"),
)


def load_lvit_split(root: Path, split_dir: str, text_file: str) -> pd.DataFrame:
    split_root = root / split_dir
    df = pd.read_excel(split_root / text_file)
    img_dir = split_root / "img"
    existing = {p.name for p in img_dir.iterdir() if p.is_file()}
    matched = df[df["Image"].astype(str).isin(existing)].copy()
    # Some demo folders keep text with original extensions while converted images
    # use a different extension. For text EDA, keep the annotations if names do
    # not match literally but the split-level text file is present.
    df = matched if len(matched) else df.copy()
    df["split"] = split_dir.replace("_Folder", "")
    return df


def load_lvit_dataset(root: Path) -> pd.DataFrame:
    parts = []
    for _, split_dir, text_file in SPLITS:
        path = root / split_dir / text_file
        if path.exists():
            parts.append(load_lvit_split(root, split_dir, text_file))
    if not parts:
        raise FileNotFoundError(f"No LViT text splits found under {root}")
    return pd.concat(parts, ignore_index=True)


def number_from_text(text: str) -> int | None:
    m = re.search(r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+infected areas?\b", text)
    return NUMBER_WORDS.get(m.group(1)) if m else None


def parse_lung_description(text: str) -> dict[str, object]:
    lower = str(text).lower().strip().replace("..", ".")
    laterality = "Bilateral" if lower.startswith("bilateral") else "Unilateral" if lower.startswith("unilateral") else "Unknown"
    area_count = number_from_text(lower)

    info: dict[str, object] = {
        "laterality": laterality,
        "area_count": area_count,
        "left_regions": [],
        "right_regions": [],
    }
    for side in ("left", "right"):
        matches = re.findall(r"((?:upper|middle|lower|all)(?:\s+(?:upper|middle|lower|all))*)\s+" + side + r"\s+lung", lower)
        regions = []
        for match in matches:
            for region in REGIONS:
                if region in match.split():
                    regions.append(region)
        info[f"{side}_regions"] = sorted(set(regions), key=REGIONS.index)
    return info


def enrich_lung(df: pd.DataFrame) -> pd.DataFrame:
    parsed = df["Description"].map(parse_lung_description)
    parsed_df = pd.DataFrame(parsed.tolist())
    out = pd.concat([df.reset_index(drop=True), parsed_df], axis=1)
    out["left_region_combo"] = out["left_regions"].map(lambda xs: "+".join(xs) if xs else "none")
    out["right_region_combo"] = out["right_regions"].map(lambda xs: "+".join(xs) if xs else "none")
    return out


def plot_lung_eda(df: pd.DataFrame, title: str, output: Path) -> dict[str, object]:
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 8.4))
    fig.suptitle(title, fontsize=17, fontweight="bold")

    laterality = df["laterality"].value_counts()
    axes[0, 0].bar(laterality.index, laterality.values, color=["#0f4c81", "#0b8f86", "#9aa7b2"][: len(laterality)])
    axes[0, 0].set_title("Kiểu lan tổn thương")
    axes[0, 0].set_ylabel("Số mẫu")

    area_counts = df["area_count"].dropna().astype(int).value_counts().sort_index()
    axes[0, 1].bar([str(x) for x in area_counts.index], area_counts.values, color="#1f78b4")
    axes[0, 1].set_title("Số vùng nhiễm được mô tả trong text")
    axes[0, 1].set_xlabel("Số vùng")
    axes[0, 1].set_ylabel("Số mẫu")

    left = Counter()
    right = Counter()
    for rows in df["left_regions"]:
        left.update(rows)
    for rows in df["right_regions"]:
        right.update(rows)
    region_labels = list(REGIONS)
    axes[1, 0].bar(region_labels, [left[r] for r in region_labels], color="#2a9d8f")
    axes[1, 0].set_title("Trường vị trí: phổi trái")
    axes[1, 0].set_ylabel("Số lần xuất hiện")
    axes[1, 1].bar(region_labels, [right[r] for r in region_labels], color="#e76f51")
    axes[1, 1].set_title("Trường vị trí: phổi phải")
    axes[1, 1].set_ylabel("Số lần xuất hiện")

    for ax in axes.flat:
        ax.grid(axis="y", linestyle="--", alpha=0.28)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)

    return {
        "n": int(len(df)),
        "laterality": laterality.to_dict(),
        "area_count": {str(k): int(v) for k, v in area_counts.to_dict().items()},
        "left_regions": dict(left),
        "right_regions": dict(right),
        "top_left_combos": df["left_region_combo"].value_counts().head(8).to_dict(),
        "top_right_combos": df["right_region_combo"].value_counts().head(8).to_dict(),
    }


def mosmed_source(image_name: str) -> str:
    name = str(image_name)
    if name.startswith("Morozov"):
        return "Morozov / MosMedData"
    if name.startswith("Jun_coronacases") or name.startswith("Jun_radiopaedia"):
        return "Jun / Coronacases-Radiopaedia"
    if name.startswith("bjorke"):
        return "Bjørke / MedSeg CT"
    return "Khác"


def plot_mosmed_sources(df: pd.DataFrame, output: Path) -> dict[str, object]:
    source_by_split = pd.crosstab(df["split"], df["Image"].map(mosmed_source))
    order = ["Train", "Val", "Test"]
    source_by_split = source_by_split.reindex([x for x in order if x in source_by_split.index])

    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    source_by_split.plot(kind="bar", stacked=True, ax=ax, color=["#0f4c81", "#2a9d8f", "#e9c46a", "#9aa7b2"])
    ax.set_title("MosMedData+: thành phần nguồn theo tiền tố tên ảnh", fontweight="bold")
    ax.set_xlabel("Split")
    ax.set_ylabel("Số lát CT")
    ax.legend(title="Nguồn con", loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.28)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)

    return {
        split: {source: int(count) for source, count in row.items()}
        for split, row in source_by_split.to_dict(orient="index").items()
    }


def parse_monuseg(text: str) -> dict[str, str]:
    lower = str(text).lower()
    if "evenly" in lower:
        density = "đều"
    elif "sparse" in lower or "sparsely" in lower:
        density = "thưa"
    elif "high" in lower or "higher" in lower:
        density = "mật độ cao"
    else:
        density = "khác"

    locations = []
    for token in ("upper", "lower", "left", "right", "around"):
        if token in lower:
            locations.append(token)
    location = "+".join(locations) if locations else "toàn ảnh"
    return {"density_type": density, "location": location}


def plot_monuseg_eda(df: pd.DataFrame, output: Path) -> dict[str, object]:
    parsed = pd.DataFrame(df["Description"].map(parse_monuseg).tolist())
    enriched = pd.concat([df.reset_index(drop=True), parsed], axis=1)

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))
    density = enriched["density_type"].value_counts()
    axes[0].bar(density.index, density.values, color="#0b8f86")
    axes[0].set_title("Loại mô tả mật độ nhân")
    axes[0].set_ylabel("Số mẫu")

    locations = enriched["location"].value_counts()
    axes[1].barh(locations.index, locations.values, color="#0f4c81")
    axes[1].set_title("Vị trí/kiểu phân bố được mô tả")
    axes[1].set_xlabel("Số mẫu")

    for ax in axes:
        ax.grid(axis="x" if ax is axes[1] else "y", linestyle="--", alpha=0.28)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("MoNuSeg: EDA text annotation", fontsize=16, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)

    return {
        "n": int(len(enriched)),
        "density_type": density.to_dict(),
        "location": locations.to_dict(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qata-root", type=Path, required=True)
    parser.add_argument("--mosmed-root", type=Path, required=True)
    parser.add_argument("--monuseg-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("manuscript") / "figures")
    args = parser.parse_args()

    qata = enrich_lung(load_lvit_dataset(args.qata_root))
    mosmed = enrich_lung(load_lvit_dataset(args.mosmed_root))
    monuseg = load_lvit_dataset(args.monuseg_root)

    summary = {
        "qata": plot_lung_eda(qata, "QaTa-COV19: EDA text annotation", args.out_dir / "dataset_text_eda_qatacov19.png"),
        "mosmed": plot_lung_eda(mosmed, "MosMedData+: EDA text annotation", args.out_dir / "dataset_text_eda_mosmeddata.png"),
        "mosmed_sources": plot_mosmed_sources(mosmed, args.out_dir / "dataset_sources_mosmeddata.png"),
        "monuseg": plot_monuseg_eda(monuseg, args.out_dir / "dataset_text_eda_monuseg.png"),
    }
    (args.out_dir / "dataset_text_eda_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
