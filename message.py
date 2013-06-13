import db
import ssl
import json
import uuid

def message(obj, ip, data):
    addr = db.data.find("data", "all")[0]['addr']
    msg = data['message']
    from_ = data['from']
    title = data['title']
    to = data['to']
    id = data['id']
    if len(from_) == 32 and len(to) == 32:
        db.messages.insert("messages", {"id":id, "message":msg, "from":from_, "title":title, "to":to})
        if to == addr:
            print "\nYou have a new message from", from_

def send_msg(msg, title, to, addr):
    try:
        data = db.nodes.find("nodes", {"addr":to})[0]
    except:
        return "Address doesn't exist"
    
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
            s.send(json.dumps({"cmd":"message", "id":id, "message":msg, "title":title, "to":to, "from":addr}))
            s.close()
        except Exception, error:
            db.unsent.insert("unsent", {"to":[x['ip'], x['port']], "message":{"cmd":"message", "id":id, "message":msg, "title":title, "to":to, "from":addr}})
    return "Message Sent!"

