import os, sys, re
import whoosh.index as index
from whoosh import query
from whoosh.query import And, Or, Term
from whoosh.qparser import QueryParser,MultifieldParser
from whoosh.searching import Searcher
from whoosh.filedb.filestore import FileStorage
import json

# open index
#BASE_DIR=os.getenv('WHOOSH_BASEDIR')
BASE_DIR='/data1/whoosh/index'

PRODUCT_TITLE='title'
PRODUCT_CATEGORY='catpred'

storage = FileStorage(BASE_DIR+"/ix")
ix = storage.open_index()


p_key=r'(\w+)'
p_val=r'(\w+|".+?")'
p_vals_ored=r'(\('+p_val+r'( OR (\w+|".+?"))+\))'
p_kvp='('+p_key+r':(('+p_val+')|('+p_vals_ored+'))?)'
p_kvps_anded='('+p_kvp+r'( AND '+p_kvp+')+)'
pattern_key=re.compile(p_key)
pattern_val=re.compile(p_val)
pattern_vals_ored=re.compile(p_vals_ored)
pattern_kvp=re.compile(p_kvp)
pattern_kvps_anded=re.compile(p_kvps_anded)
def parseFQ(s, valid_keys):
	and_match = pattern_kvps_anded.match(s)
	exprs_ = [s]
	if and_match!=None:
		anded_values = and_match.group(0)
		exprs_ = [match[0] for match in pattern_kvp.findall(anded_values)]
	exprs = []
	for expr_ in exprs_:
		expr = None
		kvp_match = pattern_kvp.match(expr_)
		try:
			kvp = kvp_match.group(0)
			key = pattern_key.match(kvp).group(0)
			if(key in valid_keys):
				voffset = len(key)+1
				ored_values_match = pattern_vals_ored.match(s[voffset:])
				if ored_values_match!=None:
					ored_values = ored_values_match.group(0)
					values = [v for v in pattern_val.findall(ored_values) if v!='OR']
					values = [v[1:-1] for v in values if (v[0]=='"' and v[-1]=='"')]
					expr = Or([Term(key, value) for value in values])
				else:
					value = pattern_val.match(kvp[voffset:]).group(0)
					print key, value
					if value[0]=='"' and value[-1]=='"':
						value = value[1:-1]
					expr = Term(key,value)
		except Exception, e:
			sys.stderr.write('Error parsing %s, Exception: %s'%(s,str(e)))
			raise Exception('Error Parsing FQ')
		if expr!=None: exprs.append(expr)
	return And(exprs) if len(exprs)>0 else None

def to_solr_format(res, start):
	solr_res={'responseHeader':{}}
	solr_res['responseHeader'].update({'QTime':'0.0'})
	solr_res.update({'response':{}})
	solr_res['response'].update({'numFound':0})
	solr_res['response'].update({'start':start})
	solr_res['response'].update({'maxScore':'0.0'})
	solr_res['response'].update({'docs':[]})
	for r in res:
		solr_res['response']['docs'].append({
			'url':r['url'],
			'product_title':r['title'],
			'raw_catpred':r['catpred'],
			'sku':r['sku'],
		})
	return json.dumps(solr_res)
		

def search(params):
	q_=params.get('q','*')
	fq=params.get('fq','*')
	start=int(params.get('start',0))
	rows=int(params.get('rows',20))
	titleparse = QueryParser(PRODUCT_TITLE, schema=ix.schema)
	with ix.searcher() as s:
		q=[]
		print "Parsing q:%s"%q_
		if q_!='*':
			titleq=titleparse.parse(q_)
			q.append(titleq)
		print "Parsing fq:%s"%fq
		if fq!='*':
			filterq=parseFQ(fq, ix.schema.names())
			print str(filterq)
			if filterq!=None: q.append(filterq)
		print "Whoosh query: %s"%str(q)
		results = s.search_page(And(q), start+1, pagelen=rows)
		return to_solr_format(results, 0)


if __name__ == "__main__":
	if len(sys.argv)>2:
		print str(search({'q':sys.argv[1],'fq':sys.argv[2]}))
	else:
		print str(search({'q':sys.argv[1]}))
