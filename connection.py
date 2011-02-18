#!/usr/bin/python
'''
	SFTP Interface

'''
import paramiko, time, dbclient, config
from datetime import datetime

class SFTPConnection():
	
	def get_file_list(self):
		transport = paramiko.Transport( (config.get_config('sftp','SERVER'), int(config.get_config('sftp','PORT'))) )
		transport.connect(username = config.get_config('sftp','USERNAME'), password = config.get_config('sftp','PASSWORD'))
		sftp = paramiko.SFTPClient.from_transport(transport)
		files = []
		attrs = sftp.listdir_attr(config.get_config('sftp','PATH'))
		db = dbclient.Client()
		for attr in attrs:
			if db.get('files.kch',attr.filename) is None:
				# if the filename is not in the database, we assume that the file has not been processed. 
				sftp.get(config.get_config('sftp','PATH') + attr.filename, attr.filename + ".csv")
				# then we get the file
				db.set('files.kch', attr.filename, str(int(time.mktime(datetime.timetuple(datetime.now())))))
				# then we save the filename in the database so that we don't pull it again.
				files.append(attr.filename + '.csv')
				# finally, we put it in the list 
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
