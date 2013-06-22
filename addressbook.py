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
        return
    else:
        check = db.addressdb.find("addresses", "all")
        done = False
        for x in check:
            for y in x:
                if y == entryname:
                    db.addressdb.remove("addresses", x)
                    db.addressdb.insert("addresses", {entryname:address})
                    done = True
                    break
            if done:
                break
        if not done:
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

def remove_address(entryname):
    
    check = db.addressdb.find("addresses", "all")
    for x in check:
        for y in x:
            if y == entryname:
                db.addressdb.remove("addresses", x)
    return "Address Deleted"
