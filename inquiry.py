#!/usr/bin/python
'''
	Processes and parses the inquiry information
'''
import odbc, csv, config, re
from datetime import datetime

CONNECTION_STRING = str(config.get_config('db','x64_CONNECTION_STRING'))
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
	
	potential_duplicate = False
	
	if len(results) > 0:
		for result in results:
			#if (result[3].strip() == middle)):
			if re.sub('\.','',result[3]).strip() == middle:			
				potential_duplicate = True
				result.append('Matched Middle Initial')
			if result[4].strip() == state:
				result.append('Matched State')	
				potential_dupilcate = True				
	
	return result, potential_duplicate				
	
def process(filename):	
	
	reader = csv.DictReader(open(filename, "rb"))
	inquiries = []
	for row in reader:
		row["FULLNAME"] = "%s, %s %s" % (row["NAME_LAST"].strip(), row["NAME_FIRST"].strip(), row["NAME_MIDDLE"].strip())		
		dup_info, isdup = scan_dupe(row["NAME_LAST"].strip(), row["NAME_FIRST"].strip(), row["NAME_MIDDLE"].strip(), row["STATE"].strip())
		if isdup is not True:
			try:
				row["DSEMINQ-TRANSACTION_DATE"] = convert_date(row["DSEMINQ-TRANSACTION_DATE"])
			except:
				row["DSEMINQ-TRANSACTION_DATE"] = row["DSEMINQ-TRANSACTION_DATE"]		
			try:
				row["BIRTH_DATE"] = convert_date(row["BIRTH_DATE"])
			except:
				row["BIRTH_DATE"] = row["BIRTH_DATE"]		
			sql = "insert into apptmp_rec (app_source, add_date, stat, birth_date) values (?, DATE(?), ?, DATE(?))"
			params = ['WEB', row["DSEMINQ-TRANSACTION_DATE"], 'C', row["BIRTH_DATE"]]								
			cur.execute(sql, params)	
			cur.execute("select dbinfo('sqlca.sqlerrd1') from apptmp_rec")
			results = cur.fetchone()
			new_id = results[0]			
			sql = '''insert into app_idtmp_rec (id, fullname, addr_line1, city, st, zip, ctry, aa, title, ss_no, 
						phone, add_date, ofc_add_by, firstname, lastname, email) 
					 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, DATE(?), ?, ?, ?, ?)'''
			params = [new_id, row['FULLNAME'], row["MAIL_STREET"], row["MAIL_CITY"], row["MAIL_STATE"], row["MAIL_ZIP"], row["MAIL_COUNTRY"], 
					'HOME', row["DSEMINQ-TITLE"], row["SS_NUM"], row["PHONE"], row["DSEMINQ-TRANSACTION_DATE"], 'ADM', row["NAME_FIRST"], row["NAME_LAST"], row["EMAIL"]]		
			cur.execute(sql, params)
			
			sql = "insert into app_proftmp_rec (id, birth_date, res_st, res_cty) values (?, DATE(?), ?, ?)"
			params = [new_id, row['BIRTH_DATE'], row['STATE'], row['CITY']]	
			#need some new logic in here that if STATE == '' then go to MAIL_STATE		
			cur.execute(sql, params)
					
			sql = '''insert into app_admtmp_rec (id, plan_enr_sess, plan_enr_yr, prog, subprog, add_date, ref_source, enrstat, major, major2, deg, app_source, jics_candidate)
				values (?,?,?,?,?, DATE(?),?,?,?,?,?,?,?)'''
			params = [new_id, row["DSEMINQ-ENROLL_SESSION"], row["DSEMINQ-ENROLL_YEAR"], 'MSTR', 'NA', row["DSEMINQ-TRANSACTION_DATE"], row["DSEMINQ-HOW_HEARD"], 'INQUIRED', row["DSEMINQ-MAJOR"], 'NA', row["DSEMINQ-DEGREE"], 'WEB', 'N']
			cur.execute(sql, params)
			
			sql = "insert into app_sitetmp_rec (id, beg_date, site, home) VALUES (?, DATE(?), ?, ?)"
			params = [new_id, row["DSEMINQ-TRANSACTION_DATE"], 'CARS', 'Y']
			
			cur.execute(sql, params)
		else:
			
