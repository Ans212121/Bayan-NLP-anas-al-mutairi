# BENCHMARKS

## Scope
Measured optimisation/serving evidence from the Day 4 notebook.

| Candidate | Size | p95 latency | Prediction agreement |
|---|---:|---:|---:|
| PyTorch reference parameters | 16.732 MiB | See notebook end-to-end report | Reference |
| ONNX FP32 | 16.788 MiB | 9.541 ms | 1.0000 |
| Dynamic INT8 | 4.287 MiB | 7.922 ms | 1.0000 |

Additional ONNX FP32 parity:
- max absolute logits difference: `1.639e-07`

## Decision
Selected candidate: **onnx-dynamic-int8**

Notebook decision:
- **ADOPT_INT8**
- **SYSTEMS_SMOKE_NOT_A_SHIP_DECISION**

This is an engineering smoke-test decision, not a production deployment certification.

## Service Contract
FastAPI smoke tests:
- health: 200
- Arabic inference: 200
- English inference: 200
- empty input: rejected with 422
- unsupported language: rejected with 422
- Arabic canary: PASS
- English canary: PASS

## Evidence
- `ONNX_CHECKER=PASS`
- `ONNX_FP32_PARITY=PASS`
- `INT8_ATTEMPT=PASS`
- `FASTAPI_TESTCLIENT=PASS`
- `DAY4_NOTEBOOK8_CORE=PASS`
