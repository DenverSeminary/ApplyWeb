#!/usr/bin/python
'''
	Processes and parses the inquiry information
'''
import odbc, csv, config, re
from datetime import datetime
import simplejson as json

#CONNECTION_STRING = str(config.get_config('db','x64_CONNECTION_STRING'))
#CONNECTION_STRING = "dsn=cars"
CONNECTION_STRING = "dsn=noah"
db = odbc.odbc(CONNECTION_STRING)
cur = db.cursor()

def convert_date(value):		
	'''
		because the date has appeared in different formats, this function attempts to 
		clean the date
	'''
	date_object = datetime.strptime(value, '%Y-%m-%d')
	return datetime.strftime(date_object, '%m/%d/%y')
	
def scan_dupe(lastname, firstname, middle, state):
	'''
		check the database to see if there is a potential duplicate (someone who's already applied in the past)
	'''
	sql = "select id, lastname, firstname, middlename, st from id_rec where lastname like ? and firstname like ?"
	params = [lastname + '%', firstname + '%']	
	cur.execute(sql, params)	
	results = cur.fetchall()			
	dup_info = {}
	middlematch = False
	statematch = False
	if len(results) > 0:
		for result in results:	
			if re.sub('\.','',result[3]).strip() == middle:				
				middlematch = True		
			if result[4].strip() == state:				
				statematch = True		
			dup_info[result[0]] = {'LastName': result[1], 'FirstName': result[2], 
                'MiddleName': result[3], 'State': result[4], 'MatchedMiddle': middlematch, 'MatchedState': statematch}	
	return dup_info, (middlematch or statematch)	#I may need to look into this
	
def load_data(row):
	try:
		row["DSEMINQ-TRANSACTION_DATE"] = convert_date(row["DSEMINQ-TRANSACTION_DATE"])
	except:
		row["DSEMINQ-TRANSACTION_DATE"] = row["DSEMINQ-TRANSACTION_DATE"]		
	try:
		row["BIRTH_DATE"] = convert_date(row["BIRTH_DATE"])
	except:
		row["BIRTH_DATE"] = row["BIRTH_DATE"]		
	sql = "insert into apptmp_rec (app_source, add_date, stat, birth_date) values (?, TO_DATE(?, '%m/%d/%y'), ?, TO_DATE(?, '%m/%d/%y'))"
	params = ['WEB', row["DSEMINQ-TRANSACTION_DATE"], 'C', row["BIRTH_DATE"]]		
	print sql, params						
	cur.execute(sql, params)	
	cur.execute("select dbinfo('sqlca.sqlerrd1') from apptmp_rec")
	results = cur.fetchone()
	new_id = results[0]			
	sql = '''insert into app_idtmp_rec (id, fullname, addr_line1, city, st, zip, ctry, aa, title, ss_no, 
				phone, add_date, ofc_add_by, firstname, lastname, email) 
			 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, TO_DATE(?, '%m/%d/%y'), ?, ?, ?, ?)'''
	params = [new_id, row['FULLNAME'], row["MAIL_STREET"], row["MAIL_CITY"], row["MAIL_STATE"], row["MAIL_ZIP"], row["MAIL_COUNTRY"], 
			'HOME', row["DSEMINQ-TITLE"], row["SS_NUM"], row["PHONE"], row["DSEMINQ-TRANSACTION_DATE"], 'ADM', row["NAME_FIRST"], row["NAME_LAST"], row["EMAIL"]]		
			
	print sql, params
	cur.execute(sql, params)
	
	sql = "insert into app_proftmp_rec (id, birth_date, res_st, res_cty) values (?, TO_DATE(?, '%m/%d/%y'), ?, ?)"
	params = [new_id, row['BIRTH_DATE'], row['STATE'], row['CITY']]	
	#need some new logic in here that if STATE == '' then go to MAIL_STATE		
	print sql, params
	cur.execute(sql, params)
	sql = '''insert into app_admtmp_rec (id, plan_enr_sess, plan_enr_yr, prog, subprog, add_date, ref_source, enrstat, major, major2, deg, app_source, jics_candidate)
		values (?,?,?,?,?, TO_DATE(?, '%m/%d/%y'),?,?,?,?,?,?,?)'''
	params = [new_id, row["DSEMINQ-ENROLL_SESSION"], row["DSEMINQ-ENROLL_YEAR"], 'MSTR', 'NA', row["DSEMINQ-TRANSACTION_DATE"], row["DSEMINQ-HOW_HEARD"], 'INQUIRED', row["DSEMINQ-MAJOR"], 'NA', row["DSEMINQ-DEGREE"], 'WEB', 'N']
	print sql, params
	cur.execute(sql, params)
	sql = "insert into app_sitetmp_rec (id, beg_date, site, home) VALUES (?, TO_DATE(?, '%m/%d/%y'), ?, ?)"
	params = [new_id, row["DSEMINQ-TRANSACTION_DATE"], 'CARS', 'Y']
	print sql, params
	cur.execute(sql, params)
	
def process(filename):		
	reader = csv.DictReader(open("data\\" + filename, "rb"))	
	flagged_records = {}
	fileinfo = {}	
	fileinfo['StartTime'] = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
	records = 0
	for row in reader:
		records += 1
		dup_info = {}
		row["FULLNAME"] = "%s, %s %s" % (row["NAME_LAST"].strip(), row["NAME_FIRST"].strip(), row["NAME_MIDDLE"].strip())		
		dup_info, isdup = scan_dupe(row["NAME_LAST"].strip(), row["NAME_FIRST"].strip(), row["NAME_MIDDLE"].strip(), row["STATE"].strip())		
		if not isdup:
			#load_data(row)			
			pass
		else: #finished here on 7 march, 2011. flagged_records should contain all of the matches for each record
			flagged_records[row["FULLNAME"]] = dup_info
	'''
		now i just need to load the file info into the redis db
	'''
	fileinfo['TotalRecords'] = records	
	fileinfo['FinishTime'] = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
	fileinfo['FileName'] = filename
	if len(flagged_records) > 0:
		fileinfo['Flagged'] = flagged_records
	import mail
	mail.notify(fileinfo)
	print json.dumps(fileinfo)
	
	import dbi
	db = dbi.dbi()
	db.conn()
	db.set(filename.split('.')[0], json.dumps(fileinfo))
	
	print 'Data Stored'
	
	
