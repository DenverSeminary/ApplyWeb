import time
import urllib
import httplib

class DBClient:
	def open(self, host="lindev", port=1978, timeout=30):
		self.ua = httplib.HTTPConnection(host,port)
	def close(self):
		self.ua.close()
	def set(self, key, value, xt = None):
		if isinstance(key, str): key = key.encode("UTF-8")
		if isinstance(value, str): value = value.encode("UTF-8")
		key = "/files.kch/" + urllib.quote(key)
		headers = {}
		if xt != None:
			xt = int(time.time()) + xt
			headers["X-Kt-Xt"] = str(xt)
		self.ua.request("PUT", key, value, headers)
		res = self.ua.getresponse()
		body = res.read()
		return res.status == 201
	def get(self, key):
		if isinstance(key, str): key = key.encode("UTF-8")
		key = "/files.kch/" + urllib.quote(key)
		res = self.ua.request("GET", key)
		body = res.read()
		return body
