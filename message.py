import db
import ssl
import json
import uuid
from rsa import *
import base64
import antispam

def message(obj, ip, data):
    addr = db.data.find("data", "all")[0]['addr']
    msg = data['message']
    from_ = data['from']
    title = data['title']
    to = data['to']
    id = data['id']
    as_nonce = data['nonce']
    as_num = data['num']
    if antispam.check_antispam(to,from_,msg,as_num,as_nonce):
	    if len(from_) == 32 and len(to) == 32:
	        db.messages.insert("messages", {"id":id, "message":msg, "from":from_, "title":title, "to":to,"as_num":as_num,"as_nonce":as_nonce})
	        if to == addr:
        	    print "\nYou have a new message from", from_
    else:
	    print "Blocked some spam."

def send_msg(msg, title, to, addr):
    try:
        data = db.nodes.find("nodes", {"addr":to})[0]
    except:
        return "Address doesn't exist"
    if data['publickey'].startswith("PublicKey(") and data['publickey'].endswith(")"):
        msg = encrypt(msg, eval(data['publickey']))
        msg = base64.b64encode(msg)
	as_num, as_nonce = antispam.find_antispam(to,addr,msg)
    else:
        return "Invalid public key for", addr
    id = ""
    while True:
        id = uuid.uuid4().hex
        if db.messages.find("messages", {"id":id}):
            continue
        else:
            break

    nodes = db.nodes.find("nodes", "all")
    for x in nodes:
        s = ssl.socket()
        try:
            s.settimeout(1)
            s.connect((x['ip'], x['port']))
            s.send(json.dumps({"cmd":"message", "id":id, "message":msg, "title":title, "to":to, "from":addr,"num":as_num,"nonce":as_nonce}))
            s.close()
        except Exception, error:
            db.unsent.insert("unsent", {"to":[x['ip'], x['port']], "message":{"cmd":"message", "id":id, "message":msg, "title":title, "to":to, "from":addr,"num":as_num,"nonce":as_nonce}})
    return "Message Sent!"

