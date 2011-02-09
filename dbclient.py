#!/usr/bin/python
'''
	tycoon interface
'''
import pycurl, cStringIO
GET_URL = "http://lindev:1978/%db%/%key%"
SET_URL = GET_URL
class Client:
	def __init__(self):
		self.buffer = ""	
		self.conn = pycurl.Curl()
		#self.conn.setopt(pycurl.VERBOSE, 1)						
	def on_put(self, data):
		print self.conn.getinfo(pycurl.HTTP_CODE)		
	def get(self, database, key):
		self.response = cStringIO.StringIO()								
		self.conn.setopt(pycurl.URL, GET_URL.replace("%db%", database).replace("%key%", key))
		self.conn.setopt(pycurl.CUSTOMREQUEST, "GET")
		self.conn.setopt(pycurl.WRITEFUNCTION, self.response.write)
		self.conn.perform()			
	def set(self, database, key, value):
		self.response = cStringIO.StringIO()								
		self.conn.setopt(pycurl.URL, GET_URL.replace("%db%", database).replace("%key%", key))
		#self.conn.setopt(pycurl.POST, 1)	
		self.conn.setopt(pycurl.CUSTOMREQUEST, "PUT")		
		self.conn.setopt(pycurl.POSTFIELDS, "%s" % value)
		#self.conn.setopt(pycurl.WRITEFUNCTION, self.response.write)	
		self.conn.perform()
		return self.conn.getinfo(pycurl.RESPONSE_CODE)
