from urllib import urlopen,quote
import json

SOLR_HOSTS=['solr01.perf.indix.tv:8983','solr02.perf.indix.tv:8983','solr03.perf.indix.tv:8983','solr04.perf.indix.tv:8983','solr05.perf.indix.tv:8983']
SOLR_COLLECTION='relevance'

rr=0 #round-robin
rr_max = len(SOLR_HOSTS)
def get_solr_host():
	global rr
	host = SOLR_HOSTS[rr]
	rr=(rr+1)%rr_max
	return host

def parse_params(dict):
	r=dict
	if (r.has_key('q')) and (r['q'][:2]!='{!'):
		r['q'] = LOCAL_PARAM_DF+r['q']
	return r

def escape_quote(dict):
	return '&'.join([k+'='+quote(dict[k]) for k in dict.keys()])

LOCAL_PARAM_DF='{!df=product_title_en}'
default_params={
		'q':'*:*',
		'wt':'json',
		'indent':'true',
		'rows':'100',
	}

def search(params):
	solr_params = {}
	solr_params.update(default_params)
	solr_params.update(parse_params(params))
	solr_url = 'http://%s/solr/%s/select?%s'%(get_solr_host(),SOLR_COLLECTION,escape_quote(solr_params))
	print solr_url
	res = urlopen(solr_url)
	return res

if __name__=="__main__":
	res = search({'q':'iphone'})
	print json.loads(res.read())
