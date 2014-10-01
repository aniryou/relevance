import sys
import difflib
from collections import Counter
from itertools import chain
import pickle

Q2C_DICT="Q2C_Dict_amazon.pickle"

dict = pickle.load(file(Q2C_DICT,"rb"))
keys = dict.keys()

def fuzzylookup(q,threshold=.6):
	matches = difflib.get_close_matches(q,keys,3,threshold)
	matches_kvp = ((k,dict[k]) for k in matches)
	matches_cats = list(chain.from_iterable((tup[1] for tup in matches_kvp)))
	matches_aggcats = Counter(matches_cats)
	res,counts = [],[]
	if(len(matches_aggcats)>0):
		res,counts = tuple([tup for tup in zip(*matches_aggcats.most_common())])
	return res,counts


def lookup(q):
	return fuzzylookup(q,.9)

if __name__=="__main__":
	for line in sys.stdin:
		print str(lookup(line[:-1]))
