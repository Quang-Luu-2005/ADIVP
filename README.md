# QaTaLViT

Text-augmented medical image segmentation under limited labels, built on top of LViT.

QaTaLViT combines visual features with clinical text prompts and evaluates semi-supervised segmentation on the QaTa-COV19 and MosMedData+ datasets. This repository contains the reproducible research code, selected experiment notebooks, report sources, presentation materials, and representative outputs.

## Highlights

- PyTorch implementation of the LViT baseline and improved QaTaLViT model.
- Semi-supervised training and text-guided medical image segmentation.
- Reproducible Kaggle/Colab experiment notebooks and dataset-specific runners.
- Unit tests for datasets, model components, and training utilities.
- Report, slides, references, and representative evaluation artifacts.

## Repository layout

```text
.
├── src/             # Core models, datasets, training, and evaluation code
├── scripts/         # Experiment runners, analysis, and packaging utilities
├── tests/           # Lightweight automated tests
├── notebooks/       # Standalone Kaggle/Colab notebooks
├── experiments/     # Selected experiment snapshots used in the report
├── submission/      # Curated source package organized by experiment role
├── manuscript/      # LaTeX report source, figures, tables, and compiled PDF
├── slides/          # Beamer source, speaker notes, and presentation PDFs
├── data/            # Dataset notes, sample outputs, and result visualizations
├── references/      # BibTeX entries and paper soft copies
└── docs/            # Demo notes and project documentation
```

Large datasets and model checkpoints are not included. Dataset setup notes are available in [`data/dataset_links_and_notes/DATA.md`](data/dataset_links_and_notes/DATA.md).

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

For Kaggle notebooks, install the lighter environment from `requirements-kaggle.txt` and follow the README in the corresponding experiment folder.

Example training command:

```powershell
python scripts/run_qatacov19_050pct.py --dataset-root C:\path\to\QaTa-Covid19 --epochs 120
```

## Documentation and citation

- [Report source and PDF](manuscript/)
- [Presentation materials](slides/)
- [Dataset and experiment notes](data/)
- [Citation metadata](CITATION.cff)

This project builds on the original LViT work:

```bibtex
@article{li2023lvit,
  title={LViT: Language Meets Vision Transformer in Medical Image Segmentation},
  author={Li, Zihan and Li, Yunxiang and Li, Qingde and Wang, Puyang and Guo, Dazhou and Lu, Le and Jin, Dakai and Zhang, You and Hong, Qingqi},
  journal={IEEE Transactions on Medical Imaging},
  year={2023},
  publisher={IEEE}
}
```

Released under the MIT License.
