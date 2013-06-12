import db
import ssl
import json

def delete(obj, ip, data):
    message = db.messages.find("messages", {"to":addr,"id":id})
    for x in messages:
        if x['to'] == data['to'] and x['id'] == id:
            db.messages.remove("messages", x)
            break


def send_delete(addr, id):
    message = db.messages.find("messages", {"to":addr,"id":id})
    if not message:
        return "Message with that ID doesn't exist."
    else:
        nodes = db.nodes.find("messages", "all")
        for x in nodes:
            try:
                sock = ssl.socket()
                sock.connect((x['ip'], x['port']))
                sock.send(json.dumps({"cmd":"delete", "to":addr, "id":id}))
            except:
                db.unsent.insert("unsent", {"cmd":"delete", "addr":addr, "id":id})
            sock.close()
        return "Message Removed!"
