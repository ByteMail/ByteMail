import db
import ssl
import json
import uuid
from rsa import *
import base64
import antispam
import aes
def message(obj, ip, data):
    addr = db.data.find("data", "all")[0]['addr']
    msg = data['message']
    from_ = data['from']
    title = data['title']
    to = data['to']
    id = data['id']
    as_nonce = data['nonce']
    as_num = data['num']
    key = data['key']
    if antispam.check_antispam(to,from_,msg,as_num,as_nonce,antispam.get_required_difficulty(msg)):
	    if len(from_) == 32 and len(to) == 32:
        	db.messages.insert("messages", {"id":id, "message":msg, "from":from_, "title":title, "to":to,"as_num":as_num,"as_nonce":as_nonce,"key":key})
	        if to == addr:
       		    print "\nYou have a new message from", from_
def send_msg(msg, title, to, addr):
    try:
        data = db.nodes.find("nodes", {"addr":to})[0]
    except:
        return "Address doesn't exist"
    if data['publickey'].startswith("PublicKey(") and data['publickey'].endswith(")"):
       # msg = encrypt(msg, eval(data['publickey'])) <--- Old encryption code
	aeskey = str(uuid.uuid4().hex) # Generate new AES Key
	key = encrypt(aeskey, eval(data['publickey'])) # Encrypt AES key with target's RSA Public Key
	key = base64.b64encode(key) # Base64 encode the key
	msg = aes.encryptData(aeskey,msg) # Encrypt Message with AES Key
        msg = base64.b64encode(msg) # Base64 encode the message
	as_num, as_nonce = antispam.find_antispam(to,addr,msg,antispam.get_required_difficulty(msg))
    else:
        return "Invalid public key for", addr
    id = ""
    while True:
        id = uuid.uuid4().hex
        if db.messages.find("messages", {"id":id}):
            continue
        else:
            break
    print "Sending message ID " + id + " with key " + key
    nodes = db.nodes.find("nodes", "all")
    for x in nodes:
        s = ssl.socket()
        try:
            s.settimeout(1)
            s.connect((x['ip'], x['port']))
            s.send(json.dumps({"cmd":"message", "id":id, "message":msg, "title":title, "to":to, "from":addr,"num":as_num,"nonce":as_nonce,"key":key}))
            s.close()
        except Exception, error:
            db.unsent.insert("unsent", {"to":[x['ip'], x['port']], "message":{"cmd":"message", "id":id, "message":msg, "title":title, "to":to, "from":addr,"num":as_num,"nonce":as_nonce,"key":key}})
    return "Message Sent!"

