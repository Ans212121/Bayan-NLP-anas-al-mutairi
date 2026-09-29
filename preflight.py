"""Local repository preflight for the Bayan NLP submission.

This checks the current repository structure and writes reports/preflight.json.
It is a local project check, not the course's official schema validator.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

required_paths = [
    "README.md",
    "DECISIONS.md",
    "BENCHMARKS.md",
    "PROJECT_SUMMARY.json",
    "requirements.txt",
    "notebooks/bayan_NLP_ANAS_AI_Mutairi.ipynb",
    "reports/EVALUATION_REPORT.md",
    "reports/preflight.json",
    "tests/test_contracts.py",
]

checks = {path: (ROOT / path).exists() for path in required_paths}

json_files = [
    ROOT / "PROJECT_SUMMARY.json",
    ROOT / "reports" / "preflight.json",
]
json_errors = []
for path in json_files:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError, OSError) as exc:
        json_errors.append({"file": str(path.relative_to(ROOT)), "error": str(exc)})

checks["json_parses"] = not json_errors
checks["main_notebook_present"] = (ROOT / "notebooks" / "bayan_NLP_ANAS_AI_Mutairi.ipynb").is_file()
checks["evidence_report_present"] = (ROOT / "reports" / "EVALUATION_REPORT.md").is_file()

report = {
    "validator": "bayan-repository-preflight/1.1",
    "official_course_schema_validated": False,
    "checks": checks,
    "package_checks_pass": all(checks.values()),
    "submission_ready": False,
    "json_errors": json_errors,
    "pending": [
        "Complete A4 versioned final submission and declare final commit SHA",
        "Complete A5 authorship and assistance disclosure in README"
    ],
    "note": (
        "This is a local repository preflight. Final submission readiness remains false "
        "until the remaining administrative requirements are completed."
    ),
}

out = ROOT / "reports" / "preflight.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
