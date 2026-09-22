from feeds import fetch,run
from engine import SearchIndex

def acquire():
    return {'sources':[fetch('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson')]}


def analyze(snapshot):
    data=snapshot['sources'][0]['payload']
    documents={f['id']:f"{f['properties'].get('title','')} Place: {f['properties'].get('place','')} Magnitude: {f['properties'].get('mag')}" for f in data['features']}
    index=SearchIndex(documents)
    urls={f['id']:f['properties'].get('url') for f in data['features']}
    # An actual place from the current feed ensures the example stays tied to live evidence.
    query=next((f['properties'].get('place') for f in data['features'] if f['properties'].get('place')),'earthquake')
    results=[dict(row,url=urls[row['source']]) for row in index.search(query,k=5)]
    return {'project':'EvidenceSearch','indexed_real_documents':len(documents),
            'source_generated_ms':data['metadata']['generated'],'query':query,'evidence':results,
            'note':'Live retrieval results, not an accuracy evaluation; offline relevance judgments are in demo.py.'}


if __name__=='__main__': run(acquire,analyze)
