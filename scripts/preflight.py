"""Local packaging checks, not the course's official preflight/schema validator."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
required=['README.md','DECISIONS.md','EVALUATION_REPORT.md','BENCHMARKS.md','PROJECT_SUMMARY.json','AUDIT_T1_T7_AR.md','notebooks/original_bayan.ipynb']
summary=json.loads((ROOT/'PROJECT_SUMMARY.json').read_text(encoding='utf-8'))
checks={p:(ROOT/p).is_file() for p in required}
checks['source_hash_matches']=hashlib.sha256((ROOT/'notebooks/original_bayan.ipynb').read_bytes()).hexdigest()==summary['source_sha256']
errors=[]
for path in ROOT.rglob('*.json'):
    try: json.loads(path.read_text(encoding='utf-8'))
    except (ValueError,UnicodeError) as exc: errors.append({'path':str(path.relative_to(ROOT)),'error':str(exc)})
checks['json_parses']=not errors
result=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
checks['local_contract_tests']=result.returncode==0
report={'validator':'local-package-preflight/1.0','official_course_schema_validated':False,
    'checks':checks,'package_checks_pass':all(checks.values()),'submission_ready':False,
    'notebook_models_rerun_by_packager':False,'json_errors':errors,
    'tests_output':result.stdout+result.stderr,'pending':summary['pending'],
    'note':'Model reports require real runs and review. Passing packaging checks does not award rubric points.'}
(ROOT/'reports'/'preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['package_checks_pass','submission_ready','official_course_schema_validated']},indent=2))
raise SystemExit(0 if report['package_checks_pass'] else 1)
