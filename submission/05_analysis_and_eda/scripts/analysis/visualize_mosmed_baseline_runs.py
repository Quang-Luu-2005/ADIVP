from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(r"C:\Users\ASUS\OneDrive\Documents\GitHub\LViT_improved")
BASE = ROOT / "tmp_mosmed_baseline"
FIG_DIR = ROOT / "manuscript" / "figures"


RUNS = {
    "25": BASE / "mosmed_25",
    "50": BASE / "mosmed_50",
    "100": BASE / "mosmed_100",
}


def load_bundle(run_dir: Path) -> dict[str, object]:
    return {
        "summary": pd.read_csv(run_dir / "metrics_report.csv"),
        "epochs": pd.read_csv(run_dir / "epoch_metrics.csv"),
        "pseudo": json.loads((run_dir / "pseudo_label_vs_ground_truth_holdout.json").read_text(encoding="utf-8")),
        "meta": json.loads((run_dir / "labeled_subset_meta.json").read_text(encoding="utf-8")),
    }


def save_score_bars(bundles: dict[str, dict[str, object]]) -> None:
    ratios = ["25", "50", "100"]
    val_dice = []
    test_dice = []
    val_iou = []
    test_iou = []

    for ratio in ratios:
        summary = bundles[ratio]["summary"].set_index("split")
        val_dice.append(float(summary.loc["val", "dice"]) * 100)
        test_dice.append(float(summary.loc["test", "dice"]) * 100)
        val_iou.append(float(summary.loc["val", "iou"]) * 100)
        test_iou.append(float(summary.loc["test", "iou"]) * 100)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), dpi=180)
    x = range(len(ratios))
    width = 0.34

    axes[0].bar([i - width / 2 for i in x], val_dice, width=width, color="#4c78a8", label="Validation Dice")
    axes[0].bar([i + width / 2 for i in x], test_dice, width=width, color="#f58518", label="Test Dice")
    axes[0].set_xticks(list(x), [f"{r}%" for r in ratios])
    axes[0].set_ylabel("Dice (%)")
    axes[0].set_title("Dice theo tỉ lệ nhãn")
    axes[0].legend()
    axes[0].grid(axis="y", alpha=0.25)

    axes[1].bar([i - width / 2 for i in x], val_iou, width=width, color="#54a24b", label="Validation IoU")
    axes[1].bar([i + width / 2 for i in x], test_iou, width=width, color="#b279a2", label="Test IoU")
    axes[1].set_xticks(list(x), [f"{r}%" for r in ratios])
    axes[1].set_ylabel("IoU (%)")
    axes[1].set_title("IoU theo tỉ lệ nhãn")
    axes[1].legend()
    axes[1].grid(axis="y", alpha=0.25)

    fig.suptitle("MosMedData+ baseline LViT: metric trên validation và test", fontsize=14)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "mosmed_baseline_scores.png", bbox_inches="tight")
    plt.close(fig)


def save_training_curves(bundles: dict[str, dict[str, object]]) -> dict[str, dict[str, float]]:
    ratios = ["25", "50", "100"]
    fig, axes = plt.subplots(3, 2, figsize=(12, 13), dpi=180, sharex="col")
    summary: dict[str, dict[str, float]] = {}

    for row, ratio in enumerate(ratios):
        epochs = bundles[ratio]["epochs"]
        best_idx = epochs["val_dice"].idxmax()
        best_epoch = int(epochs.loc[best_idx, "epoch"])
        best_val_dice = float(epochs.loc[best_idx, "val_dice"]) * 100
        best_val_iou = float(epochs.loc[best_idx, "val_iou"]) * 100
        final_epoch = int(epochs["epoch"].iloc[-1])
        final_val_dice = float(epochs["val_dice"].iloc[-1]) * 100
        final_val_iou = float(epochs["val_iou"].iloc[-1]) * 100

        axes[row, 0].plot(epochs["epoch"], epochs["loss"], color="#1f77b4", linewidth=2, label="Train loss")
        axes[row, 0].plot(epochs["epoch"], epochs["val_loss"], color="#d62728", linewidth=2, label="Val loss")
        axes[row, 0].axvline(best_epoch, color="gray", linestyle="--", linewidth=1)
        axes[row, 0].set_title(f"{ratio}% nhãn: loss")
        axes[row, 0].set_ylabel("Loss")
        axes[row, 0].grid(alpha=0.25)
        if row == 0:
            axes[row, 0].legend()

        axes[row, 1].plot(epochs["epoch"], epochs["dice"] * 100, color="#2ca02c", linewidth=2, label="Train Dice")
        axes[row, 1].plot(epochs["epoch"], epochs["val_dice"] * 100, color="#ff7f0e", linewidth=2, label="Val Dice")
        axes[row, 1].plot(epochs["epoch"], epochs["val_iou"] * 100, color="#9467bd", linewidth=2, label="Val IoU")
        axes[row, 1].scatter([best_epoch], [best_val_dice], color="black", s=24, zorder=5)
        axes[row, 1].annotate(
            f"Best E{best_epoch}\nDice {best_val_dice:.2f}",
            (best_epoch, best_val_dice),
            xytext=(6, -20),
            textcoords="offset points",
            fontsize=8,
        )
        axes[row, 1].set_title(f"{ratio}% nhãn: Dice/IoU")
        axes[row, 1].set_ylabel("Score (%)")
        axes[row, 1].grid(alpha=0.25)
        if row == 0:
            axes[row, 1].legend()

        summary[ratio] = {
            "best_epoch": best_epoch,
            "best_val_dice": best_val_dice,
            "best_val_iou": best_val_iou,
            "final_epoch": final_epoch,
            "final_val_dice": final_val_dice,
            "final_val_iou": final_val_iou,
        }

    axes[2, 0].set_xlabel("Epoch")
    axes[2, 1].set_xlabel("Epoch")
    fig.suptitle("MosMedData+ baseline LViT: learning curves theo tỉ lệ nhãn", fontsize=14)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "mosmed_baseline_training_curves.png", bbox_inches="tight")
    plt.close(fig)
    return summary


def save_pseudo_plot(bundles: dict[str, dict[str, object]]) -> dict[str, dict[str, float]]:
    ratios = ["25", "50"]
    metric_keys = [
        ("dice", "Global Dice"),
        ("iou", "Global IoU"),
        ("mean_sample_dice", "Mean-sample Dice"),
        ("mean_sample_iou", "Mean-sample IoU"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), dpi=180)
    pseudo_summary: dict[str, dict[str, float]] = {}

    for ax, ratio in zip(axes, ratios):
        pseudo = bundles[ratio]["pseudo"]
        values = [float(pseudo[key]) * 100 for key, _ in metric_keys]
        labels = [label for _, label in metric_keys]
        colors = ["#4c78a8", "#54a24b", "#f58518", "#b279a2"]
        ax.bar(range(len(labels)), values, color=colors)
        ax.set_xticks(range(len(labels)), labels, rotation=15, ha="right")
        ax.set_ylim(0, 100)
        ax.set_title(f"{ratio}% nhãn, thr={float(pseudo['threshold']):.2f}")
        ax.set_ylabel("Score (%)")
        ax.grid(axis="y", alpha=0.25)
        pseudo_summary[ratio] = {key: float(pseudo[key]) * 100 for key, _ in metric_keys}
        pseudo_summary[ratio]["threshold"] = float(pseudo["threshold"])
        pseudo_summary[ratio]["samples"] = int(pseudo["samples"])

    fig.suptitle("MosMedData+ baseline LViT: chất lượng pseudo-label holdout", fontsize=14)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "mosmed_baseline_pseudo_holdout.png", bbox_inches="tight")
    plt.close(fig)
    return pseudo_summary


def save_gap_plot(bundles: dict[str, dict[str, object]]) -> None:
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=180)
    palette = {
        "25": "#d62728",
        "50": "#1f77b4",
        "100": "#2ca02c",
    }
    for ratio, color in palette.items():
        epochs = bundles[ratio]["epochs"]
        gap = (epochs["dice"] - epochs["val_dice"]) * 100
        ax.plot(epochs["epoch"], gap, linewidth=2, color=color, label=f"{ratio}% nhãn")

    ax.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_title("Generalization gap của baseline LViT trên MosMedData+")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Train Dice - Val Dice (điểm phần trăm)")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "mosmed_baseline_generalization_gap.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    bundles = {ratio: load_bundle(run_dir) for ratio, run_dir in RUNS.items()}
    save_score_bars(bundles)
    training_summary = save_training_curves(bundles)
    pseudo_summary = save_pseudo_plot(bundles)
    save_gap_plot(bundles)

    summary = {
        "scores": {
            ratio: json.loads((RUNS[ratio] / "metrics_report.json").read_text(encoding="utf-8"))
            for ratio in RUNS
        },
        "training": training_summary,
        "pseudo_holdout": pseudo_summary,
    }
    (FIG_DIR / "mosmed_baseline_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
