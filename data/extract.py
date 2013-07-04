#!/usr/bin/env python
# python version running: 2.7.5
# -*- encoding: utf-8

import MySQLdb as mdb
import sys

################################
#          DB DATA             #
################################
SQLUSER = "humitsec"          ##
SQLPASSWD = "humitsecpasswd"  ##
SQLHOST = "127.0.0.1"         ##
SQLDB = "humitsec"            ##
SQLTABLE = "emailcrypt"       ##
################################
#                              #
################################


sub = {	"Computational Engineering" : "CE",
		"Lehramt Informatik" : "Inf",
		"Informatik PhD" : "Inf",
		"Informatik (Master)" : "Inf",
		"Master Informatik" : "Inf",
		"Informatik MA" : "Inf",
		"informatik" : "Inf",
		"Informatik" : "Inf",
		"Inf Master" : "Inf",
		"Wirtschaftsinformatik Promotion" : "WInf",
		"Wirtschaftsinformatik" : "WInf",
		"maschinenbau" : "MB",
		"Maschinenbau" : "MB",
		"Maschinenbau (Master)" : "MB",
		"mb" : "MB",
		"WIrtschaftsingenieurwesen" : "WIng",
		"Wirtschaftsingenieurwesen" : "WIng",
		"wing" : "WIng",
		"Wing" : "WIng",
		"WING" : "WIng",
		"Chemie und Bioingenieurwesen" : "CBI",
		"Chemie-Bioingenieurswesen" : "CBI",
		"Chemie- und Bioingenieurwesen" : "CBI",
		"Chemie- Bioingeniuerwesen" : "CBI",
		"Chemie- und Bioingenierwesen" : "CBI",
		"Chemie- und Bioingenieurswesen" : "CBI",
		"Chemie- und Bioingenieurwesen " : "CBI",
		"Cbi " : "CBI",
		"Chemieingenieur" : "CEN",
		"Chemical Engineering" : "CEN",
		"Life Science Engineering" : "LSE",
		"Medizintechnik, Schwerpunkt Informatik" : "MedTech",
		"Medizintechnik " : "MedTech",
		"Medizintechnik" : "MedTech",
		"Life scienece Engineering" : "LSE",
		"Elektrotechnik, Elektronik und Informationstechnik" : "EEI",
		"Elektrotechnik-Elektronik-Informationstechnik" : "EEI",
		"Master EEI" : "EEI",
		"Masterstudiengang Advanced Materials and Processes " : "MAP",
		"MSc IIS" : "IIS",
		"International Information Systems" : "IIS",
		"materialwissenschaft" : "Materialwissenschaften",
		"International Production Engineering and Management" : "IPEM",
		"international production Engineering and Management" : "IPEM",
		"Informations- und Kommunikationstechnik" : "IuK",
		"Materialwissenschaften und Werkstofftechnik" : "Materialwissenschaften",
		"Materialwissenschaft" : "Materialwissenschaften",
		"Materialwissenschaft und Werkstofftechnik" : "Materialwissenschaften",
		"Masters" : "unbekannt",
		"Lehramt" : "unbekannt",
		None : "unbekannt"
		}
def subst(s):
	for k in sub:
		if s == k:
			return sub[k]
	return s



def studienfach(cur):
	cur.execute("""select studienfach from %s""" % SQLTABLE)
	x = cur.fetchall()
	stud = {}
	print "studienfach:"
	for i in x:
		st = subst(i[0])
		
		if st in stud:
			stud[st] += 1
		else:
			stud[st] = 1
	for i in stud:
		print i, " : ", stud[i]
	print ""

def betriebssystem(cur):
	cur.execute("""select os_name from %s""" % SQLTABLE)
	oses = {}
	for i in cur.fetchall():
		if i[0] in oses:
			oses[i[0]] += 1
		else:
			oses[i[0]] = 1
	print "Betriebssysteme:"
	for i in oses:
		print i, " : ", oses[i]
	print ""

if __name__ == "__main__":
	# connect to DB
	con = None
	cur = None
	try:
		con = mdb.connect(host=SQLHOST,
			user=SQLUSER, passwd=SQLPASSWD, db=SQLDB)
		with con:
			cur = con.cursor()
			############################################
			# fill in functions with select statements #
			############################################
			if len(sys.argv) > 1:
				if sys.argv[1] == "showtable":
					cur.execute("""show columns from %s""" % SQLTABLE)
					for i in cur.fetchall():
						print i[0]
			else:
				studienfach(cur)
				betriebssystem(cur)
			############################################
			#                  end                     #
			############################################

	except mdb.Error as e:
		print "Error:", e

	finally:
		if cur:
			cur.close()
		if con:
			con.close()