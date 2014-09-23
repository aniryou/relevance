import whoosh.index as index
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser
from whoosh.searching import Searcher

# open index
storage = FileStorage("ix")
ix = storage.open_index()

def search(params):
	qp = QueryParser("title", schema=ix.schema)
	with ix.searcher() as s:
		
