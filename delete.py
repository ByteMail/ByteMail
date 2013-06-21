import db
import ssl
import json
from rsa import *
import base64

def delete(obj, ip, data):
    message = db.messages.find("messages", {"id":data['id']})
    pubkey_expression = db.nodes.find("nodes", {"addr":data['to']})[0]['publickey']
    if pubkey_expression.startswith("PublicKey(") and pubkey_expression.endswith(")"):
        try:
            verify("delete" + data['id'], base64.b64decode(data['signature']),eval(pubkey_expression))
        except Exception, error:
            return
    try:
        db.messages.remove("messages", message[0])
    except IndexError:
        pass

def send_delete(id, addr):
    message = db.messages.find("messages", {"id":id})
    if not message:
        return "Message with that ID doesn't exist."
    else:
       db.messages.remove("messages", message[0])
       nodes = db.nodes.find("nodes", "all")
       signature = base64.b64encode(sign("delete" + id, eval(db.data.find("data","all")[0]['privatekey']),"SHA-1"))
       for x in nodes:
            try:
                sock = ssl.socket()
                sock.settimeout(1)
                sock.connect((x['id'], x['port']))
                sock.send(json.dumps({"cmd":"delete", "to":addr, "id":id, "signature":signature}))
            except:
                db.unsent.insert("unsent", {"to":[x['ip'], x['port']], "message":{"cmd":"delete", "addr":addr, "id":id, "signature":signature}})
            sock.close()
       return "Message Removed!"

def send_delete_all(addr):
    messages = db.messages.find("messages", {"to":addr})
    if not messages:
        return "No messages to delete!"
    else:
        for msg in messages:
            send_delete(msg['id'],addr)
    return "Success!"
