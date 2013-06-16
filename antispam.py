import hashlib
import time
import uuid
import db
def find_antispam(to, addr, message):

	nonce = str(int(time.time()))
	basestring = to + addr + message + nonce
	currenthash = ""
	num = 0
	while not currenthash.startswith('00000'):
		currenthash = hashlib.sha1(basestring + str(num)).hexdigest()
		num += 1
	num -= 1
	return str(num),nonce

def check_antispam(to,addr,message,num,nonce):
	targetstring = to + addr + message + nonce + num
	if hashlib.sha1(targetstring).hexdigest().startswith('00000'):
		try:
			if nonce in db.nonces.find(addr,"all"):
				return False
			else:
				db.nonces.insert(addr, nonce)
		except Exception, error:
			db.nonces.insert(addr,nonce)

		return True
	else:
		return False

