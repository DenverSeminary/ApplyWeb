#!/usr/bin/python
'''
	Main Inquiry System
'''
#import dbclient, connection

import connection


conn = connection.SFTPConnection()
#db = dbclient.Client()
file_list = conn.get_file_list()

print file_list

for filename in file_list:
	print filename
