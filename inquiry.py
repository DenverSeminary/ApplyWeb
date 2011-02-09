#!/usr/bin/python
'''
	Processes and parses the inquiry information
'''
import odbc, csv, config
from datetime import datetime

def convert_date(value):		
	date_object = datetime.strptime(value, '%Y-%m-%d')
	return datetime.strftime(date_object, '%m/%d/%y')
	
CONNECTION_STRING = config.get_config('db','x64_CONNECTION_STRING')
reader = csv.DictReader(open("C:\\Users\\sethw\\Desktop\\20110207.csv", "rb"))
inquiries = []
for row in reader:
	row["FULLNAME"] = "%s, %s %s" % (row["NAME_LAST"].strip(), row["NAME_FIRST"].strip(), row["NAME_MIDDLE"].strip())
	print row["FULLNAME"]
	print row["DSEMINQ-TRANSACTION_DATE"]
	try:
		row["DSEMINQ-TRANSACTION_DATE"] = convert_date(row["DSEMINQ-TRANSACTION_DATE"])
	except:
		row["DSEMINQ-TRANSACTION_DATE"] = row["DSEMINQ-TRANSACTION_DATE"]
	print row["DSEMINQ-TRANSACTION_DATE"]
	print row["MAIL_STREET"]
	print row["BIRTH_DATE"]
	try:
		row["BIRTH_DATE"] = convert_date(row["BIRTH_DATE"])
	except:
		row["BIRTH_DATE"] = row["BIRTH_DATE"]
	print row["BIRTH_DATE"]
	print row["MAIL_CITY"]
	print row["MAIL_COUNTRY"]
	print row["DSEMINQ-MAJOR"]
	print row["EMAIL"]
	print row["DSEMINQ-ENROLL_SESSION"]
	print row["DSEMINQ-ENROLL_YEAR"]
	print row["APP_FEE_PAID"]
	print row["NAME_FIRST"]
	print row["NAME_LAST"]
	print row["DSEMINQ-MAJOR"]
	print row["NAME_MIDDLE"]
	print row["PHONE"]
	print row["DSEMINQ-PHONE_TYPE"]
	print row["DSEMINQ-PREF_CONTACT"]
	print row["MAIL_STATE"]
	print row["DSEMINQ-TITLE"]
	print row["MAIL_ZIP"]	
	
	sql = "insert into apptmp_rec (app_source, add_date, stat, birth_date) values (?, DATE(?), ?, DATE(?))"
	params = ['WEB', row["DSEMINQ-TRANSACTION_DATE"], 'C', row["BIRTH_DATE"]]
	print sql
	print params
	
	db = odbc.odbc(CONNECTION_STRING)
	cur = db.cursor()
	cur.execute(sql, params)	
	cur.execute("select dbinfo('sqlca.sqlerrd1') from apptmp_rec")
	results = cur.fetchone()
	new_id = results[0]	
	
	sql = '''insert into app_idtmp_rec (id, fullname, addr_line1, city, st, zip, ctry, aa, title, ss_no, 
				phone, add_date, ofc_add_by, firstname, lastname, email) 
			 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, DATE(?), ?, ?, ?, ?)'''
	params = [new_id, row['FULLNAME'], row["MAIL_STREET"], row["MAIL_CITY"], row["MAIL_STATE"], row["MAIL_ZIP"], row["MAIL_COUNTRY"], 
			'HOME', row["DSEMINQ-TITLE"], row["SS_NUM"], row["PHONE"], row["DSEMINQ-TRANSACTION_DATE"], 'ADM', row["NAME_FIRST"], row["NAME_LAST"], row["EMAIL"]]
	print sql	
	print params
	
	cur.execute(sql, params)
	
	sql = "insert into app_proftmp_rec (id, birth_date, res_st, res_cty) values (?, DATE(?), ?, ?)"
	params = [new_id, row['BIRTH_DATE'], row['STATE'], row['CITY']]	
	#need some new logic in here that if STATE == '' then go to MAIL_STATE
	
	print sql, params
	cur.execute(sql, params)
			
	sql = '''insert into app_admtmp_rec (id, plan_enr_sess, plan_enr_yr, prog, subprog, add_date, ref_source, enrstat, major, major2, deg, app_source, jics_candidate)
		values (?,?,?,?,'NA', DATE(?),?,?,?,?,?,?)'''
	params = [new_id, row["DSEMINQ-ENROLL_SESSION"], row["DSEMINQ-ENROLL_YEAR"], 'MSTR', row["DSEMINQ-TRANSACTION_DATE"], row["DSEMINQ-HOW_HEARD"], 'INQUIRED', row["DSEMINQ-MAJOR"], 'NA', row["DSEMINQ-DEGREE"], 'WEB', 'N']
		
	print sql
	print params
	cur.execute(sql, params)
	
	sql = "insert into app_sitetmp_rec (id, beg_date, site, home) VALUES (?, DATE(?), ?, ?)"
	params = [new_id, row["DSEMINQ-TRANSACTION_DATE"], 'CARS', 'Y']
	print sql
	print params
	
	cur.execute(sql, params)
