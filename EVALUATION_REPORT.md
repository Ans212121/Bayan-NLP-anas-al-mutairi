# EVALUATION REPORT

## Scope
This report summarises the evaluation and error-analysis evidence recorded in the Bayan notebook.

## Classification
- Baseline validation Macro-F1: 0.6667
- Transformer validation Macro-F1: 1.0000
- Baseline test Macro-F1: 0.7333
- Transformer test Macro-F1: 0.8667
- Transformer test accuracy: 0.875

## NER
- Recall: 0.5000
- F1: 0.5714
- Final training loss after 12 epochs: 0.0427
- Strict entity-boundary test: PASS

## QA
- Recorded QA loss: 3.6451
- Offset-to-token conversion: PASS
- Valid span extraction: PASS
- Honest no-answer handling: PASS

## Semantic Search
- Recall@3: 1.0000
- MRR@3 before re-ranking: 0.6667
- MRR@3 after re-ranking: 0.7222
- Validation-only threshold: 0.4592
- Validation accuracy: 1.0000
- Frozen-threshold no-answer test accuracy: 1.0000

## Slices and Uncertainty
The notebook evaluates language, variant, retrieval-mode, and length-related slices and explicitly flags small slices. Confidence intervals and a paired comparison are included.

## Behavioural Evaluation
Course-fixture behavioural tests:
- Passed: 3
- Total: 6
- Pass rate: 0.5000

## Error Taxonomy
Observed categories include:
- dialect gap
- hard/ambiguous cases
- class confusion

## Prioritised Fixes
The notebook records three ranked fixes, including better Gulf-dialect coverage and resolving class-confusion patterns. These should guide the next iteration rather than claiming perfect generalisation.

## Evidence
- `DAY3_NOTEBOOK7_CORE=PASS`
- Generated reports recorded by the notebook:
  - `day3_error_taxonomy.csv`
  - `day3_evaluation_fixture.json`
  - `day3_slice_report.csv`
