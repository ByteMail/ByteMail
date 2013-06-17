import hashlib
import time
import uuid
import db
def find_antispam(to, addr, message,difficulty):
	if difficulty == 5:
		print "Generating antispam on average difficulty (5)"
	else:
		print "Generaring antispam on an elevated difficulty (" + str(difficulty) + ".) This is probably because your message is a kilobyte or larger. This may take a while..."
	nonce = str(int(time.time()))
	basestring = to + addr + message + nonce
	currenthash = ""
	num = 0
	while not currenthash.startswith('0'*difficulty):
		currenthash = hashlib.sha1(basestring + str(num)).hexdigest()
		num += 1
	num -= 1
	return str(num),nonce

def check_antispam(to,addr,message,num,nonce,difficulty):
	targetstring = to + addr + message + nonce + num
	if hashlib.sha1(targetstring).hexdigest().startswith('0'*difficulty):
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


def get_required_difficulty(msg):
	difficulty = int(4)
	difficulty += len(msg) / 1024
	if difficulty == 4:
		return 5
	return difficulty
	
