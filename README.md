# Bayan NLP Project

**Name:** Anas Ibrahim Al-Mutairi  
**Program:** Applied Natural Language Processing  
**Project Name:** Bayan  
**Instructor**/**اMeaad Al-Marri**

https://github.com/SDAIAAcademy

## Project Overview

**Bayan** is an applied Natural Language Processing project that brings together the full practical workflow covered in the training program: text preparation, tokenisation, Transformer attention, text classification, Named Entity Recognition (NER), Extractive Question Answering (QA), bilingual semantic search, evaluation/error analysis, and inference optimisation/serving.

The repository is centered around one complete Google Colab notebook containing the practical implementation and recorded outputs:

`notebooks/bayan_NLP_ANAS_AI_Mutairi.ipynb`

> **Important:** The results reported below are the actual values recorded in the submitted notebook. Several course experiments are explicitly labelled as measured smoke tests / course fixtures and should not be interpreted as production-scale benchmarks.

---

## Technical Coverage

### T1 — Text Preparation and Arabic Handling
Implemented and validated:
- Unicode inspection
- Raw-text preservation
- PII masking for email and Saudi mobile examples
- spaCy sentence segmentation
- WordPiece tokenisation
- Token fertility and truncation checks
- Padding, attention masks, and embeddings
- Arabic/multilingual tooling, including `camel-tools==1.6.0`

Validation:
- `DAY1_NOTEBOOK1_CORE=PASS`
- `unicode: PASS`
- `spacy_sentence_pipeline: PASS`
- `raw_copy_preserved: PASS`
- `pii_masked: PASS`
- `token_metrics: PASS`
- `embedding_shape: PASS`

### T2 — Attention and Transformer Architecture
Implemented and validated:
- Scaled Dot-Product Attention
- Q/K/V shape checks
- Causal masking
- Multi-head split/combine journey
- NumPy ↔ PyTorch parity
- Actual Transformer forward pass and attention inspection
- Two-checkpoint parameter audit

Validation:
- `Scaled attention=PASS`
- `Mask semantics=PASS`
- `Multi-head shape journey=PASS`
- `NumPy/PyTorch parity=PASS`
- `ACTUAL_TRANSFORMER_FORWARD=PASS`
- `DAY1_NOTEBOOK2_CORE=PASS`

Actual Transformer example:
- Parameters: **134,734,080**
- Hidden-state shape: **(2, 10, 768)**

### T3 — Classification, NER and QA

#### Text Classification
Measured results:
- Baseline validation Macro-F1: **0.6667**
- Transformer validation Macro-F1: **1.0000**
- Baseline test Macro-F1: **0.7333**
- Transformer test Macro-F1: **0.8667**
- Transformer test accuracy: **0.875**
- Selected epoch: **9**
- Transformer optimizer steps: **72**

Validation:
- `DAY2_NOTEBOOK3_CORE=PASS`

#### Named Entity Recognition (NER)
Training loss decreased from **2.2637** to **0.0427** across 12 epochs.

Measured NER metrics:
- Recall: **0.5000**
- F1: **0.5714**

Validation:
- `NER alignment contract=PASS`
- `Strict entity-boundary test=PASS`
- `NER optimizer steps=PASS`

#### Extractive QA
Measured QA loss:
- **3.6451**

Validated:
- offset-to-token alignment
- valid span extraction
- honest no-answer handling

Validation:
- `QA offsets-to-token positions=PASS`
- `QA optimizer steps=PASS`
- `QA post-processing tests=PASS`
- `DAY2_NOTEBOOK4_CORE=PASS`

### T4 — Bilingual Semantic Search
Implemented:
- Multilingual sentence embeddings
- L2 normalisation
- FAISS index
- Validation-only threshold selection
- Cross-lingual retrieval
- Re-ranking experiment

Measured retrieval results:
- Recall@3: **1.0000**
- MRR@3 before re-ranking: **0.6667**
- MRR@3 after re-ranking: **0.7222**
- MRR@3 delta: **+0.0556**
- Validation-only threshold: **0.4592**
- Validation accuracy at selected threshold: **1.0000**
- Frozen-threshold no-answer test accuracy: **1.0000**

Decision:
- **ADOPT_FOR_EXPERIMENT** for re-ranking

Validation:
- `DAY3_NOTEBOOK6_CORE=PASS`

### T5 — Evaluation and Error Analysis
Implemented:
- validation-only evaluation
- slice-based analysis
- confidence intervals
- paired comparison
- small-slice flags
- behavioural tests
- manual error taxonomy
- three prioritised fixes
- traceable report generation

Course-fixture behavioural tests:
- Passed: **3 / 6**
- Pass rate: **0.5000**

Generated evaluation artifacts include:
- `day3_error_taxonomy.csv`
- `day3_evaluation_fixture.json`
- `day3_slice_report.csv`

Validation:
- `DAY3_NOTEBOOK7_CORE=PASS`

### T6 — Inference Optimisation and Tested Service
Implemented:
- PyTorch reference benchmark
- ONNX export and checker
- ONNX numerical parity
- dynamic INT8 quantisation attempt
- latency and quality budgets
- FastAPI contract tests
- Arabic/English service canaries
- invalid-input rejection

Measured optimisation results:
- PyTorch parameter size: **16.732 MiB**
- ONNX FP32 size: **16.788 MiB**
- INT8 size: **4.287 MiB**
- ONNX FP32 prediction agreement: **1.0000**
- ONNX max absolute logits difference: **1.639e-07**
- INT8 prediction agreement: **1.0000**
- ONNX FP32 model-only p95 latency: **9.541 ms**
- INT8 model-only p95 latency: **7.922 ms**

Selected service candidate:
- **onnx-dynamic-int8**
- Decision recorded by the notebook: **ADOPT_INT8**
- Scope note: **SYSTEMS_SMOKE_NOT_A_SHIP_DECISION**

FastAPI tests:
- health: **200**
- Arabic request: **200**
- English request: **200**
- empty input rejected: **422**
- unsupported language rejected: **422**
- Arabic canary: **PASS**
- English canary: **PASS**

Validation:
- `DAY4_NOTEBOOK8_CORE=PASS`

### T7 — Measured Extension
A measured re-ranking extension was evaluated on the semantic-search pipeline:
- MRR@3 before: **0.6667**
- MRR@3 after: **0.7222**
- Improvement: **+0.0556**
- Decision: **ADOPT_FOR_EXPERIMENT**

This provides an explicit measured benefit/cost decision rather than an unmeasured feature addition.

---

## Core Notebook Validation Summary

```text
DAY1_NOTEBOOK1_CORE=PASS
DAY1_NOTEBOOK2_CORE=PASS
DAY2_NOTEBOOK3_CORE=PASS
DAY2_NOTEBOOK4_CORE=PASS
DAY3_NOTEBOOK6_CORE=PASS
DAY3_NOTEBOOK7_CORE=PASS
DAY4_NOTEBOOK8_CORE=PASS
```

---

## Key Technologies

- Python
- Google Colab / Jupyter
- NumPy
- spaCy
- Hugging Face Transformers
- Tokenizers
- PyTorch
- Scikit-learn
- CAMeL Tools
- Sentence Transformers
- FAISS
- ONNX
- ONNX Runtime
- FastAPI
- Matplotlib

---

## Repository Structure

```text
Bayan-NLP-Project/
├── README.md
├── DECISIONS.md
├── BENCHMARKS.md
├── PROJECT_SUMMARY.json
├── requirements.txt
├── notebooks/
│   └── bayan_NLP_ANAS_AI_Mutairi.ipynb
├── reports/
│   └── EVALUATION_REPORT.md
└── tests/
    └── README.md
```

The complete implementation is intentionally preserved in the notebook above so the code, execution history, plots, metrics, and PASS evidence can be reviewed in one place.

---

## Generated Runtime Artifacts

The notebook records creation/checks for runtime artifacts such as:

- `day2_classification_metrics.json`
- `day2_ner_qa_metrics.json`
- `runtime_report.json`
- `reports/search_manifest.json`
- `reports/retrieval_metrics.json`
- `reports/day3_error_taxonomy.csv`
- `reports/day3_evaluation_fixture.json`
- `reports/day3_slice_report.csv`
- `reports/benchmark_results.json`
- `reports/service_smoke.json`
- `reports/BENCHMARKS_DRAFT.md`

Large model weights, model caches, `.faiss` indexes, and large ONNX artifacts should remain outside the GitHub repository unless the course explicitly requires them.

---

## How to Run

1. Open `notebooks/bayan_NLP_ANAS_AI_Mutairi.ipynb` in Google Colab.
2. Use a current Python 3.11+ runtime.
3. Run cells in order.
4. Allow the notebook to install the pinned dependencies when required.
5. For Transformer/ONNX sections, internet access may be required the first time models are downloaded.
6. Confirm the final `*_CORE=PASS` checks for each notebook section.
7. Save the generated small reports required for submission.

---

## Reproducibility and Evaluation Notes

- Fixed seeds are used where applicable.
- Validation-only threshold tuning is used before test evaluation in semantic search.
- Group/split isolation checks are included in classification.
- Evaluation includes small-slice warnings and uncertainty reporting.
- Optimisation decisions include both latency and quality/parity checks.
- Smoke-test/course-fixture results are labelled honestly and are not presented as production certification.

---

## Supporting Documentation

- `DECISIONS.md` — important technical decisions and evidence
- `EVALUATION_REPORT.md` — evaluation/error-analysis summary
- `BENCHMARKS.md` — optimisation and serving benchmark summary
- `PROJECT_SUMMARY.json` — machine-readable project summary
- `requirements.txt` — main dependencies used by the notebook

---

## Certificate

**Program:** Applied Natural Language Processing  
**Participant:** Anas Ibrahim Al-Mutairi  
**Project:** Bayan  

> Add the final program certificate image/PDF here after it is issued, or link to it from a `docs/` folder.

---

## Author

**Anas Ibrahim Al-Mutairi**  
Applied Natural Language Processing  
Project: **Bayan**
