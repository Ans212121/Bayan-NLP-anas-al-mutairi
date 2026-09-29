import unittest
from bayan_additions.preprocessing import prepare
from bayan_additions.contracts import align_word_labels,entity_report,best_span
class GoldenTests(unittest.TestCase):
    def test_arabic_protected(self): self.assertEqual(prepare('أهلاً  وسهلاً'),'أهلاً وسهلاً')
    def test_search_alef_and_maksura(self): self.assertEqual(prepare('إِلَى مُسْتَشْفَى','arabic-search'),'الي مستشفي')
    def test_tatweel_whitespace(self): self.assertEqual(prepare('مرحبــاً\u00a0بكم'),'مرحباً بكم')
    def test_english(self): self.assertEqual(prepare('  Natural   language  '),'Natural language')
    def test_email_phone(self): self.assertEqual(prepare('a@example.org 0551234567'),'<EMAIL> <PHONE>')
    def test_idempotent_redaction(self):
        x=prepare('<b>اتصل</b> a@example.org 0551234567')
        self.assertEqual(x,'اتصل <EMAIL> <PHONE>'); self.assertEqual(prepare(x),x)
    def test_non_string(self):
        with self.assertRaises(TypeError): prepare(None)
    def test_profile_validation(self):
        with self.assertRaises(ValueError): prepare('text','unknown')
    def test_alignment(self): self.assertEqual(align_word_labels([None,0,1,1,None],[0,3]),[-100,0,3,-100,-100])
    def test_invalid_word_id(self):
        with self.assertRaises(ValueError): align_word_labels([2],[0])
    def test_entity_boundary(self): self.assertEqual(entity_report([['B-ORG','I-ORG']],[['B-ORG','O']])['f1'],0)
    def test_entity_exact(self): self.assertEqual(entity_report([['B-ORG','I-ORG']],[['B-ORG','I-ORG']])['f1'],1)
    def test_arabic_span(self): self.assertEqual(best_span([0,4],[0,4],[None,(0,6)],'الرياض')['answer'],'الرياض')
    def test_null(self): self.assertIsNone(best_span([5,1],[5,1],[None,(0,3)],'bus')['answer'])
    def test_out_of_bounds(self): self.assertEqual(best_span([0,5],[0,5],[None,(0,9)],'bus')['reason'],'no_valid_span')
    def test_question_tokens_excluded(self): self.assertEqual(best_span([0,99,3],[0,99,3],[None,None,(0,3)],'bus')['answer'],'bus')
    def test_empty_logits(self):
        with self.assertRaises(ValueError): best_span([],[],[],'')
    def test_reverse_boundary(self):
        result=best_span([0,1,9],[0,9,1],[None,(0,3),(4,7)],'bus car',top_k=1)
        self.assertEqual(result['reason'],'no_valid_span')
if __name__=='__main__': unittest.main()
