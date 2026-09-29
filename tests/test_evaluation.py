import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from evaluate_predictions import macro_f1,validate,interval
from measure_extension import choose_threshold,score

def row(i,split='validation',confidence=.9,prediction='a'):
    return {'example_id':str(i),'group_id':str(i),'split':split,'language':'en','text':'example','label':'a','prediction_a':'a','prediction_b':prediction,'confidence':confidence,'task':'topic','preprocessing_version':'test-only'}

class EvaluationTests(unittest.TestCase):
    def test_fixed_labels(self): self.assertEqual(macro_f1([row(1)],'prediction_b',['a','b']),.5)
    def test_group_leakage(self):
        a=row(1); b=row(2,'test'); b['group_id']=a['group_id']
        with self.assertRaises(ValueError): validate([a,b])
    def test_duplicates(self):
        with self.assertRaises(ValueError): validate([row(1),row(1)])
    def test_perfect_interval(self):
        r=interval([row(1),row(2)],['a'],n_boot=20)
        self.assertEqual(r['model_ci95'],[1.0,1.0]); self.assertEqual(r['paired_delta_ci95'],[0.0,0.0])
    def test_validation_only(self):
        with self.assertRaises(ValueError): choose_threshold([row(1,'test')])
    def test_abstention_tradeoff(self):
        rows=[row(1),row(2),row(3),row(4,confidence=.1,prediction='b')]
        t=choose_threshold(rows); result=score(rows,t)
        self.assertEqual(result['coverage'],.75); self.assertEqual(result['accepted_accuracy'],1.0)
    def test_zero_accepted(self): self.assertIsNone(score([row(1)],1)['accepted_accuracy'])
