from urllib import urlopen,quote
import json

PI_SEARCHURL='http://services01.production.indix.tv:2706/pi/search?'

def to_solr_format(res, start):
	solr_res={'responseHeader':{}}
	solr_res['responseHeader'].update({'QTime':0.0})
	solr_res.update({'response':{}})
	solr_res['response'].update({'numFound':0})
	solr_res['response'].update({'start':0})
	solr_res['response'].update({'maxScore':0.0})
	solr_res['response'].update({'docs':[]})
	if not res.has_key('products'):
		return solr_res
	for r in res['products'][start:]:
		solr_res['response']['docs'].append({
			'url':r['productUrl'],
			'product_title':r['title'],
			#i'raw_catpred':r['categoryName'],
			'sku':r['sku']})
	return solr_res

def oredintvaluesfix(key, values):
	values = values[1:-1] if(values[0]=='(' and values[-1]==')') else values
	values = [v.strip() for v in values.split('OR')]
	values = [v[1:-1] if(v[0]=='"' and v[-1]=='"') else v for v in values]
	res = ['%s=%s' % (key, value) for value in values]
	return res

def map_params(params):
	q = params.get('q','')
	fqdict = {}
	if(params.has_key('fq')):
		kvps = params['fq'].replace(' AND ','/').split('/')
		for kvp in kvps:
			print kvp
			tokens = kvp.strip().split(':')
			key = tokens[0]
			value = tokens[1]
			fqdict.update({key:value})
	if fqdict.has_key('sku'):
		q = 'sku:'+fqdict['sku']
	start = int(params.get('start','0'))
	rows = int(params.get('rows','10'))
	if(start>0):
		rows = start*rows
	pi_params = []
	pi_params.append('q=%s' % quote(q))
	if fqdict.has_key('store'):
		pi_params.extend(oredintvaluesfix('store', fqdict['store']))
	pi_params.append('pageSize=%s' % params.get('rows',rows))
	return pi_params, start

def search(params):
	pi_params, start = map_params(params)
	pi_url = PI_SEARCHURL + '&'.join(pi_params)
	pi_res = urlopen(pi_url)
	pi_resjson = json.loads(pi_res.read())
	res = to_solr_format(pi_resjson, start)
	res_json = json.dumps(res)
	return res_json

if __name__=='__main__':
	#print search({'q':'iphone'})
	#print search({'fq':'sku:B00EGJ0WUO'})
	#print search({'q':'iphone','fq':'store:(24 OR 270)'})
	#print search({'q':'iphone','fq':'store:"24"'})
	print search({'fq':'store:(24 OR 270) AND sku:B0027AANDA','wt':'json','fl':'sku'})
