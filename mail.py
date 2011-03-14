#!/usr/bin/env python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def format_matches(fileinfo):
	fuzzy_matches = ''
	
	for name, value in fileinfo['Flagged'].iteritems():
		fuzzy_matches += "<div style='text-indent: 15px;'>%s (note, this is the name as it appears in the file)</div>" % name
		fuzzy_matches +=  "<div style='text-indent: 25px;'>Potential Matches (data as found in CX):</div>"
		for id, data in value.iteritems():
			fuzzy_matches += "<div style='text-indent: 35px;'>Student ID: %s</div>" % id
			fuzzy_matches += "<div style='text-indent: 35px;'>Student Name: %s %s %s</div>" % (data['FirstName'], data['MiddleName'], data['LastName'])
			fuzzy_matches += "<div style='text-indent: 35px;'>State: %s</div>" % data['State']
			fuzzy_matches += "<div style='text-indent: 35px;'>Matched Middle Name: %s</div>" % data['MatchedMiddle']
			fuzzy_matches += "<div style='text-indent: 35px;'>Matched State: %s</div>" % data['MatchedState']
			
	return fuzzy_matches

def notify(file_info):
	# me == my email address
	# you == recipient's email address
	me = "seth.washeck@denverseminary.edu"
	you = "seth.washeck@denverseminary.edu"

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "New Inquiry Loaded"
	msg['From'] = me
	msg['To'] = you

	# Create the body of the message (a plain-text and an HTML version).
	text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"	
	
	html = """\
	<html>
	  <head></head>
	  <body style='font-family:Corbel, Calibri;font-size:9pt;'>
		<p>A new file has been processed. Here are your results:<br>		   
		   <div style='text-indent: 5px'>File Name: %s</div>
		   <div style='text-indent: 5px'>Start Time: %s</div>
		   <div style='text-indent: 5px'>Finish Time: %s</div>
		   <div style='text-indent: 5px'>Total Records: %s</div>
		   <div style='text-indent: 5px'>Flagged Records: %s</div>
		   %s
		</p>
	  </body>
	</html>
	""" % (file_info['FileName'], file_info['StartTime'], 
			file_info['FinishTime'], file_info['TotalRecords'], 
			len(file_info['Flagged']) if 'Flagged' in file_info.keys() else 'None',
			format_matches(file_info))

	# Record the MIME types of both parts - text/plain and text/html.
	#part1 = MIMEText(text, 'plain')
	part1 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)


	# Send the message via local SMTP server.
	s = smtplib.SMTP('jacob.densem.edu')
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(me, you, msg.as_string())
	s.quit()
