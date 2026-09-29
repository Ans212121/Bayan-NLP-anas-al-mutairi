"""Run immediately after original cell 71 (or 86), in that same notebook kernel.
Example notebook cell: %run scripts/export_retrieval.py
IPython %run -i is REQUIRED to use the current notebook variables:
    %run -i scripts/export_retrieval.py
"""
from pathlib import Path
import json

required={'test_rankings','validation_rankings','rerank_report','reranked_test'}
missing=required-set(globals())
if missing:
    raise RuntimeError('Run with %run -i immediately after the retrieval reranking cell. Missing: '+str(sorted(missing)))

def correct_metrics(rankings,k=3):
    answerable=[r for r in rankings if r['relevant_case_ids']]
    if not answerable: raise ValueError('no answerable queries')
    recalls=[]; hits=[]; reciprocal=[]
    for r in answerable:
        relevant=set(r['relevant_case_ids']); top=r['ranked_case_ids'][:k]
        recalls.append(len(set(top)&relevant)/len(relevant))
        hits.append(float(bool(set(top)&relevant)))
        rank=next((i for i,v in enumerate(top,1) if v in relevant),None)
        reciprocal.append(1/rank if rank else 0)
    return {'answerable_n':len(answerable),'set_recall_at_3':sum(recalls)/len(recalls),
        'hit_rate_at_3':sum(hits)/len(hits),'mrr_at_3':sum(reciprocal)/len(reciprocal)}

report={'status':'MEASURED_SMOKE','source':'current live notebook variables; new export, not recovered old outputs',
    'validation_rankings':validation_rankings,'test_rankings':test_rankings,
    'test_metrics':correct_metrics(test_rankings),'reranking':rerank_report,'reranked_rows':reranked_test}
target=Path('reports/retrieval_full_export.json'); target.parent.mkdir(exist_ok=True)
target.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(target)
