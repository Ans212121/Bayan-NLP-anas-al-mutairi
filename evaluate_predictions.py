"""Evaluate exported real predictions; stdlib only. Group bootstrap keeps pairs together."""
import csv
import hashlib
import json
from pathlib import Path
import random
import sys

def macro_f1(rows, key, labels):
    scores=[]
    for label in labels:
        tp=sum(r['label']==label and r[key]==label for r in rows)
        fp=sum(r['label']!=label and r[key]==label for r in rows)
        fn=sum(r['label']==label and r[key]!=label for r in rows)
        scores.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.0)
    return sum(scores)/len(scores)

def percentile(values,p):
    values=sorted(values); index=(len(values)-1)*p
    lo=int(index); hi=min(lo+1,len(values)-1)
    return values[lo]+(values[hi]-values[lo])*(index-lo)

def validate(rows):
    required={'example_id','group_id','split','language','text','label','prediction_a','prediction_b','confidence','task','preprocessing_version'}
    if not rows: raise ValueError('empty predictions')
    ids=set(); owners={}
    for r in rows:
        if not required <= r.keys(): raise ValueError(f'missing fields: {required-r.keys()}')
        if r['example_id'] in ids: raise ValueError('duplicate example ID')
        ids.add(r['example_id'])
        if r['split'] not in {'validation','test'}: raise ValueError('expected validation/test only')
        if owners.setdefault(r['group_id'],r['split']) != r['split']: raise ValueError('group leakage')
        if not 0 <= r['confidence'] <= 1: raise ValueError('invalid confidence')
    if len({r['task'] for r in rows})!=1 or len({r['preprocessing_version'] for r in rows})!=1:
        raise ValueError('mixed task or preprocessing version')

def interval(rows,labels,n_boot=1000):
    groups={}
    for r in rows: groups.setdefault(r['group_id'],[]).append(r)
    keys=sorted(groups); rng=random.Random(42); scores=[]; deltas=[]
    for _ in range(n_boot):
        sample=[r for k in rng.choices(keys,k=len(keys)) for r in groups[k]]
        a=macro_f1(sample,'prediction_a',labels); b=macro_f1(sample,'prediction_b',labels)
        scores.append(b); deltas.append(b-a)
    return {'n':len(rows),'groups':len(keys),'small_slice':len(rows)<15,
        'baseline_macro_f1':macro_f1(rows,'prediction_a',labels),
        'model_macro_f1':macro_f1(rows,'prediction_b',labels),
        'model_ci95':[percentile(scores,.025),percentile(scores,.975)],
        'paired_delta_ci95':[percentile(deltas,.025),percentile(deltas,.975)],
        'n_boot':n_boot,'method':'group bootstrap, fixed label vocabulary; exploratory small-sample interval'}

def main(path):
    path=Path(path); rows=json.loads(path.read_text(encoding='utf-8')); validate(rows)
    labels=sorted({r[k] for r in rows for k in ('label','prediction_a','prediction_b')})
    result={'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'data_kind':'MEASURED_SMOKE',
        'note':'New run of course sample; not COURSE_FIXTURE and not a production estimate.',
        'labels':labels,'task':rows[0]['task'],'splits':{}}
    for split in ('validation','test'):
        subset=[r for r in rows if r['split']==split]
        if not subset: raise ValueError(f'missing {split}')
        groups={'ALL':subset}
        for language in sorted({r['language'] for r in subset}):
            groups[f'language={language}']=[r for r in subset if r['language']==language]
        # Word count, not subword length. The boundary is fixed before evaluation.
        for name,predicate in [('short_le_10_words',lambda r:len(r['text'].split())<=10),('long_gt_10_words',lambda r:len(r['text'].split())>10)]:
            selected=[r for r in subset if predicate(r)]
            if selected: groups[name]=selected
        result['splits'][split]={name:interval(group,labels) for name,group in groups.items()}
    report=path.with_name(path.stem.replace('_predictions','')+'_actual_evaluation.json')
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    errors=path.with_name(path.stem.replace('_predictions','')+'_error_candidates.csv')
    with errors.open('w',encoding='utf-8',newline='') as f:
        fields=['example_id','split','language','text','label','prediction_b','taxonomy_tag','rationale']
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader()
        for row in rows:
            if row['label']!=row['prediction_b']:
                writer.writerow({k:row.get(k,'') for k in fields})
    print(report); print(errors)

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('Usage: python scripts/evaluate_predictions.py reports/topic_predictions.json')
    main(sys.argv[1])
