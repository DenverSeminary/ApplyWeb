#!/usr/bin/python
'''
	SFTP Interface

'''
import paramiko, time, datetime, dbclient

SERVER = "sftp.applyweb.com"
PORT = 22
USERNAME = "dsemftp"
PASSWORD = "collegenet"
PATH = "dsem/"

'''
for file in files:
	print file
for attr in files:	
	print attr.filename	
	print attr.st_mtime
	print time.ctime(int(attr.st_mtime))	
	print datetime.date.fromtimestamp(int(attr.st_mtime))

#print files
sftp.close()
transport.close()
'''
class SFTPConnection():
	def get_file_list(self):
		transport = paramiko.Transport( (SERVER, PORT) )
		transport.connect(username = USERNAME, password = PASSWORD)
		sftp = paramiko.SFTPClient.from_transport(transport)
		files = []
		attrs = sftp.listdir_attr(PATH)
		db = dbclient.Client()
		for attr in attrs:
			sftp.get(PATH + attr.filename, attr.filename + ".csv")
			'''
			if db.get('files.kch', attr.filename) == None:
				fil = {}
				fil['filename'] = attr.filename
				fil['filedate'] = attr.st_mtime
				files.append(fil)			
				sftp.get(PATH + attr.filename, attr.filename + ".csv")
			'''
		sftp.close()
		transport.close()		
		return files	
