#!/usr/bin/python
'''
	SFTP Interface

'''
import paramiko, time, datetime, dbclient, config

class SFTPConnection():
	def get_file_list(self):
		transport = paramiko.Transport( (config.get_config('sftp','SERVER'), int(config.get_config('sftp','PORT'))) )
		transport.connect(username = config.get_config('sftp','USERNAME'), password = config.get_config('sftp','PASSWORD'))
		sftp = paramiko.SFTPClient.from_transport(transport)
		files = []
		attrs = sftp.listdir_attr(config.get_config('sftp','PATH'))
		db = dbclient.Client()
		for attr in attrs:
			sftp.get(config.get_config('sftp','PATH') + attr.filename, attr.filename + ".csv")
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
