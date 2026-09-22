import json
from engine import SearchIndex, evaluate

documents = {
    'queue-guide': 'Workers claim jobs with expiring leases. Expired leases allow another worker to retry. Idempotency prevents duplicate side effects.',
    'inventory-guide': 'Inventory reservations run in a database transaction. Conditional stock updates prevent overselling under concurrent requests.',
    'warehouse-guide': 'Incremental ingestion deduplicates event identifiers. Invalid records enter quarantine. A watermark closes event time windows.'}
index = SearchIndex(documents, chunk_size=30, overlap=5)
print(json.dumps({'query': 'expired worker leases', 'evidence': index.search('expired worker leases'),
                  'evaluation': evaluate(index, [('worker leases', {'queue-guide'}), ('stock overselling', {'inventory-guide'}), ('quarantine records', {'warehouse-guide'})], k=2)}, indent=2))
