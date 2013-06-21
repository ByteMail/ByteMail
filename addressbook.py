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
    if entryname == "" or address == "":
        pass
    else:
        db.addressdb.insert("addresses",{entryname:address})

def addresses():
    addresses = db.addressdb.find("addresses", "all")
    addresses_ = "\n"
    for x in addresses:
        name, addr = "", ""
        for y in x:
            name = y
            addr = x[y]
        a = "{0} {1}\n".format(name, addr)
        addresses_ = addresses_ + a
    return addresses_
