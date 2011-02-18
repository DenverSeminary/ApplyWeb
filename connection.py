#!/usr/bin/python
'''
	SFTP Interface

'''
import paramiko, time, config, dbi
from datetime import datetime

class SFTPConnection():
	
	def get_file_list(self):
		db = dbi.dbi()
		db.conn()
		transport = paramiko.Transport( (config.get_config('sftp','SERVER'), int(config.get_config('sftp','PORT'))) )
		transport.connect(username = config.get_config('sftp','USERNAME'), password = config.get_config('sftp','PASSWORD'))
		sftp = paramiko.SFTPClient.from_transport(transport)
		files = []
		attrs = sftp.listdir_attr(config.get_config('sftp','PATH'))		
		for attr in attrs:								
			if db.get(attr.filename) is None:
				sftp.get(config.get_config('sftp','PATH') + attr.filename, attr.filename + ".csv")
				db.set(attr.filename, str(int(time.mktime(datetime.timetuple(datetime.now())))))
				files.append(attr.filename + ".csv")
		sftp.close()
		transport.close()				
		return files	
