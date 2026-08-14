from __future__ import annotations

import csv
import os
import shutil
import stat
from pathlib import Path


ROOT = Path(r"C:\Users\ASUS\OneDrive\Documents\GitHub\LViT_improved")
OUT_ROOT = ROOT / "submission_source_package"
PKG_NAME = "23127016_23127333_Project03_FINAL"
PKG = OUT_ROOT / PKG_NAME


def clean_dir(path: Path) -> None:
    def onerror(func, p, _exc):  # noqa: ANN001
        os.chmod(p, stat.S_IWRITE)
        func(p)

    if path.exists():
        shutil.rmtree(path, onerror=onerror)
    path.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    def ignore(_dir: str, names: list[str]) -> set[str]:
        ignored = set()
        for name in names:
            if name == "__pycache__" or name.endswith(".pyc") or name.endswith(".ipynb_checkpoints"):
                ignored.add(name)
        return ignored

    shutil.copytree(src, dst, ignore=ignore)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def build() -> None:
    clean_dir(PKG)
    (PKG / "Source").mkdir(parents=True, exist_ok=True)
    (PKG / "Docs").mkdir(parents=True, exist_ok=True)
    (PKG / "Demo").mkdir(parents=True, exist_ok=True)

    # Root-level metadata
    for rel in ["requirements.txt", "requirements-kaggle.txt", "LICENSE", "README.md", "CITATION.cff"]:
        copy_file(ROOT / rel, PKG / rel)

    # Core baseline reference
    copy_tree(
        ROOT / "experiments" / "kaggle_runs" / "baseline_lvit_original_reference",
        PKG / "Source" / "01_core_baseline_lvit",
    )

    # Core improved source
    copy_tree(ROOT / "src", PKG / "Source" / "02_core_improved_qatalvit" / "src")
    copy_tree(ROOT / "tests", PKG / "Source" / "02_core_improved_qatalvit" / "tests")
    copy_file(ROOT / "requirements.txt", PKG / "Source" / "02_core_improved_qatalvit" / "requirements.txt")
    copy_file(
        ROOT / "requirements-kaggle.txt",
        PKG / "Source" / "02_core_improved_qatalvit" / "requirements-kaggle.txt",
    )

    # QaTa runners / ablations
    qata_dirs = [
        "qatacov19_all_in_one_25_50_100_runner",
        "qatacov19_biomedbert_50pct_main",
        "qatacov19_biomedbert_50pct_rerun_epi099_locked",
        "qatacov19_hp_batch_global16_lr3e4_clean",
        "qatacov19_hp_batch_global24_lr3e4_clean",
        "qatacov19_hp_globalbs16_lr3e4",
        "qatacov19_hp_lr1e3_global32",
        "qatacov19_hp_lr1e4_global32",
        "qatacov19_i3_i5_clean_off_ablation",
        "qatacov19_nobert_50pct_text_encoder",
    ]
    for name in qata_dirs:
        copy_tree(
            ROOT / "experiments" / "kaggle_runs" / name,
            PKG / "Source" / "03_qatacov19_runners" / name,
        )

    # MosMed runners / ablations
    mosmed_dirs = [
        "mosmed_biomedbert_base_50pct",
        "mosmed_biomedbert_lightau_50pct",
        "mosmed_biomedbert_preprocess_crop_50pct",
        "mosmed_biomedbert_studentonly_50pct",
        "mosmed_nobert_lightau_fixedthr050_50pct",
        "mosmed_nobert_studentonly_fixedthr050_50pct",
        "mosmed_nobert_studentonly_valthr_50pct",
    ]
    for name in mosmed_dirs:
        copy_tree(
            ROOT / "experiments" / "kaggle_runs" / name,
            PKG / "Source" / "04_mosmeddata_plus_runners" / name,
        )

    # Analysis / EDA
    copy_tree(ROOT / "scripts", PKG / "Source" / "05_analysis_and_eda" / "scripts")

    # Standalone notebooks
    copy_tree(ROOT / "notebooks", PKG / "Source" / "06_notebooks")

    # Sample outputs (lightweight evidence only)
    sample_map = {
        "qata_baseline_25pct": ROOT / "analysis_outputs" / "lvit_baseline_25pct",
        "qata_baseline_50pct": ROOT / "analysis_outputs" / "lvit_baseline_50pct",
        "qata_improved_25pct": ROOT / "analysis_outputs" / "qatalvit_25pct",
        "qata_improved_50pct": ROOT / "analysis_outputs" / "qatalvit_50pct",
        "qata_improved_100pct": ROOT / "analysis_outputs" / "qatalvit_100pct",
        "mosmed_baseline_50pct": ROOT / "tmp_mosmed_baseline" / "mosmed_50",
        "mosmed_improved_50pct": ROOT / "analysis_outputs" / "mosmed_improved_runs" / "50pct",
    }
    allowed_names = {
        "metrics_report.csv",
        "metrics_report.json",
        "epoch_metrics.csv",
        "epoch_metrics.json",
        "epoch_training_metrics.csv",
        "epoch_training_metrics.json",
        "pseudo_label_vs_ground_truth_holdout.csv",
        "pseudo_label_vs_ground_truth_holdout.json",
        "labeled_subset_meta.json",
        "train_mask_area.csv",
        "val_mask_area.csv",
        "test_threshold_summary.csv",
        "val_threshold_diagnostics.csv",
        "test_threshold_diagnostics.csv",
        "test_source_threshold_metrics.csv",
        "val_source_threshold_metrics.csv",
        "test_source_best_threshold.csv",
        "val_source_best_threshold.csv",
        "test_area_by_threshold.csv",
        "val_area_by_threshold.csv",
        "test_probability_histogram.csv",
        "val_probability_histogram.csv",
    }
    allowed_suffixes = {".log"}
    for tag, src_dir in sample_map.items():
        dst_dir = PKG / "Source" / "07_sample_outputs" / tag
        dst_dir.mkdir(parents=True, exist_ok=True)
        for item in src_dir.iterdir():
            if item.is_file() and (item.name in allowed_names or item.suffix in allowed_suffixes):
                copy_file(item, dst_dir / item.name)

    # Docs and demo
    report_pdf = ROOT / "manuscript" / "main.pdf"
    slides_pdf = ROOT / "slides" / "lvit_full_report_slides.pdf"
    if report_pdf.exists():
        copy_file(report_pdf, PKG / "Docs" / "qatalvit_report.pdf")
    if slides_pdf.exists():
        copy_file(slides_pdf, PKG / "Docs" / "qatalvit_slides.pdf")
    copy_file(ROOT / "docs" / "phan_cong_cong_viec_fft.pdf", PKG / "Docs" / "phan_cong_cong_viec_fft.pdf")
    write_text(
        PKG / "Docs" / "README.md",
        """
        Thư mục này chứa tài liệu PDF đi kèm bộ source nộp:
        - `qatalvit_report.pdf`: báo cáo chính
        - `qatalvit_slides.pdf`: slide thuyết trình
        - `phan_cong_cong_viec_fft.pdf`: bảng phân công công việc
        """,
    )
    write_text(
        PKG / "Demo" / "DEMO_LINK.txt",
        """
        GitHub repository tham khảo / nơi tổng hợp mã:
        https://github.com/TQC0103/QaTaLViT
        """,
    )
    write_text(
        PKG / "Demo" / "README.md",
        """
        Thư mục này chứa thông tin truy cập nhanh tới bản demo / repo tổng hợp mã.
        Nếu cần xem nhanh cấu trúc tổng thể hoặc lịch sử cập nhật, mở `DEMO_LINK.txt`.
        """,
    )

    # Folder READMEs
    write_text(
        PKG / "Source" / "01_core_baseline_lvit" / "README_SUBMISSION.md",
        """
        Thư mục này chứa source baseline LViT gốc dùng làm mốc phương pháp.
        Mục đích: tái hiện mô hình gốc, đối chiếu với các kết quả cải tiến ở phần sau.
        """,
    )
    write_text(
        PKG / "Source" / "02_core_improved_qatalvit" / "README_SUBMISSION.md",
        """
        Thư mục này chứa source code lõi mà nhóm dùng để tổ chức lại pipeline QaTaLViT:
        - mô hình / nets
        - train / eval
        - text encoder
        - dataset loader
        - test và tiện ích
        Đây là phần source quan trọng nhất nếu muốn đọc cấu trúc chương trình theo module.
        """,
    )
    write_text(
        PKG / "Source" / "03_qatacov19_runners" / "README_SUBMISSION.md",
        """
        Runner, notebook và ablation dành cho QaTa-COV19.
        Bao gồm các cấu hình chính, rerun, hyperparameter sweep và biến thể NoBERT / clean-off.
        """,
    )
    write_text(
        PKG / "Source" / "04_mosmeddata_plus_runners" / "README_SUBMISSION.md",
        """
        Runner, notebook và recipe dành cho MosMedData+.
        Bao gồm các cấu hình BiomedBERT, NoBERT, crop, light augmentation, student-only và threshold variants.
        """,
    )
    write_text(
        PKG / "Source" / "05_analysis_and_eda" / "README_SUBMISSION.md",
        """
        Script EDA và phân tích kết quả:
        - EDA văn bản / hình học mask
        - alignment prompt-mask
        - gallery prior LV loss
        - dựng notebook / Kaggle bundle
        - trực quan hóa kết quả QaTa / MosMed
        """,
    )
    write_text(
        PKG / "Source" / "06_notebooks" / "README_SUBMISSION.md",
        """
        Notebook rời dùng để chạy hoặc kiểm tra nhanh trên Kaggle / Colab.
        """,
    )
    write_text(
        PKG / "Source" / "07_sample_outputs" / "README_SUBMISSION.md",
        """
        Một số output nhẹ được chọn lọc từ các lần chạy:
        metrics, learning curves dạng CSV/JSON, pseudo-label holdout, threshold summaries và log.
        Mục đích là chứng minh pipeline đã chạy và tạo artifact, nhưng không nhồi toàn bộ output nặng vào bộ source nộp.
        """,
    )

    # Root README and manifest
    write_text(
        PKG / "README.md",
        f"""
        # {PKG_NAME}

        Đây là bộ source code được tổ chức lại để nộp đồ án môn **Ứng dụng xử lý ảnh và video số**.

        ## Cấu trúc chính

        - `Source/01_core_baseline_lvit/`: source baseline LViT gốc dùng làm mốc đối chiếu.
        - `Source/02_core_improved_qatalvit/`: source code lõi đã tổ chức lại cho pipeline QaTaLViT.
        - `Source/03_qatacov19_runners/`: runner và notebook cho các thí nghiệm QaTa-COV19.
        - `Source/04_mosmeddata_plus_runners/`: runner và notebook cho các thí nghiệm MosMedData+.
        - `Source/05_analysis_and_eda/`: script EDA và phân tích kết quả.
        - `Source/06_notebooks/`: notebook độc lập tiện chạy trên Kaggle/Colab.
        - `Source/07_sample_outputs/`: output mẫu nhẹ (csv/json/log) để minh họa kết quả chạy.
        - `Docs/`: báo cáo PDF, slide PDF và tài liệu phụ.
        - `Demo/`: thông tin demo / liên kết repo.

        ## Nguyên tắc tổ chức

        1. Tách rõ **source tham khảo** và **source nhóm phát triển**.
        2. Tách rõ **runner thí nghiệm theo dataset**.
        3. Tách rõ **code phân tích** và **output mẫu**.
        4. Giữ lại notebook và script `.py` song song ở các cấu hình Kaggle quan trọng.
        """,
    )

    manifest_rows = [
        ["01_core_baseline_lvit", "Source baseline LViT gốc", "Mốc phương pháp / tái hiện LViT"],
        ["02_core_improved_qatalvit", "Source lõi QaTaLViT đã tổ chức lại", "Mã nguồn chính của nhóm"],
        ["03_qatacov19_runners", "Runner và notebook QaTa-COV19", "Các cấu hình 25/50/100 và ablation"],
        ["04_mosmeddata_plus_runners", "Runner và notebook MosMedData+", "Các recipe CT và threshold variants"],
        ["05_analysis_and_eda", "Script EDA và phân tích", "Phân tích dữ liệu, metric, artifact"],
        ["06_notebooks", "Notebook độc lập", "Chạy nhanh / tham khảo môi trường Kaggle-Colab"],
        ["07_sample_outputs", "Output mẫu nhẹ", "CSV/JSON/log đại diện cho các lần chạy"],
        ["Docs", "Tài liệu PDF", "Báo cáo, slide, phân công"],
        ["Demo", "Liên kết demo / repo", "Thông tin truy cập nhanh"],
    ]
    with (PKG / "Source" / "MANIFEST.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["folder", "description", "purpose"])
        writer.writerows(manifest_rows)

    # Zip package
    zip_base = OUT_ROOT / PKG_NAME
    zip_target = OUT_ROOT / f"{PKG_NAME}.zip"
    if zip_target.exists():
        zip_target.unlink()
    shutil.make_archive(str(zip_base), "zip", root_dir=OUT_ROOT, base_dir=PKG_NAME)


if __name__ == "__main__":
    build()
    print(PKG)
