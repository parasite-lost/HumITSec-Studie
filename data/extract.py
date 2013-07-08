#!/usr/bin/env python
# vim: set fileencoding=utf-8
# python version running: 2.7.5

from __future__ import division
import MySQLdb as mdb
import sys
import math

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
		"Mathemaik" : "Mathematik",
		"Masters" : "unbekannt",
		"Lehramt" : "unbekannt",
		None : "unbekannt"
		}
def subst(s):
	for k in sub:
		if s == k:
			return sub[k]
	return s

# standard deviation:
def sigma(liste):
	if liste == []:
		print "Error: std. dev. of empty list"
		return 0.0
	avg = sum(liste) / len(liste)
	sig = 0
	for i in liste:
		sig += (i - avg)**2
	sig /= len(liste)
	return math.sqrt(sig)


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

# count number of entries in database
def countall(cur):
	cur.execute("""select count(*) from %s""" % SQLTABLE)
	return cur.fetchone()[0]

# print number and percentage
def pnumperc(num, absnum):
	print "Anzahl: {:d}, Prozent: {:.2%}".format(num,(num / absnum))

def countnoidea(cur):
	cur.execute("""select count(*) from %s where was_email_krypto = 'Nein'""" % SQLTABLE)
	num = cur.fetchone()[0]
	absnum = countall(cur)
	cur.execute("""select studienfach, os_name from %s where was_email_krypto = 'Nein'""" % SQLTABLE)
	x = cur.fetchall()
	stud = {}
	for i in x:
		st = subst(i[0])
		if st in stud:
			stud[st] += 1
		else:
			stud[st] = 1
	print "Emailkryptographie unbekannt"
	pnumperc(num, absnum)
	for i in stud:
		print i, "\t", stud[i]
	print ""

def semnoidea(cur):
	cur.execute("""select num_semester from %s where was_email_krypto = 'Nein'""" % SQLTABLE)
	x = cur.fetchall()
	semlist = []
	for i in x:
		if i[0] != None:
			semlist.append(int(i[0]))
	print "semester für emailkryptographie unbekannt"
	print "Max:", max(semlist), "avg:", sum(semlist)/len(semlist), "std dev:", sigma(semlist)
	print ""

def os_clientnoidea(cur):
	cur.execute("""select os_name, client_thunderbird, client_outlook, client_opera,
			client_winmail, client_evolution, client_seamonkey, client_webseite,
			client_os_x_mail, client_sonstiges from %s where was_email_krypto = 'Nein'""" % SQLTABLE)
	x = cur.fetchall()
	getclients(x, 1, 10)
	for i in x:
		print i[0]

# print used clients for one line in database
clientslist = ["Thunderbird", "Outlook", "Opera", "Windows Live Mail", "Evolution", "Seamonkey", "Webclient", "OS X Mail"]
def pclients(entry, start, end):
	for i in range(start, end):
		if entry[i] == "Ja":
			print clientslist[i-2],
		elif entry[i] == "Nein" or entry[i] == None:
			pass
		else:
			print entry[i],
	print " ."

# print all clients used
def getclients(x, start, end):
	for i in x:
		pclients(i, start, end)

def countidea(cur):
	cur.execute("""select count(*) from %s where was_email_krypto = 'Ja'""" % SQLTABLE)
	num = cur.fetchone()[0]
	absnum = countall(cur)
	print "Begriff emailkrypto bekannt"
	pnumperc(num, absnum)
	print ""

def countreglm(cur):
	cur.execute("""select count(*) from %s where regelmaessig = 'Ja'""" % SQLTABLE)
	num = cur.fetchone()[0]
	absnum = countall(cur)
	cur.execute("""select studienfach, os_name, client_thunderbird, client_outlook, client_opera,
			client_winmail, client_evolution, client_seamonkey, client_webseite,
			client_os_x_mail, client_sonstiges from %s where regelmaessig = 'Ja'""" % SQLTABLE)
	x = cur.fetchall()
	stud = {}
	for i in x:
		st = subst(i[0])
		if st in stud:
			stud[st] += 1
		else:
			stud[st] = 1
	print "Emailkryptographie regelmäßig eingesetzt"
	pnumperc(num, absnum)
	for i in stud:
		print i, "\t", stud[i]
	getclients(x, 2, 11)
	print ""

def countnotreglm(cur):
	cur.execute("""select count(*) from %s where regelmaessig = 'Nein'""" % SQLTABLE)
	num = cur.fetchone()[0]
	absnum = countall(cur)
	print "emailkrypto nicht regelmäßig"
	pnumperc(num, absnum)
	print ""

def noteasy(cur):
	cur.execute("""select studienfach, os_name, client_thunderbird, client_outlook, client_opera,
			client_winmail, client_evolution, client_seamonkey, client_webseite,
			client_os_x_mail, client_sonstiges from %s where einfach = 'Nein'""" % SQLTABLE)
	x = cur.fetchall()
	print "Wer setzt Verschlüsselung regelmäßig ein, findet es aber schwierig"
	for i in x:
		print subst(i[0]),
		print i[1]
		pclients(i, 2, 11)
	print ""

def zusatzfragenreglm(cur):
	cur.execute("""select wievieledurchnitt, num_person_komm, einfach from %s where regelmaessig = 'Ja'""" % SQLTABLE)
	x = cur.fetchall()
	wieviele = []
	kontakte = []
	einfach = 0
	schwer = 0
	print "zusatzfragen für leute die regelmäßig verschlüsselte mails versenden:"
	for i in x:
		if i[0] != None:
			wieviele.append(i[0])
		if i[1] != None:
			kontakte.append(i[1])
		if i[2] == 'Ja':
			einfach += 1
		elif i[2] == 'Nein':
			schwer += 1
		else: pass
	print "#mails pro monat, avg:", sum(wieviele)/len(wieviele), "std dev:", sigma(wieviele), "range:", min(wieviele), max(wieviele)
	print "#kontakte, avg:", sum(kontakte)/len(kontakte) , "std dev:", sigma(kontakte), "range:", min(kontakte), max(kontakte)
	print "einfach:", einfach
	print "schwer:", schwer
	print ""

def countinst_notinst(cur):
	cur.execute("""select count(*) from %s where installiert = 'Ja'""" % SQLTABLE)
	inst = cur.fetchone()[0]
	cur.execute("""select count(*) from %s where installiert = 'Nein'""" % SQLTABLE)
	notinst = cur.fetchone()[0]
	absnum = countall(cur)

	print "installiert:"
	pnumperc(inst, absnum)
	print "not inst:"
	pnumperc(notinst, absnum)
	print ""

def countjemalssend_ornot(cur):
	cur.execute("""select count(*) from %s where jemals_send = 'Ja'""" % SQLTABLE)
	jem = cur.fetchone()[0]
	cur.execute("""select count(*) from %s where jemals_send = 'Nein'""" % SQLTABLE)
	notjem = cur.fetchone()[0]
	absnum = countall(cur)

	print "jemals -> Ja"
	pnumperc(jem, absnum)
	print "jemals -> Nein"
	pnumperc(notjem, absnum)
	print ""

def counthaskontakt(cur):
	cur.execute("""select count(*) from %s where kontakt = 'Ja'""" % SQLTABLE)
	kon = cur.fetchone()[0]
	cur.execute("""select count(*) from %s where kontakt = 'Nein'""" % SQLTABLE)
	nokon = cur.fetchone()[0]
	absnum = countall(cur)

	print "hat kontakte -> Ja"
	pnumperc(kon, absnum)
	print "hat kontakte -> Nein"
	pnumperc(nokon, absnum)
	print ""

def countwasinst(cur):
	cur.execute("""select count(*) from %s where warinstalliert = 'Ja'""" % SQLTABLE)
	wasinst = cur.fetchone()[0]
	cur.execute("""select count(*) from %s where warinstalliert = 'Nein'""" % SQLTABLE)
	wasnotinst = cur.fetchone()[0]
	absnum = countall(cur)

	print "war installiert -> Ja"
	pnumperc(wasinst, absnum)
	print "war installiert -> Nein"
	pnumperc(wasnotinst, absnum)
	print ""

def countbewentf(cur):
	cur.execute("""select count(*) from %s where bewusst_entfernt = 'Ja'""" % SQLTABLE)
	bewentf = cur.fetchone()[0]
	cur.execute("""select count(*) from %s where bewusst_entfernt = 'Nein'""" % SQLTABLE)
	notbewentf = cur.fetchone()[0]
	absnum = countall(cur)

	print "bewusst entfernt -> Ja"
	pnumperc(bewentf, absnum)
	print "bewusst entfernt -> Nein"
	pnumperc(notbewentf, absnum)
	print ""

def countgeplant(cur):
	cur.execute("""select count(*) from %s where geplant = 'Ja'""" % SQLTABLE)
	plan = cur.fetchone()[0]
	cur.execute("""select count(*) from %s where geplant = 'Nein'""" % SQLTABLE)
	notplan = cur.fetchone()[0]
	absnum = countall(cur)

	print "geplant -> Ja"
	pnumperc(plan, absnum)
	print "geplant -> Nein"
	pnumperc(notplan, absnum)
	print ""

def countversucht(cur):
	cur.execute("""select count(*) from %s where versucht = 'Ja'""" % SQLTABLE)
	vers = cur.fetchone()[0]
	cur.execute("""select count(*) from %s where versucht = 'Nein'""" % SQLTABLE)
	notvers = cur.fetchone()[0]
	absnum = countall(cur)

	print "versucht -> Ja"
	pnumperc(vers, absnum)
	print "versucht -> Nein"
	pnumperc(notvers, absnum)
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
				if sys.argv[1] == "count":
					cur.execute("""select count(*) from %s""" % SQLTABLE)
					print cur.fetchone()[0]
				if sys.argv[1] == "exec":
					cur.execute(sys.argv[2])
					print cur.fetchall()
			else:
				#studienfach(cur)
				#betriebssystem(cur)
				#countnoidea(cur)
				#semnoidea(cur)
				#os_clientnoidea(cur)
				#countidea(cur)
				#countreglm(cur)
				#noteasy(cur)
				#zusatzfragenreglm(cur)
				#countnotreglm(cur)
				#countinst_notinst(cur)
				#countjemalssend_ornot(cur)
				#counthaskontakt(cur)
				#countwasinst(cur)
				#countbewentf(cur)
				countgeplant(cur)
				countversucht(cur)
				
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
