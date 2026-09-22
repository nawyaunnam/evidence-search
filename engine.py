"""Inspectable lexical search with source-level ranking evaluation."""
import math
import re
from collections import Counter, defaultdict

def tokenize(text):
    return re.findall(r'[a-z0-9]+', text.lower())

class SearchIndex:
    def __init__(self, documents, chunk_size=120, overlap=20, k1=1.5, b=0.75):
        if chunk_size <= 0 or not 0 <= overlap < chunk_size or k1 <= 0 or not 0 <= b <= 1:
            raise ValueError('invalid chunking or BM25 parameters')
        self.chunks, self.postings, self.df = [], defaultdict(list), Counter()
        self.k1, self.b = k1, b
        for source, text in sorted(documents.items()):
            spans = list(re.finditer(r'[a-z0-9]+', text.lower()))
            for offset in range(0, len(spans), chunk_size-overlap):
                window = spans[offset:offset+chunk_size]
                terms = [s.group() for s in window]
                counts = Counter(terms)
                chunk_id = len(self.chunks)
                self.chunks.append({'source': source, 'offset': offset,
                    'text': text[window[0].start():window[-1].end()], 'length': len(terms)})
                for term, frequency in counts.items():
                    self.postings[term].append((chunk_id, frequency))
                    self.df[term] += 1
                if offset + chunk_size >= len(spans): break
        self.average_length = sum(c['length'] for c in self.chunks) / max(len(self.chunks), 1)

    def search(self, query, k=5):
        if k < 1: raise ValueError('k must be positive')
        scores = defaultdict(float)
        n = len(self.chunks)
        for term in set(tokenize(query)):
            if term not in self.df: continue
            idf = math.log(1 + (n-self.df[term]+0.5)/(self.df[term]+0.5))
            for idx, tf in self.postings[term]:
                norm = 1-self.b+self.b*self.chunks[idx]['length']/self.average_length
                scores[idx] += idf * tf * (self.k1+1)/(tf+self.k1*norm)
        ordered = sorted(scores, key=lambda idx: (-scores[idx], self.chunks[idx]['source'], self.chunks[idx]['offset']))
        return [dict(self.chunks[idx], score=round(scores[idx], 6)) for idx in ordered[:k]]

def evaluate(index, judgments, k=5):
    if not judgments: raise ValueError('at least one judged query required')
    rows = []
    for query, relevant in judgments:
        if not relevant: raise ValueError('each query needs a relevant source')
        # Rank unique sources, so overlapping chunks do not inflate retrieval counts.
        ranked = list(dict.fromkeys(x['source'] for x in index.search(query, max(1, len(index.chunks)))))[:k]
        hits = set(ranked) & set(relevant)
        rr = next((1/rank for rank, source in enumerate(ranked, 1) if source in relevant), 0)
        rows.append({'query': query, 'recall': len(hits)/len(relevant), 'reciprocal_rank': rr})
    return {'k': k, 'queries': len(rows), 'mean_recall': sum(r['recall'] for r in rows)/len(rows),
            'mrr': sum(r['reciprocal_rank'] for r in rows)/len(rows), 'per_query': rows}
