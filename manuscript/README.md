# Manuscript

This folder contains the LaTeX source for the QaTaLViT report.

## Structure

```text
manuscript/
|-- main.tex
|-- preface.tex
|-- info.tex
|-- Glossary.tex
|-- references.bib
|-- figures/
|-- sections/
|   `-- content_main.tex
|-- tables/
`-- Bao_cao_do_an_LViT_QaTaLViT.pdf
```

`Bao_cao_do_an_LViT_QaTaLViT.pdf` is the latest compiled report. Temporary LaTeX logs and preview renders are not kept in the repository.

## Build

Run from this folder:

```powershell
xelatex -interaction=nonstopmode main.tex
bibtex main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

The content body is in `sections/content_main.tex`; metadata and cover information are in `main.tex`, `cover.tex`, and `info.tex`.
