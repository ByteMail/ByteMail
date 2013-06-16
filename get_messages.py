import ssl
import json
import db

def get_messages(obj, ip, data):
    with open("messages.db", 'rb') as file:
        for x in file.readlines():
            obj.send(x)
    obj.close()


def send_get_messages(ip, port):
    sock = ssl.socket()
    sock.connect((ip, port))
    sock.send(json.dumps({"cmd":'get_messages'}))
    with open("messages.db", 'wb') as file:
        while True:
            data = sock.recv(1024)
            if data:
                file.write(data)
            else:
                break
    sock.close()
