import db

def check_entry(entryname):
	ourdb = db.addressdb.find("addresses","all")
	for x in ourdb:
		try:
			return x[entryname]
		except Exception, error:
			pass
	return None

def add_entry(entryname,address):
	db.addressdb.insert("addresses",{entryname:address})

