# CECS 429/529 – Assignment 4: Term-Document Matrix Search

A basic single-term search engine over the first 10 chapters of *Moby Dick*. It uses a boolean term-document matrix.

## Running

From the project root, which holds the `chapter*.txt` files:

```
python3 src/TermDocumentIndexer.py
```

The program prints each document as it indexes it. It then asks for a term, lists the documents that contain it, and keeps asking until you type `quit`.

## What was implemented

- `src/TermDocumentIndexer.py`
  - `index_corpus()`: the first pass tokenizes every document (`EnglishTokenStream` + `BasicTokenProcessor`) to build the vocabulary. The second pass builds a `TermDocumentIndex` and calls `add_term()` for every term.
  - `main`: a loop that asks for a term, processes it with the same `BasicTokenProcessor`, and prints the matching documents. It exits on `quit`.
- `src/indexing/termdocumentindex.py`
  - `get_postings()`: binary-searches the sorted vocabulary with `bisect_left`, then walks the term's matrix row and returns a `Posting` for each `True` column. Postings come back in increasing doc ID order. If the term isn't in the vocabulary, it returns an empty list.

## Fixes to the starter code

- Removed unused imports that crash on Python 3.12+ (`from ast import Str`) or are dead code (`pyclbr`, `pydoc`, `email.generator`).
- Removed `from indexing.invertedindex import InvertedIndex` from `indexing/__init__.py`. That module isn't in the starter code, so the import fails.

## Example: `whale`

Returns chapters 1, 2, 3, 7 and 9. Chapter 6 only has "whale-lance", which the processor turns into the single term `whalelance`, so it is correctly left out.

## Other corpora

These datasets are included so the whole group has them. Assignment 4 doesn't use them.

- `corpora/all-nps-sites-extracted/`: 36,803 JSON documents from National Park Service web pages
- `corpora/mlb-articles-4000/`: 4,000 MLB news articles as JSON, split across subfolders `1`–`4`
