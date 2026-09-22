# Engineering notes: EvidenceSearch — retrieval with source citations

## Problem and flow

Documents → overlapping token chunks with source IDs → inverted index and BM25 statistics → ranked passages → source-level evaluation. Search returns evidence verbatim, with source ID and token offset. Unknown queries yield no evidence rather than invented answers.

## Current boundaries

Lexical retrieval baseline, not a neural embedding model or generative RAG system. No LLM is called. The included corpus and relevance judgments are small hand-authored fixtures; metrics are a correctness demonstration, not real-world accuracy claims.

## Interview walkthrough

1. Run the demo and explain each output in terms of the code.
2. Show a test that exercises a failure rather than only a successful call.
3. Trace one input through the core implementation and its stored state.
4. Explain the tradeoff made by the current storage or algorithm choice.
5. Describe what would change with 100× the data or concurrent users.
6. Make a small extension and add a regression test before using this in a resume.

## Validation

See `test_engine.py` for executable assertions and `docs/demo-output.txt` for
captured results. CI is configured but remote CI results are not assumed.
