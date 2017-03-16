import sys, os
cur = os.path.dirname (__file__)
parent_dir = '/'.join(cur.split('/')[:-1])
#print 'parent'
#print parent_dir
sys.path.append(parent_dir)

# if left empty, there will be no limit
QUERY_LIMIT = "LIMIT 100"
RAW_ENDPOINT = "http://4v.dia.fi.upm.es:10043/sparql"
#RAW_ENDPOINT = "http://dbpedia.org/sparql"
META_ENDPOINT = "http://patents.linkeddata.es/sparql"
