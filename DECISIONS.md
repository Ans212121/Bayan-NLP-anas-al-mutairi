# DECISIONS

## 1. Text Preparation
- Preserve both raw text and model-ready text.
- Mask PII examples such as email and Saudi mobile patterns before model use.
- Validate Unicode handling before aggressive cleaning.

## 2. Tokenisation
- Measure token fertility and truncation instead of assuming a tokenizer is suitable.
- Keep truncation/padding behaviour explicit and test embedding shapes.

## 3. Transformer Attention
- Use scaled dot-product attention and validate row sums.
- Apply causal masks so masked positions receive zero attention.
- Verify NumPy attention against PyTorch for numerical parity.

## 4. Classification
- Keep grouped split isolation to avoid leakage.
- Baseline validation Macro-F1: 0.6667.
- Selected Transformer epoch: 9.
- Selected Transformer validation Macro-F1: 1.0000.
- Transformer test Macro-F1: 0.8667; test accuracy: 0.875.

## 5. NER and QA
- Require strict BIO/subword alignment and boundary checks.
- Validate QA token offsets and no-answer behaviour.
- NER F1 recorded in the notebook: 0.5714.

## 6. Semantic Search
- Use L2-normalised sentence vectors with FAISS.
- Tune the no-answer threshold on validation only.
- Frozen threshold: 0.4592.
- Re-ranking improved MRR@3 from 0.6667 to 0.7222 (+0.0556).
- Decision: ADOPT_FOR_EXPERIMENT.

## 7. Evaluation
- Include slices, sample-size warnings, confidence intervals, paired comparisons, and a manual error taxonomy.
- Behavioural fixture pass rate: 3/6 = 0.50.
- Use the three ranked fixes recorded in the notebook rather than hiding observed failure modes.

## 8. Optimisation and Serving
- Compare PyTorch, ONNX FP32 and dynamic INT8 with quality/parity checks.
- ONNX FP32 prediction agreement: 1.0.
- INT8 prediction agreement: 1.0.
- p95 latency: 9.541 ms (ONNX FP32) vs 7.922 ms (INT8).
- INT8 size: 4.287 MiB.
- Selected candidate: onnx-dynamic-int8.
- Notebook decision: ADOPT_INT8 / SYSTEMS_SMOKE_NOT_A_SHIP_DECISION.
