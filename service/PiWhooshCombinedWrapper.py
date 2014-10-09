import WhooshWrapper as w
import PiWrapper as p
import json

def interleave(a,b,N):
	res = {}
	res.update({'responseHeader':{}})
	res['responseHeader'].update({'QTime':a['responseHeader']['QTime']+b['responseHeader']['QTime']})
	res.update({'response':{}})
	res['response'].update({'numFound':a['response']['numFound']+b['response']['numFound']})
	res['response'].update({'start':a['response']['start']})
	res['response'].update({'maxScore':max(a['response']['maxScore'],b['response']['maxScore'])})
	m = len(a['response']['docs'])
	n = len(b['response']['docs'])
	i = 0
	j = 0
	skus = set()
	docs = []
	for k in range(m+n):
		if(i<m):
			sku = a['response']['docs'][i].get('sku',None)
			if(sku!=None and sku not in skus):
				docs.append(a['response']['docs'][i])
				skus.add(sku)
			i += 1
		if(j<n):
			sku = b['response']['docs'][j].get('sku',None)
			if(sku!=None and sku not in skus):
				docs.append(b['response']['docs'][j])
				skus.add(sku)
			j += 1
	res['response']['docs'] = docs[:N]
	return res

def search(params):
	rows = int(params.get('rows','10'))
	wres = w.search(params)
	pres = p.search(params)
	res = interleave(json.loads(wres),json.loads(pres),rows)
	res_json = json.dumps(res)
	return res_json
	
if __name__=='__main__':
	#print search({'q':'iphone'})
	#print search({'fq':'sku:B00EGJ0WUO'})
	print search({'fq':'raw_catpred:("tools & home improvement > parts & accessories > refrigerator parts & accessories" OR "tools & home improvement > lighting & ceiling fans > ceiling lights > pendant lights" OR "tools & home improvement > kitchen & bath fixtures > bathroom fixtures > bathtub faucets & showerheads > bathtub & shower systems") AND sku:B001IDJCXY'})
	#print search({'fq':'sku:B00EGJ0WUO'})
