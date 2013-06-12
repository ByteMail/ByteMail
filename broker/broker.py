import ssl
import socket
import json
import threading
import landerdb

class Broker:

    def __init__(self):
        self.port = 4321
        self.db = landerdb.Connect("nodes.db")
    def main(self):
        s = ssl.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", self.port))
        s.listen(5)
        while True:
            obj, conn = s.accept()
            threading.Thread(target=self.handle, args=(obj, conn[0])).start()
    def handle(self, obj, ip):
        data = obj.recv(1024)
        print data
        if data:
            data = json.loads(data)
            port = data['port']
            addr = data['addr'].replace("\n", '').replace(" ", '')
            if len(addr) == 32:
                self.db.insert("nodes", {"addr":addr, "ip":ip, "port":port})
                with open("nodes.db", 'r') as file:
                    for x in file.readlines():
                        obj.send(x)
                    obj.close()
            else:
                obj.close()

Broker().main()
