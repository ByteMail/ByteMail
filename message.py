import db
import ssl
import json
import uuid
from rsa import *
import base64
import antispam
import aes
import time

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
    signature = data['signature']
    if "time" in data:
        time_ = data['time']
    else:
        time_ = "Unknown"

    try:
        data = db.nodes.find("nodes", {"addr":from_})[0]
    except:
        return
    if data['publickey'].startswith("PublicKey(") and data['publickey'].endswith(")"):
        try:
            decodedsig = base64.b64decode(signature)
            verify(msg + to, decodedsig, eval(data['publickey']))
        except Exception, error:
            return
    if antispam.check_antispam(to,from_,msg,as_num,as_nonce,antispam.get_required_difficulty(msg)):
	    if len(from_) == 32 and len(to) == 32:
                message = {"id":id, 
                    "time":time_, 
                    "message":msg, 
                    "from":from_, 
                    "title":title,
                    "to":to,
                    "as_num":as_num,
                    "as_nonce":as_nonce,
                    "key":key,
                    "signature":signature}
	        db.messages.insert("messages", message)
            if to == addr:
                check = db.addressdb.find("addresses", 'all')
                done = False
                for x in check:
                    for y in x:
                        if x[y] == from_:
                            print "\nYou have a new message from", y
                            done = True
                if not done:
       		        print "\nYou have a new message from", from_
def send_msg(msg, title, to, addr):
    # Copied and pasted from read.py
    my_key = db.data.find("data", "all")[0]["privatekey"]
    if my_key.startswith("PrivateKey(") and my_key.endswith(")"):
        my_key = eval(my_key)

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
	as_num, as_nonce = antispam.find_antispam(to,addr,msg,antispam.get_required_difficulty(msg)) # Generate the AntiSpam
        signature = base64.b64encode(sign(msg + to,my_key,"SHA-1")) # Sign the message
    else:
        return "Invalid public key for", addr
    id = ""
    while True:
        id = uuid.uuid4().hex
        if db.messages.find("messages", {"id":id}):
            continue
        else:
            break
    print "Sending message ID " + id + " with key " + key + " and signature " + signature
    nodes = db.nodes.find("nodes", "all")
    t = time.localtime()
    time_ = "{0}/{1}/{2} {3}:{4}:{5}".format(t[1], t[2], t[0], t[3], t[4], t[5])
    for x in nodes:
        s = ssl.socket()
        try:
            s.settimeout(1)
            s.connect((x['ip'], x['port']))
            s.send(json.dumps({"cmd":"message", "time":time_ ,"id":id, "message":msg, "title":title, "to":to, "from":addr,"num":as_num,"nonce":as_nonce,"key":key,"signature":signature}))
            s.close()
        except Exception, error:
            db.unsent.insert("unsent", {"to":[x['ip'], x['port']], "message":{"cmd":"message", "time":time_, "id":id, "message":msg, "title":title, "to":to, "from":addr,"num":as_num,"nonce":as_nonce,"key":key,"signature":signature}})
    db.sent.insert("sent", {"id":id, "title":title, "to":to, "time":time_})
    return "Message Sent!"

