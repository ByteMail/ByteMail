import socket                                                                                                                         
import db
import checkin
import message
import read
import check
import json
import threading
import os
import uuid
import cmd
import thread
import unsent
import delete
import ssl
import get_messages
import get_nodes
import time
import random
import rsa
import addressbook

__version__ = "0.2.81"

class ByteMail:
    
    def __init__(self, addr, pubkey):
        self.cmds = {
                "delete":delete.delete,
                "checkin":checkin.checkin,
                "message":message.message,
                "get_messages":get_messages.get_messages,
                "get_nodes":get_nodes.get_nodes,
                }
        self.broker = ("198.147.20.190", 4321)
        self.addr = addr
        self.pubkey = pubkey
        self.port = 5333
        self.host = "0.0.0.0"
        self.open_port = False
        self.config = {
                "relay":True
                }
    def main(self): 
        if not db.nodes.find("nodes", "all"):
            check = self.config['relay']
            if check:
                self.open_port = True
                print "You are running as a relay node."
            db.data.insert("data", {"port":self.port})
            print "Downloading Nodes..."
            self.get_nodes()
            print "Checking in to nodes..."
            self.send_checkin()
            print "Done!"
        
        check = self.config['relay']
        if check:
            self.open_port = True
            print "You are running as a relay node."
        else:
            print "You are not running as a relay node."
        if self.open_port:
            sock = ssl.socket()
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(5)
            while True:
                obj, conn = sock.accept()
                threading.Thread(target=self.handle, args=(obj, conn[0])).start()
        else:
            while True:
                check = db.nodes.find("nodes", "all")
                random.shuffle(check)
                node = None
                for x in check:
                    s = ssl.socket()
                    try:
                        s.connect((x['ip'], x['port']))
                    except:
                        s.close()
                        continue
                    else:
                        node = (x['ip'], x['port'])
                        s.close()
                        break

                sock = ssl.socket()
                try:
                    sock.connect(node)
                except:
                    continue
                else:
                    while True:
                        try:
                            get_messages.send_get_messages(x['ip'], x['port'])
                            get_nodes.send_get_nodes(x['ip'], x['port'])
                            time.sleep(10)
                        except Exception, error:
                            sock.close()
                            break

    def handle(self, obj, ip):
        data = obj.recv(102400)
        if data:
            data = json.loads(data)
            self.cmds[data['cmd']](obj, ip, data)

    def send_checkin(self):
        nodes = db.nodes.find("nodes", "all")
        for x in nodes:
            s = ssl.socket()
            try:
                s.settimeout(1)
                s.connect((x['ip'], x['port']))
                s.send(json.dumps({"cmd":"checkin", "addr":self.addr, "port":self.port, "publickey":self.pubkey}))
                s.close()
            except Exception, error:
                s.close()
                db.unsent.insert("unsent",  {"to":[x['ip'], x['port']], "message":{"cmd":"checkin", "addr":self.addr, "port":self.port, "publickey":self.pubkey}}) 

    def get_nodes(self):
        send = {"addr":self.addr, "port":self.port, "publickey":self.pubkey}
        s = ssl.socket()
        s.connect(self.broker)
        s.send(json.dumps(send))
        with open("nodes.db", 'wb') as file:
            while True:
                data = s.recv(1024)
                if data:
                    file.write(data)
                else:
                    break
        print "Downloaded Nodes!"

class Prompt(cmd.Cmd):
    prompt = "ByteMail$ "
    
    def do_send(self, line):
        addr = db.data.find("data", "all")[0]['addr']
        to = raw_input("To: ")
	if len(to) != 32:
		if len(str(addressbook.check_entry(to))) != 32:
			print "Address Invalid."
			return
		else:
			to = str(addressbook.check_entry(to))
        title = raw_input("Title: ")
        msg = raw_input("Message: ")
        if not to or not title or not msg:
            print "You need to fill out all the fields."
        else:
	    print message.send_msg(msg, title, to, addr)
    def do_check(self, line):
        addr = db.data.find("data", "all")[0]['addr']
        check_ = check.check(addr)
        if not check_:
            print "You have no messages."
        else:
            for x in check_:
                print x

    def do_read(self, id):
        addr = db.data.find("data", "all")[0]['addr']
        print read.read(id, addr)

    def do_addr(self, line):
        addr = db.data.find("data", "all")[0]['addr']
        print "Your address is:", addr

    def do_add_address(self, line):
	name = raw_input("Name: ")
	address = raw_input("Address: ")
	addressbook.add_entry(name,address)

    def do_delete(self, line):
        addr = db.data.find("data", "all")[0]['addr']
        print delete.send_delete(line, addr)

    def do_exit(self, line):
        print "Bye!"
        exit()

if __name__ == "__main__":
    exists = db.data.find("data", "all")
    if not exists:
        print "First time running ByteMail"
        print "Generating new keys... This could take a while."
        publickey, privatekey = rsa.newkeys(512)
        db.data.insert("data", {"addr":uuid.uuid4().hex, "publickey":str(publickey), "privatekey":str(privatekey)})
        db.messages.insert("messages", {})
        data = db.data.find("data", "all")[0]
        addr = data['addr']
        pubkey = data['publickey']
    else:
        data = db.data.find("data", "all")[0]
        addr = data['addr']
        pubkey = data['publickey']

    b = ByteMail(addr, pubkey)
    c = Prompt()
    thread.start_new_thread(b.main, ())
    thread.start_new_thread(unsent.unsent, ())
    while True:
        try:
            c.cmdloop()
        except KeyboardInterrupt:
            continue
