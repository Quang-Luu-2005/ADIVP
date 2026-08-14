# Report Development Notes

## Global Writing Requirements From User

Use these requirements for every section from now on:

- Main focus is LViT by Li et al. and the official HUANGLIZI/LViT source code.
- Use the current repo only as reproduction/documentation/illustrative extension; do not make the report mainly about our improved variant.
- Refer to the LViT paper and official repo when explaining method, experiments, source layout, datasets, and results.
- Write self-explanatory sections. Assume the reader may not already know many external architectures.
- At the start of each major section/subsection, include an overview paragraph explaining the big idea, philosophy, and meaning before technical details.
- When using terms such as segmentation, pseudo-label, Transformer, CNN, attention, PLAM, EPI, LV loss, explain the intuition before equations or implementation.
- Add visual illustrations when they help understanding. Prefer clear, professional figures; current Chapter 1 conceptual diagrams use AI-generated PNGs supplied by the user, while repo/paper/dataset images should be used when they clarify the method or experiments.
- Keep continuity: when writing a later section, explicitly build on what earlier sections established.
- Avoid turning the report into a personal project narrative. Contributions from our repo should appear in contribution, implementation, or extension discussion only.
- For Chapter 2, compare works using the same criteria tied to the problem framework.
- Chapter 2 tables should be short and scannable. Keep detailed explanations in prose, not inside table cells. Prefer columns such as work name, text usage or focus, short summary, and limitation.
- For Chapter 4, source code must go together with the method it implements, and the report should describe the source layout clearly.
- For Chapter 3, every method subsection should follow the same internal structure: principle (`Nguyen ly`/bản chất), method (`Phuong phap`/cách LViT thực hiện), algorithm (`Giai thuat`/trình tự tính toán), and illustration (`Minh hoa`/how to read figure/source/formula). Detailed module names should come after the principle, not before it.

## Scope

Report focus: LViT by Li et al., not QaTaLViT as the central contribution.

Repo additions and improved code should be presented as:

- reproduction support,
- code documentation,
- small illustrative extension,
- not as the main method.

## Chapter Continuity

### Chapter 1

Chapter 1 should make the problem understandable before naming detailed architectures.

Key ideas already established or being established:

- Medical image segmentation is dense prediction: each pixel/voxel receives a semantic label.
- It is harder than image-level classification because it must answer what, where, and boundary.
- Pixel masks are expensive because experts need to draw and verify boundaries.
- Medical text annotations/reports are often available and contain useful semantic cues.
- LViT's motivation: use both visual evidence and text annotation to improve segmentation, especially when masks are limited.
- Do not present CNN/Transformer details too early; only introduce them as broad families.

### Section 1.1 Direction

Needs to be self-explanatory:

- Define segmentation with simple contrast to classification/detection.
- Explain clinical relevance.
- Explain why medical segmentation is hard visually.
- Explain why annotation is hard economically and procedurally.
- Explain why text exists naturally and why it matters.
- End by positioning LViT as a bridge between image, text, and limited masks.

Figures added:

- `medical_segmentation_tasks_generated.png`: classification vs detection vs segmentation.
- `lvit_data_context_generated.png`: data sources in an LViT-like setting: image, text annotation, pixel mask.
- `lvit_motivation_generated.png`: three motivations of LViT: ambiguous medical images, expensive masks, underused clinical text.
- `clinical_text_workflow_generated.png`: clinical workflow showing how medical images and clinical text are created before entering an LViT-like model.

### Section 1.1 Completed Summary

Section 1.1 now establishes the background for LViT:

- Medical image segmentation is introduced as a dense prediction task.
- It contrasts segmentation with classification and detection through an AI-generated conceptual figure.
- It explains why masks matter clinically: area, volume, progression, treatment planning, quantitative analysis.
- It explains why medical images are visually hard: low contrast, fuzzy boundaries, noise, anatomical overlap, patient/device/domain variation.
- It explains why pixel masks are expensive: expert annotation, boundary review, ambiguous cases, possible multi-expert agreement.
- It introduces medical text annotation as a naturally available semantic signal.
- It positions LViT as a multi-source view of a medical sample: image gives visual morphology, text gives clinical semantics, mask gives accurate but costly supervision.
- It ends by preparing the next section: LViT is motivated by the need to preserve image detail, use text, and learn carefully when masks are missing.

### Later Awareness

When writing 1.2:

- Build on the bottleneck identified in 1.1: limited high-quality masks and underused text.
- Split scientific meaning and practical meaning explicitly.
- Mention three research motivations:
  1. visual ambiguity of medical segmentation,
  2. annotation scarcity,
  3. underused text annotation.
- Explain why these are scientific problems, not only engineering inconveniences.
- Explain why LViT's idea is meaningful: it asks how to fuse image and text for dense prediction, and how to use text in semi-supervised learning.

When writing 1.3:

- Reuse the same image/text/mask symbols introduced in 1.1.
- Keep framework method-agnostic first.
- Section 1.3 has been rewritten around seven framework stages: data normalization, image encoding, text encoding, image-text fusion, hybrid CNN-Transformer, pseudo-label control, and final segmentation.
- Input/output/ground truth are now separated into Vietnamese subsections: `Dữ liệu đầu vào`, `Đầu ra của hệ thống`, and `Nhãn xác thực và vai trò của mặt nạ`.
- Dataset analysis was added to 1.3:
  - QaTa-COV19: 5716 train, 1429 validation, 2113 test, 9258 total; X-ray COVID-19 lesion segmentation with structured text about laterality/count/location.
  - MosMedData+: 2183 train, 273 validation, 273 test, 2729 total; CT COVID-19 lung infection slices with similar structured text.
  - ESO-CT: 182 train, 46 validation, 58 test, 286 total; esophageal cancer CT with rough tumor location text.
  - Current repo experiments focus on QaTa-COV19 25/50/100% labels and MosMedData+ 50% labels.
- It explicitly separates pretrained parts from task-trained parts:
  - Original LViT uses pretrained BERT-Embed/BERT_12_768_12 for word vectors, while CNN/ViT/PLAM/fusion/decoder are trained for segmentation.
  - Current repo extension can use Microsoft BiomedBERT to cache medical text embeddings, but segmentation and fusion still learn from target datasets.
- It frames Generator-Specialist as a functional explanation for semi-supervised pseudo-labeling, then maps it back to official LViT mechanisms: EPI and LV loss.
- Later Chapter 3 should expand these same stages into the concrete LViT method rather than introducing a different structure.

When writing Chapter 2:

- Compare works by the same framework components: image representation, text representation, fusion, semi-supervised learning, evaluation.

## Update For Section 1.3 Dataset And Framework Revision

- Do not treat data normalization/preparation as a model block in the general framework. It is preprocessing before the model pipeline.
- The current 1.3 framework has six model-level blocks: image encoding, text encoding, image-text fusion, hybrid CNN-Transformer, iterative pseudo-label quality control, and final segmentation.
- Pseudo-label control must be described as an iterative loop: current model generates pseudo-labels, the pseudo-labels are smoothed/checked, the model learns from them, and the updated model generates the next round.
- The datasets now emphasized in 1.3 are QaTa-COV19 and MosMedData+. ESO-CT and MoNuSeg are intentionally omitted from the main dataset discussion to keep the report focused on the COVID-19 LViT setting.
- The report reserves one image-text contact sheet for each selected dataset:
  - `manuscript/figures/dataset_examples_qatacov19.png`
  - `manuscript/figures/dataset_examples_mosmeddata.png`
- `scripts/build_dataset_contact_sheets.py` was added to generate those figures from an LViT-like split containing `img/`, `labelcol/`, and `Train_text.xlsx`/`Val_text.xlsx`.
- `scripts/analyze_lvit_dataset_text.py` was added to perform EDA on LViT text annotations and generate:
  - `dataset_text_eda_qatacov19.png`
  - `dataset_text_eda_mosmeddata.png`
  - `dataset_sources_mosmeddata.png`
  - `dataset_text_eda_summary.json`
- Dataset text analysis should emphasize that the LViT annotations are structured text released with the LViT dataset packages, not raw full clinical reports.
- MosMedData+ should be described as a merged CT dataset with three source families visible from filenames: Morozov/MosMedData, Jun/Coronacases-Radiopaedia, and Bjørke/MedSeg CT.
- The text fields to carry forward are:
  - QaTa-COV19/MosMedData+: laterality, infected-area count, left/right lung location, and upper/middle/lower/all region.

## Chapter 2 Progress

### Section 2.1 Completed Summary

Section 2.1 has been expanded from a short related-work paragraph into a self-explanatory discussion of CNN-based medical image segmentation.

Key ideas now established:

- CNN/U-Net is the feature-map based foundation for medical image segmentation.
- CNN is explained through locality, weight sharing, and spatial feature maps.
- The section maps CNN methods to the Chapter 1 framework: image encoding and segmentation decoding are covered, but text encoding, image-text fusion, and language-guided pseudo-label control are absent.
- FCN is described as the move from image classification to dense pixel prediction.
- DeepLab is described through atrous convolution and multi-scale context.
- U-Net is described through encoder, decoder, and skip connection, including why this helps recover medical boundaries.
- UNet++, Attention U-Net, and nnU-Net are explained as improvements to skip paths, attention filtering, and the full training/evaluation pipeline.
- A comparison table `tab:cnn-related-works` was added with shared criteria: principle, framework component, contribution, and limitation relative to LViT.
- The section ends by motivating the next directions: Transformer for long-range context, vision-language learning for text annotation, and semi-supervised learning for limited masks.

### Section 2.2 Writing Direction

When writing Section 2.2:

- Start by connecting directly to the limitation of Section 2.1: CNN captures local evidence well but long-range relationships are indirect.
- Explain self-attention intuitively before naming ViT or segmentation models.
- Keep the framework mapping clear: Transformer mainly strengthens long-range context and token-based reasoning, while hybrid CNN-Transformer keeps local feature maps.
- Cover the development path: Transformer in NLP, ViT for image tokens, SETR for segmentation as sequence prediction, TransUNet for CNN+Transformer, Swin-Unet for window attention, and UCTransNet for skip/channel modeling.
- Emphasize why LViT is closer to the hybrid family than to pure Transformer segmentation: medical images still need CNN locality and boundary preservation, but also need global context and later text fusion.

### Section 2.2 Completed Summary

Section 2.2 now explains Transformer and hybrid CNN-Transformer methods in continuity with Section 2.1.

Key ideas now established:

- Transformer is introduced as a way to model long-range relationships between tokens, not just local pixel patterns.
- The section explicitly contrasts CNN as feature-map based and Transformer as token-based.
- Self-attention is explained intuitively through query, key, value, and weighted aggregation.
- ViT is described as converting image patches into tokens, with the tradeoff that pure Transformer models often need large data or pretraining.
- SETR is described as segmentation through sequence-to-sequence style patch modeling.
- TransUNet is presented as the most direct bridge from U-Net to hybrid CNN-Transformer segmentation.
- Swin-Unet is explained through window/shifted-window attention as a cost-control mechanism.
- UCTransNet is explained as using Transformer ideas to improve skip connections/channel relationships.
- A comparison table `tab:transformer-related-works` was added with shared criteria: image representation, long-range context, contribution, and limitation/gap for LViT.
- The section concludes that LViT should be read as a hybrid model that preserves CNN locality, adds Transformer context, and prepares for text-guided segmentation rather than as a pure Transformer replacement for U-Net.

### Section 2.3 Completed Summary

Section 2.3 has been expanded into a self-explanatory discussion of vision-language learning and text-guided segmentation.

Key ideas now established:

- Medical images often come with reports, notes, or structured text annotations, so text should be treated as a useful semantic signal rather than decoration.
- The section maps vision-language methods to the Chapter 1 framework: text encoding, image-text fusion, and text-assisted segmentation/semi-supervised learning.
- CLIP is explained as global image-text contrastive alignment, useful for representation but not directly pixel-level segmentation.
- ViLT is explained as a lower-cost way to fuse image tokens and text tokens in one Transformer.
- VLT/LAVT are explained as referring segmentation methods where language acts as a query for the target region.
- ConVIRT and GLoRIA are explained as medical image-report representation learning methods, with GLoRIA adding more local alignment.
- The section emphasizes the gap between image-text representation learning and producing a sharp segmentation mask.
- A comparison table `tab:vl-related-works` was added with shared criteria: role of text, alignment level, contribution, and limitation/gap for LViT.
- The section concludes that LViT is different because text annotation directly participates in the segmentation network and in LV loss for semi-supervised learning, not only in pretraining or global matching.

### Section 2.4 Completed Summary

Section 2.4 has been expanded into a self-explanatory discussion of semi-supervised learning and pseudo-labels.

Key ideas now established:

- Semi-supervised learning is motivated by the gap between abundant medical images/text and scarce expert pixel masks.
- The section explicitly defines labeled data `D_l = {(x_i, t_i, y_i)}` and unlabeled data `D_u = {(x_j, t_j)}`.
- It explains that ground truth `y` exists only for labeled samples; unlabeled samples need temporary pseudo-labels.
- Pseudo-label is explained as a model-generated mask for unlabeled data, with the risk that wrong masks become wrong training targets.
- Consistency regularization is explained as requiring stable predictions under non-semantic perturbations.
- Mean Teacher is explained through student updates and EMA teacher targets.
- Error amplification is highlighted as the core danger of pseudo-labeling in medical segmentation.
- DTC is positioned as a representative medical segmentation SSL method using consistency ideas.
- A comparison table `tab:ssl-related-works` was added with shared criteria: extra data, unlabeled supervision mechanism, contribution, and limitation/gap for LViT.
- The section concludes that LViT combines SSL with text annotation through EPI and LV loss: EPI stabilizes pseudo-labels over time, while LV loss makes text useful for unlabeled samples.

### Chapter 2 Structure Update

Chapter 2 has been strengthened using the user's academic outline reference. The chapter now has a clearer survey-style structure instead of only listing method families.

Added before the CNN section:

- A new section on approach taxonomy for medical image segmentation with text.
- It classifies related work into CNN/U-Net, Transformer, hybrid CNN-Transformer, vision-language learning, semi-supervised learning, and LViT.
- It adds a concise taxonomy table mapping each approach to framework stages, summary, and missing piece that motivates LViT.
- It adds a benchmark/evaluation metrics subsection explaining Dice, IoU, precision, recall, and the need to discuss computational cost, not just accuracy.
- It adds a data/challenges subsection covering expert mask cost/subjectivity, text annotation as semantic support rather than a mask replacement, domain shifts between QaTa-COV19 and MosMedData+, and pseudo-label risk.

Added after the related-work comparison table:

- A new final section "Tổng kết và khoảng trống nghiên cứu".
- Gap 1: trade-off between local detail and long-range context.
- Gap 2: medical text is not yet deeply integrated into pixel-level segmentation in many prior works.
- Gap 3: expert masks are scarce and pseudo-labels can amplify errors.
- Gap 4: data quality and cross-domain generalization remain difficult.
- The ending now explicitly leads into Chapter 3 by positioning LViT as a pipeline that connects Double-U, text annotation, PLAM, EPI, and LV loss.

## Chapter 3 Progress

### Section 3.1 Completed Summary

Section 3.1 has been rewritten again to more closely follow the user's morphology/dilation example: start from the mathematical essence, then explain equivalent interpretations, method, step-by-step procedure, pseudocode, and illustration.

- Chapter 3 introduction now restates the overall framework before entering specific LViT modules.
- It explains that Chapter 3 should present each block through principle, method, algorithm, and illustration.
- It explicitly uses the user's morphology/dilation example as a writing analogy: first explain the underlying principle, then the method/formula/steps.
- Section 3.1 now defines the mathematical core as `f_theta(x,t)=y_hat`, with `x` as image, `t` as text annotation, `y` as expert mask when available, and `theta` as all learnable parameters.
- It gives the supervised + semi-supervised objective form: supervised loss on expert masks plus an SSL term for unlabeled image-text pairs.
- It explains three equivalent views: multimodal mapping, feature fusion `F_xt^l = Phi_l(F_x^l,E_t)`, and labeled/unlabeled learning with pseudo-labels.
- It concludes the principle as: CNN preserves local pixel structure, Transformer learns long-range context, text adds semantic guidance, and pseudo-label control helps exploit unlabeled data.
- The method subsection now writes LViT as `y_hat = D({Phi_l(I_l(x),T(t))})`, explains each symbol, and then gives a step-by-step procedure from sample representation to supervised/SSL training.
- The text explicitly states that CNN relies on local pixel assumptions, while attention learns distant context; text is a semantic auxiliary signal, not a replacement for the image or expert mask.
- A pseudocode-style algorithm was added for the overall LViT forward/training loop.
- The illustration subsection explains how to read `fig:lvit-system-overview` and `fig:lvit-arch` together and preempts common misunderstandings about CNN, attention, text branch, and pseudo-labels.

When writing 3.2 onward:

- Keep 3.1 as the global overview.
- Each later section should focus on one block in the already-defined pipeline.
- Avoid starting with source filenames; begin with the conceptual role, then map to source implementation.

### Section 3.2 Completed Summary

Section 3.2 has been rewritten as the processing flow for training and testing, using the same requested structure:

- Principle: separates image/text input, expert ground truth, and pseudo-label. It stresses that ground truth and pseudo-label must not be confused.
- Method: explains supervised learning on `(x,t,y)`, semi-supervised learning on `(x,t)`, and testing on `(x,t)` without parameter updates.
- Algorithm: gives three explicit procedures: supervised training, semi-supervised training, and testing.
- Illustration: describes the two training paths and the test path, while noting that detailed architecture should rely on paper/source figures rather than AI-generated diagrams when exact arrows matter.

Figure decision:

- For complex LViT architecture/fusion arrows, prefer paper/source figures instead of AI-generated diagrams.
- Current paper/source architecture figure in report: `manuscript/figures/lvit_original_architecture.png`.
- Still need a reliable PLAM figure from paper/source if available; do not use a generated PLAM figure unless it is checked carefully against the paper/source.

### Sections 3.3--3.7 Completed Summary

The remaining Chapter 3 method sections have been expanded and rewritten with the requested academic structure: overview, principle, method, algorithm, and illustration.

Section 3.3: Double-U and multi-level Vision Transformer

- Explains the local/global trade-off: CNN preserves local pixel structure, Transformer learns long-range token context.
- Adds self-attention formula `softmax(QK^T/sqrt(d))V`.
- Maps source implementation to `inc`, `down1`--`down4`, `up4`--`up1`, and multi-level `VisionTransformer`.
- Adds a table for LViT ViT levels: feature sizes 224/112/56/28, patch sizes 16/8/4/2, 196 tokens each, embedding dims 64/128/256/512.
- Explains `Reconstruct` as the bridge from token representation back to feature maps.

Section 3.4: Text representation and image-text fusion

- Explains text as semantic auxiliary information, not a substitute for images or expert masks.
- Defines `E_t = T(t)` and `F_xt^l = Phi_l(F_x^l, E_t^l)`.
- Documents source behavior: BERT embedding produces 768-dim text, `text_module4/3/2/1` project 768 -> 512 -> 256 -> 128 -> 64.
- Carefully states that explicit additive text injection in the inspected `Vit.py` is clearest at dim=64 via `x = x + CTBN3(text)`, while text tensors are still computed and passed to multi-level Vision Transformers.

Section 3.5: PLAM

- Explains PLAM as a pixel-level modulation module for skip features.
- Gives average/max channel statistics and modulation formula `Y = M ⊙ X`.
- Documents `pixlevel.py`: conv_avg/conv_max, mean/max over channels, concatenate avg/max/sum, bottleneck, multiply by original feature.
- Notes source defines `conv_sig` but does not use it in forward; therefore describe PLAM as modulation/attention map, not strictly a sigmoid probability gate.

Section 3.6: EPI and LV loss

- Explains the semi-supervised problem for unlabeled `(x,t)`.
- Presents EPI as exponential temporal smoothing: `P^(k)=alpha P^(k-1)+(1-alpha)Y_hat^(k)`, with paper/source context around `alpha=0.99`.
- Explains LV loss as a text-based semantic constraint for unlabeled learning.
- Documents source pattern: `WeightedDiceBCE_unsup` combines Dice, BCE, and `0.1 * LV_loss`.

Section 3.7: Loss functions and metrics

- Defines BCE and Dice loss mathematically.
- Explains why BCE alone can be weak for small foreground and why Dice is aligned with segmentation overlap.
- Maps to source `WeightedBCE`, `WeightedDiceLoss`, `WeightedDiceBCE`, and `WeightedDiceBCE_unsup`.
- Defines Dice and IoU metrics and links them to performance interpretation and computational-cost discussion.

### Chapter 3 Algorithm Formatting Update

All "Giải thuật" subsections in Chapter 3 have been converted from prose/checklist style into formal LaTeX algorithm blocks using `algorithm` + `algpseudocode`.

Pseudo-code blocks now exist for:

- General LViT forward/training step.
- Supervised training step, semi-supervised training step, and inference/evaluation.
- Double-U CNN-ViT forward pass.
- Text encoding and image-text fusion.
- Pixel-Level Attention Module.
- EPI and LV loss for unlabeled samples.
- Loss and metric computation.

The report preamble now loads `algorithm` and `algpseudocode`, renames algorithm captions to "Thuật toán", and uses Vietnamese `Input`/`Output` labels.

## Chapter 4 Progress

Chapter 4 has been rewritten in detail with the requested structure: state the improvement result first, then explain implementation, datasets, experiment setup, ablations, and limitations.

Key content now included:

- Opens with the locked improvement result for QaTaLViT on QaTa-COV19:
  - 25% labels: 82.22 / 73.35
  - 50% labels: 84.03 / 75.62
  - 100% labels: 85.28 / 77.25
- Compares these directly with the ablation baseline:
  - Baseline 25/50/100: 78.42 / 68.43, 80.32 / 70.60, 82.76 / 73.78
  - Gains: +3.80, +3.71, +2.52 Dice.
- Adds source/layout description distinguishing original LViT source from repo improvements.
- Adds dataset/split/evaluation explanation for QaTa-COV19 and MosMedData+.
- Keeps official LViT README results as the method baseline table.
- Adds main QaTa-COV19 ablation table with Baseline, B0, I1--I5, and QaTaLViT.
- Adds text encoder ablation table:
  - B0, I1, BiomedBERT, NoBERT.
- Adds hyperparameter ablation table:
  - lr 1e-3, 1e-4, 3e-4 with batch/effective batch variants.
- Adds MosMedData+ ablation table:
  - initial BiomedBERT, crop-only, student-only/loss cleanup, NoBERT, LightAU.
- Adds a discussion of accuracy, computational trade-off, limitations, and how to interpret threshold-tuned MosMed results.

### Chapter 3 Figure Update

- Section 3.2 now includes generated high-level training and inference flow diagrams.
- Section 3.3 now repeats the original LViT architecture figure at the point where Double-U and multi-level ViT are explained.
- The caption for Section 3.3 explicitly frames CNN as the local-detail branch and Transformer as the long-context branch, so the architecture figure is easier to read in the method flow.
- All remaining Chapter 3 pseudo-code blocks were expanded with detailed Vietnamese comments: Double-U forward, text/LV fusion, PLAM, EPI/LV loss, and loss/metric computation.
- Added generated diagrams for Section 3.4 LV Fusion, Section 3.5 PLAM, and Section 3.6 EPI/LV Loss with captions that explain the role of each module in the LViT flow.

### Chapter 4 Section 4.1 Update

- Rewrote Section 4.1 "Mục đích thử nghiệm" with a stronger experimental framing.
- It now states the locked QaTaLViT gains first, then explains four experiment goals: validating LViT, testing limited-label behavior, ablation analysis, and cross-domain MosMedData+ evaluation.
- Added explicit research questions and a detailed interpretation of the main QaTa-COV19 result table.

### Chapter 4 Section 4.2 Update

- Expanded "Môi trường cài đặt" to explain why hardware/software constraints matter for LViT.
- Added details on GPU/RAM/storage roles, text embedding cache, fixed image size, batch-size limits, and augmentation trade-offs.
- Added a new subsection on experimental control principles: consistent preprocessing, fixed metric convention, locked result configurations, and careful interpretation of MosMedData+ threshold/crop sensitivity.

### Chapter 4 Section 4.3 Update

### Chapter 4 Section 4.4 Overview and Setup Update

- Added a new overview at the beginning of "Quy trình thử nghiệm" explaining what experiments are performed and which unknowns they answer.
- Added an experiment-question table covering: LViT baseline, label ratios, text encoder, pseudo-label/loss, and cross-domain CT evaluation.
- Added a detailed original LViT setup table:
  - image size 224x224, 3 channels, 1 binary mask output,
  - Double-U/CNN base channel 64,
  - CTrans patch sizes [16, 8, 4, 2], 4 heads, 4 layers, MLP expand ratio 4,
  - Dice+BCE loss, Adam, batch size 16, seed 666,
  - COVID learning-rate note 3e-4 and cosine warm restart.
- Added a detailed improved experiment setup table:
  - 120 epochs, batch size 4, grad accumulation 4, effective batch 16,
  - AdamW, lr 1e-4, min lr 1e-6, weight decay 1e-4,
  - EMA 0.99, BiomedBERT 768-dim text embedding, max 10 text units,
  - label ratios 25%, 50%, 100%, threshold 0.5 by default.
- Added a generated Dice/IoU comparison figure to the shared evaluation-metrics subsection, with an explanation of intersection, union, and why IoU is stricter than Dice.

### Additional EDA Scripts

- Added `scripts/eda_mask_geometry.py`.
  - Computes mask area ratio, average image, average mask heatmap, centroid distribution, connected components, and mask area by text laterality.
  - Exports a PNG figure, per-sample CSV, and JSON summary.
- Added `scripts/eda_text_mask_alignment.py`.
  - Parses structured LViT text fields and compares text laterality/vertical region/infected-area count against mask geometry.
  - Exports laterality/vertical confusion-style heatmaps, agreement rates, boxplots, per-sample CSV, and JSON summary.
- Added `docs/eda_data_scripts.md` with PowerShell commands for QaTa-COV19 and MosMedData+.
- Local search did not find raw QaTa-COV19 or MosMedData+ folders in the current workspace; only the scripts and commands are prepared for when the dataset root is available.

Deep EDA revision:

- Re-expanded Section 4.3 as a deeper EDA section rather than only dataset description.
- The section still focuses only on QaTa-COV19 and MosMedData+ for Chapter 4 experiments.
- QaTa-COV19 now covers X-ray projection challenges, blurry COVID-19 lesion boundaries, foreground/background imbalance, pseudo-label risk in low-label settings, structured location text, and why prompt normalization / text encoder ablations are motivated.
- MosMedData+ now covers CT slice behavior, multi-source composition, crop/threshold sensitivity, small fragmented masks, weaker text-to-slice alignment, and why crop-only / student-only / loss cleanup / LightAU / NoBERT ablations are motivated.
- Added repeated visual evidence in Chapter 4: dataset examples, MosMedData+ source composition, and text EDA figures.
- Added an EDA-to-experiment table mapping observations to risks and corresponding experiment choices.

- Rewrote "Mô tả tập dữ liệu" to focus only on QaTa-COV19 and MosMedData+ for experiments.
- Added a dataset summary table with image domain, Train/Val/Test counts, ground truth, and experimental role.
- Expanded each dataset with overview, role in experiments, image characteristics, ground truth/labeling, text annotation, and dataset-specific challenges.

### Chapter 4 Section 4.3 Quantitative EDA Update

- Re-downloaded the clean LViT-style dataset package and ran the new EDA scripts on QaTa-COV19 and MosMedData+.
- Added four quantitative EDA figures into Section 4.3:
  - QaTa-COV19 mask geometry EDA.
  - QaTa-COV19 text-mask alignment EDA.
  - MosMedData+ mask geometry EDA.
  - MosMedData+ text-mask alignment EDA.
- Added numeric QaTa-COV19 insights:
  - 9258/9258 masks are non-empty.
  - Median mask area is 10.15% of the image; mean is 12.10%.
  - Only 3.75% of samples have mask area below 1%.
  - Median connected components is 2; 6667/9258 masks have exactly two components.
  - Text laterality matches mask laterality at 95.68%.
  - Text infected-area count correlates with mask component count at 0.911.
- Added numeric MosMedData+ insights:
  - 2728/2729 masks are non-empty.
  - Median mask area is 0.758% of the image; mean is 1.54%.
  - 58.54% of samples have mask area below 1%.
  - Median connected components is 3; 95th percentile is 17.
  - Text-mask joint laterality/vertical match is 56.98%.
  - Text infected-area count correlates with mask component count at 0.442.
- Updated the EDA-to-experiment decision table so each row is backed by quantitative findings rather than only qualitative observations.

### Chapter 3 Dice/IoU Figure Update

- Reused the generated Dice/IoU comparison figure inside Chapter 3, immediately after the inference/evaluation pseudo code.
- Added explanation that Dice emphasizes overlap and is useful for small lesions, while IoU is stricter because it normalizes by the union and penalizes broad false positives more strongly.
- Kept the Chapter 4 metric discussion figure as well, so the metric is introduced in the method chapter and revisited in the experiment chapter.

### Chapter 4 Section 4.5 LViT Baseline Output Analysis

- Inspected the provided LViT 25% label output archive for QaTa-COV19.
- Extracted lightweight run artifacts:
  - metrics report,
  - epoch training metrics,
  - labeled subset metadata,
  - pseudo-label vs ground-truth holdout report,
  - validation prediction/ground-truth visualization artifacts.
- Added three generated figures:
  - `lvit_baseline_25pct_training_curves.png`,
  - `lvit_baseline_25pct_pseudo_holdout.png`,
  - `lvit_baseline_25pct_val_artifacts.png`.
- Rewrote the QaTa-COV19 result flow in Section 4.5:
  - first analyze the rerun LViT baseline,
  - then present QaTaLViT improvements,
  - then compare baseline and improved results across metric, learning behavior, pseudo-label quality, and visual artifacts.
- Added rerun baseline numbers:
  - Train: 78.45 Dice / 68.01 IoU.
  - Validation: 76.49 Dice / 65.61 IoU.
  - Test: 78.42 Dice / 68.43 IoU.
  - Best validation epoch: 79, validation Dice 0.7650, validation IoU 0.6554.
  - Pseudo-label holdout: pixel Dice 0.8489, pixel IoU 0.7374, mean-sample Dice 0.7719, mean-sample IoU 0.6655.

### Chapter 4 Section 4.5 LViT Baseline 50% Output Analysis

- Inspected the provided LViT 50% label output archive for QaTa-COV19.
- Extracted the same artifact types as the 25% run: metrics report, epoch metrics, labeled subset metadata, pseudo-label holdout report, and validation GT/prediction visualizations.
- Added three generated figures:
  - `lvit_baseline_50pct_training_curves.png`,
  - `lvit_baseline_50pct_pseudo_holdout.png`,
  - `lvit_baseline_50pct_val_artifacts.png`.
- Updated the rerun baseline table to include both 25% and 50% labels.
- Added baseline 50% numbers:
  - Train: 81.47 Dice / 71.46 IoU.
  - Validation: 79.11 Dice / 68.48 IoU.
  - Test: 80.32 Dice / 70.60 IoU.
  - Best validation epoch: 69, validation Dice 0.7938, validation IoU 0.6881.
  - Pseudo-label holdout: pixel Dice 0.8583, pixel IoU 0.7517, mean-sample Dice 0.7923, mean-sample IoU 0.6879.
- Revised the baseline-vs-QaTaLViT artifact comparison so the baseline column covers both 25% and 50% runs.
- Regenerated the 25% and 50% validation artifact contact sheets with ASCII-only in-image labels (`GT`, `Pred`, `Sample`) to avoid Vietnamese font/encoding rendering errors; Vietnamese interpretation remains in the report captions and body text.
- Regenerated all remaining Section 4.5 baseline figures with ASCII/English-only in-image text, including training curves and pseudo-label holdout charts, to avoid font/encoding issues in the rendered PDF.

### Chapter 4 Section 4.5 LViT Baseline 100% Output Analysis

- Inspected the provided `output_QaTa-Covid19` archive and identified it as the LViT baseline 100% label run.
- Extracted metrics:
  - Train: 86.58 Dice / 77.88 IoU.
  - Validation: 81.21 Dice / 71.24 IoU.
  - Test: 82.76 Dice / 73.78 IoU.
- Added `lvit_baseline_100pct_val_artifacts.png` as the validation GT/prediction contact sheet with ASCII-only in-image labels.
- Updated the baseline rerun table and baseline-vs-QaTaLViT artifact comparison to cover 25%, 50%, and 100% label settings.

### QaTaLViT Metric Verification

- Inspected the three provided QaTaLViT metric archives for 25%, 50%, and 100% label settings.
- The archives were used for cross-checking, but the report keeps the previously selected best-model numbers from the earlier report/results:
  - 25% test: 82.22 Dice / 73.35 IoU.
  - 50% test: 84.03 Dice / 75.62 IoU.
  - 100% test: 85.28 Dice / 77.25 IoU.
- Reverted the Chapter 4 overview table, ablation table, artifact comparison table, text encoder table, and locked recipe line to the report-chosen numbers.
- Added corresponding QaTaLViT analysis artifacts to Section 4.5:
  - `qatalvit_training_artifacts.png` for training/validation Dice and loss curves across 25%, 50%, and 100%.
  - `qatalvit_pseudo_holdout.png` for pseudo-label holdout quality at 25% and 50%.
- Added explanatory text that these artifacts illustrate training behavior and pseudo-label quality, while the final result table remains based on the report-selected best-model numbers.

### Float Placement Cleanup

- Added `\FloatBarrier` boundaries around the dense Chapter 4.5 result blocks so baseline figures/tables, QaTaLViT artifacts, comparison tables, text ablations, and hyperparameter ablations do not drift into the following subsection.
- Changed the main Chapter 4 result tables in this region from top-floating forms to `[H]` placement where appropriate.

### MosMedData+ Improved Artifact Analysis

- Inspected the three provided MosMedData+ improved archives for 25%, 50%, and 100% label settings.
- Extracted lightweight run artifacts only: metrics reports, epoch metrics, threshold diagnostics, source-level diagnostics, pseudo-label holdout reports, labeled-subset metadata, logs, and a small validation visualization sample.
- Aggregated `test_threshold_diagnostics.csv` by threshold to obtain the final operating-point metrics used in the report:
  - 25% labels: 65.50 Dice / 51.32 IoU.
  - 50% labels: 73.84 Dice / 60.31 IoU.
  - 100% labels: 73.60 Dice / 60.12 IoU.
- Added MosMedData+ report figures with ASCII-only in-image labels:
  - `mosmed_improved_scores.png`,
  - `mosmed_improved_threshold_curves.png`,
  - `mosmed_improved_pseudo_holdout.png`,
  - `mosmed_improved_source_behavior.png`,
  - `mosmed_improved_val_artifacts.png`.
- Updated Chapter 4 MosMedData+ result text so it presents the final method and artifact analysis without discussing test-threshold selection details.
- Removed report wording such as `test tuned`, `diagnostic best`, and `test diagnostic threshold` from the MosMedData+ result discussion.
- Updated the MosMedData+ Kaggle submission script/notebook so the final test evaluation uses a fixed `final_test_threshold = 0.55` for the 50% submitted run, while diagnostics can still be exported separately.

### Clarified Experiment Plan and Ablation Naming

- Expanded Chapter 4 experiment planning so QaTaLViT is introduced as a concrete improved model rather than a vague name.
- Added a module summary table for QaTaLViT covering prompt normalization, text encoder, cross-modal fusion, spatial prior/skip adapter, pseudo-label control, and training recipe.
- Added an ablation legend before the QaTa-COV19 ablation table explaining Baseline, B0, I1, I2, I3, I4, I5, and final QaTaLViT in terms of what changes from the previously described model.
- Rewrote the MosMedData+ configuration table and discussion to explain crop-only, student-only, loss cleanup, LightAU, BiomedBERT, and NoBERT in plain terms.
- Rebuilt `manuscript/main.pdf` successfully with XeLaTeX.

### Chapter 4 Conclusion Rewrite

- Rewrote the Chapter 4 conclusion so it summarizes the whole experiment chapter rather than only closing with a generic sentence.
- Added a compact summary table for the key QaTa-COV19 and MosMedData+ results:
  - QaTa-COV19 25%, 50%, 100% baseline vs QaTaLViT with absolute and relative improvements.
  - MosMedData+ 50% improved recipe compared with U-Net and LViT-T references.
- Added sharper interpretation:
  - The largest gains appear under limited labels.
  - IoU gains show better overlap, not only smoother masks.
  - Gains shrink at 100% labels, so text/pseudo-label help most when labels are scarce.
  - MosMedData+ exposes CT-domain limits: small fragmented masks, multi-source shift, threshold sensitivity.
- Added concise advantages and limitations of the proposed improvements.
- Rebuilt `manuscript/main.pdf` successfully with XeLaTeX.

### MosMedData+ 50% Reference Correction

- Corrected the Chapter 4 MosMedData+ comparison so the 50% label row uses the 50% LViT-T reference (`73.56 / 61.05`) instead of the full-label/paper reference (`74.57 / 61.33`).
- Updated the conclusion summary table:
  - Improved recipe: `73.84 / 60.31`.
  - Compared with LViT-T 50%: `+0.28` Dice, `-0.74` IoU.
- Rewrote the limitation sentence to state that the improved MosMed recipe is slightly higher in Dice but lower in IoU, rather than incorrectly saying it is below the official LViT-T benchmark overall.
- Rebuilt `manuscript/main.pdf` successfully.

### Chapter 5 Full Draft

- Replaced the short Chapter 5 text with a full conclusion chapter.
- Added sections:
  - `K?t lu?n chung`,
  - `K?t qu? d?t du?c`,
  - `��ng g�p c?a b�o c�o`,
  - `H?n ch?`,
  - `Hu?ng ph�t tri?n`,
  - `K?t lu?n cu?i`.
- Chapter 5 now summarizes LViT as a multimodal medical segmentation framework, restates the main QaTa-COV19 and MosMedData+ results, explains what the report contributed, and gives detailed but concise limitations/future directions.
- Rebuilt `manuscript/main.pdf` successfully; current PDF has 84 pages.

### Chapter 5 Template-Aligned Expansion

- Adapted Chapter 5 to follow the suggested conclusion/future-work template while keeping the content specific to LViT.
- Kept the core sections: `K?t lu?n`, `H?n ch?`, `Hu?ng ph�t tri?n`.
- Added an extended future-work block analogous to the self-supervised-learning template:
  - `�?ng l?c v� b?i c?nh c?a hu?ng m? r?ng t? gi�m s�t`,
  - `Kh�i ni?m co b?n`,
  - `C�c nh�m phuong ph�p t? gi�m s�t ph� h?p v?i LViT`,
  - `Li�n h? v?i b�i to�n LViT`,
  - `R?i ro v� h?n ch? c?a t? gi�m s�t trong b�i to�n n�y`,
  - `�? xu?t th?c nghi?m m? r?ng`.
- The new sections discuss masked image modeling, image contrastive learning, image-text contrastive learning, pseudo-mask/region-level pretraining, and how they could extend LViT/QaTaLViT.
- Rebuilt `manuscript/main.pdf` successfully; current PDF has 87 pages.

### Chapter 2 Related Works Reorganization

- Reworked Chapter 2 to better follow the suggested related-works framework:
  - approach taxonomy,
  - benchmark and evaluation metrics,
  - human/computational attention,
  - data and ground-truth challenges,
  - state-of-the-art method groups,
  - summary comparison and research gaps.
- Added the local taxonomy figure `manuscript/figures/related_taxonomy_lvit.png` with English in-image labels and Vietnamese report caption.
- Added a compact SOTA quick-map table covering U-Net, nnU-Net, TransUNet, Swin-Unet, ConVIRT/GLoRIA, Mean Teacher/DTC, and LViT.
- Adjusted Chapter 2 heading levels so CNN/U-Net, Transformer/hybrid, vision-language, and semi-supervised learning are all subsections under `State-of-the-Art Methods`.
- Added `\FloatBarrier` after dense Chapter 2 tables to keep floats from drifting across sections.
- Rebuilt `manuscript/main.pdf` successfully with XeLaTeX; current PDF has 89 pages.
### Float Barriers, Lists, and English-Term Review

- Added `\listoffigures` and `\listoftables` immediately after the table of contents in `manuscript/info.tex`.
- Removed the Chapter 2 subsection `Human attention v� computational attention` because it could distract from the LViT-related workflow and be misread as a separate research direction.
- Inserted `\FloatBarrier` immediately after every `table`/`table*` environment in `manuscript/sections/content_main.tex`; verified 28 table starts and 28 table ends, with all table ends followed by a barrier.
- Generated `manuscript/english_terms_scan.txt` as a raw scan of common English technical terms in the report.
- Added `manuscript/english_translation_review.md` with proposed Vietnamese replacements and a separate translation map for the English labels in `related_taxonomy_lvit.png`.
- Rebuilt `manuscript/main.pdf` successfully with XeLaTeX; current PDF has 92 pages.