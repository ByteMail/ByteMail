import landerdb
import ssl
import json
import db
import time

def unsent():
    #{'unsent':[{'to':[ip, port], 'message':{}]}
    while True:
        messages = db.unsent.find("unsent", "all")
        if messages:
            for x in messages:
                to = tuple(x['to'])
                message = x['message']
                s = ssl.socket()
                try:
                    s.settimeout(2)
                    s.connect(to)
                except:
                    s.close()
                    continue
                else:
                    s.send(json.dumps(message))
                    s.close()
                    db.unsent.remove("unsent", x)
        time.sleep(60)

                    
