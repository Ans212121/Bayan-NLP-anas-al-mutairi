"""New bounded extension: validation-tuned abstention. No pre-filled model results."""
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import time
from evaluate_predictions import validate

def score(rows,threshold):
    kept=[r for r in rows if r['confidence']>=threshold]
    return {'n':len(rows),'accepted':len(kept),'rejected':len(rows)-len(kept),
        'coverage':len(kept)/len(rows),
        'accepted_accuracy':sum(r['prediction_b']==r['label'] for r in kept)/len(kept) if kept else None}

def choose_threshold(validation):
    if not validation or any(r['split']!='validation' for r in validation): raise ValueError('validation-only tuning required')
    candidates=[(score(validation,t),t) for t in sorted({0.0,*[r['confidence'] for r in validation]})]
    candidates=[(s,t) for s,t in candidates if s['coverage']>=.75]
    return max(candidates,key=lambda pair:(pair[0]['accepted_accuracy'],pair[0]['coverage'],-pair[1]))[1]

def main(path):
    path=Path(path); rows=json.loads(path.read_text(encoding='utf-8')); validate(rows)
    if {r['task'] for r in rows}!={'topic'}: raise ValueError('This extension is defined for topic classification')
    validation=[r for r in rows if r['split']=='validation']; test=[r for r in rows if r['split']=='test']
    if not test: raise ValueError('test rows required')
    threshold=choose_threshold(validation)
    timings=[]
    for i in range(35):
        start=time.perf_counter_ns()
        decisions=[r['confidence']>=threshold for r in test]
        elapsed=(time.perf_counter_ns()-start)/1e6
        if i>=5: timings.append(elapsed)
    before=score(test,0.0); after=score(test,threshold)
    benefit=None if after['accepted_accuracy'] is None else after['accepted_accuracy']-before['accepted_accuracy']
    result={'status':'MEASURED_SMOKE','extension':'confidence abstention','source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'threshold':threshold,'selection':'validation only; minimum 75% coverage; highest accepted accuracy then coverage',
        'validation':score(validation,threshold),'test_baseline':before,'test_extension':after,
        'benefit_accepted_accuracy_delta':benefit,'cost_rejection_rate':1-after['coverage'],
        'threshold_check_median_ms':statistics.median(timings),'timing_scope':'threshold comparisons only on full test list; excludes model inference',
        'timing_warmup':5,'timing_repetitions':30,
        'decision':'REVIEW_TRADEOFF' if benefit is not None and benefit>0 else 'NO_OBSERVED_ACCURACY_BENEFIT',
        'limitations':['Small known course test is exploratory','Accepted accuracy changes the evaluated population; report coverage alongside it','Confidence is not calibrated','No proof of latency improvement or production quality']}
    target=path.parent/'extension_results.json'; target.write_text(json.dumps(result,indent=2),encoding='utf-8'); print(target)

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('Usage: python scripts/measure_extension.py reports/topic_predictions.json')
    main(sys.argv[1])
