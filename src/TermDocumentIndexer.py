from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, TermDocumentIndex
from text import BasicTokenProcessor, EnglishTokenStream

"""This basic program builds a term-document matrix over the .txt files in
the current working directory, then lets the user search it for single terms."""

def index_corpus(corpus : DocumentCorpus) -> Index:

    token_processor = BasicTokenProcessor()
    vocabulary = set()

    # First pass: find the full vocabulary of the corpus.
    for d in corpus:
        print(f"Found document {d.title}")
        with d.get_content() as content:
            for token in EnglishTokenStream(content):
                term = token_processor.process_token(token)
                if len(term) > 0:
                    vocabulary.add(term)

    # Second pass: now that the vocabulary and corpus size are known, build the matrix.
    index = TermDocumentIndex(vocabulary, len(corpus))
    for d in corpus:
        with d.get_content() as content:
            for token in EnglishTokenStream(content):
                term = token_processor.process_token(token)
                if len(term) > 0:
                    index.add_term(term, d.id)

    return index

if __name__ == "__main__":
    corpus_path = Path()
    d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")

    # Build the index over this directory.
    index = index_corpus(d)
    token_processor = BasicTokenProcessor()

    # Prompt the user for terms to search for until they enter "quit".
    while True:
        query = input("\nEnter a term to search for (or \"quit\" to exit): ").strip()
        if query.lower() == "quit":
            break

        # Process the query the same way document tokens were processed, so it matches index terms.
        term = token_processor.process_token(query)
        postings = index.get_postings(term)
        if len(postings) == 0:
            print(f"No documents contain the term \"{term}\".")
            continue

        for p in postings:
            print(f"Document {d.get_document(p.doc_id)}")
        print(f"{len(postings)} document(s) found.")
