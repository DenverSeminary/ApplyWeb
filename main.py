#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import re
from dbi import dbi
import simplejson as json


from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),  
            (r"/async", AsynchHandler),          
        ]
        settings = dict(
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",            
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,            
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class AsynchHandler():	
	def get(self):
		key = self.get_argument('file')
		self.write(key)
		#db = dbi()
		#db.conn()
		#data = db.get(key)
		#self.write(data)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
		files = []
		db = dbi()
		db.conn()
		flist = os.listdir('data/')
		for f in flist:	
			data = db.get(f)
			if data is not None:
				data = json.loads(data)
				if 'Flagged' in data.keys():
					files.append( (f,re.search("[0-9]{8}",f).group(0), 'flagged') )
				else:
					files.append( (f,re.search("[0-9]{8}",f).group(0), 'good') )
			else:
				files.append( (f,re.search("[0-9]{8}",f).group(0), 'sync') )
		self.render("main.html", files = sorted(files, key=lambda f: f[1], reverse=True))

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
