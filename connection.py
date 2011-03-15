#!/usr/bin/python
'''
	SFTP Interface

'''
import paramiko, time, config, os
from datetime import datetime
from dbi import dbi

class SFTPConnection():
	
	def get_file_list(self):				
		transport = paramiko.Transport( (config.get_config('sftp','SERVER'), int(config.get_config('sftp','PORT'))) )
		db = dbi()
		db.conn()
		transport.connect(username = config.get_config('sftp','USERNAME'), password = config.get_config('sftp','PASSWORD'))
		sftp = paramiko.SFTPClient.from_transport(transport)
		files = []
		dirfiles = os.listdir('data/')
		attrs = sftp.listdir_attr(config.get_config('sftp','PATH'))		
		for attr in attrs:								
			if (attr.filename + '.csv') not in dirfiles:
				sftp.get(config.get_config('sftp','PATH') + attr.filename, 'data/' + attr.filename + ".csv")				
				files.append(attr.filename + ".csv")
		sftp.close()
		transport.close()				
		return files	
