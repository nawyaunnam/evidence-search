import unittest
from engine import SearchIndex, evaluate

class SearchTests(unittest.TestCase):
    def test_ranking(self):
        idx = SearchIndex({'a':'database transaction rollback', 'b':'neural model training'})
        self.assertEqual(idx.search('rollback')[0]['source'], 'a')
    def test_unknown_and_empty(self):
        self.assertEqual(SearchIndex({'a':'hello'}).search('xyz'), [])
        self.assertEqual(SearchIndex({}).search('hello'), [])
    def test_citations_are_verbatim(self):
        source = 'Hello, world! A searchable document with punctuation.'
        idx = SearchIndex({'a':source},chunk_size=4,overlap=1)
        for row in idx.search('world document'):
            self.assertIn(row['text'], source)
    def test_metrics_no_duplicate_inflation(self):
        idx = SearchIndex({'a':'cat cat cat cat cat','b':'dog'},chunk_size=2,overlap=1)
        result = evaluate(idx,[('cat',{'a','b'})],k=2)
        self.assertEqual(result['mean_recall'],0.5)
        self.assertEqual(result['mrr'],1)
    def test_invalid_chunking(self):
        with self.assertRaises(ValueError): SearchIndex({},chunk_size=2,overlap=2)
    def test_unmatched_query_scores_zero(self):
        self.assertEqual(evaluate(SearchIndex({'a':'cat'}),[('dog',{'a'})])['mrr'],0)
