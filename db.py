'''
	db.py (not to be confused with dbi.py which is kyoto product-based) is the database interface for ApplyWeb "process progress" database (Redis). This database will store information about whether or not the file has been processed
'''
import redis
import simplejson as json

r = redis.Redis(host='sp-dev')


def store_stats(filename, stats):
	r[filename] = json.dumps(stats)
	
def get_stats(filename):
	if r[filename] is not None:
		return json.loads(r[filename])
	else:
		return None
