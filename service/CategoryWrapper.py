import os
from urllib import urlopen,quote
import q2c
import json

TAXONOMY_URL = os.getenv('TAXONOMY_URL')
def search(q):
    qq = quote(q)
    r = urlopen(TAXONOMY_URL + '?doc=' + qq)
    c = json.loads(r.read())['category']
    return [c]

def lookup(q):
    return q2c.lookup(q.lower())[0]
