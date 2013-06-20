import db
import ssl
import json

def delete(obj, ip, data):
    message = db.messages.find("messages", {"id":data['id']})
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
        for x in nodes:
            try:
                sock = ssl.socket()
                sock.settimeout(1)
                sock.connect((x['ip'], x['port']))
                sock.send(json.dumps({"cmd":"delete", "to":addr, "id":id}))
            except:
                db.unsent.insert("unsent", {"to":[x['ip'], x['port']], "message":{"cmd":"delete", "addr":addr, "id":id}})
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
