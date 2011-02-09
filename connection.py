#!/usr/bin/python
'''
	SFTP Interface

'''
import paramiko, time, datetime, dbclient



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
