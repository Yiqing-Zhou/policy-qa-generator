import data
import doc_parser
import diagnostics

docs = data.load_documents()

for doc in docs:
    doc_parser.parse_paragraphs(doc)
    doc_parser.classify_paragraphs(doc)
    diagnostics.export(doc)
