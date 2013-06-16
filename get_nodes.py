import ssl
import json
import db

def get_nodes(obj, ip, data):
    with open("nodes.db", 'rb') as file:
        obj.sendall(file.read())
    obj.close()


def send_get_nodes(ip, port):
    sock = ssl.socket()
    sock.connect((ip, port))
    sock.send(json.dumps({"cmd":'get_nodes'}))
    with open("nodes.db", 'wb') as file:
        while True:
            data = sock.recv(1024)
            if data:
                file.write(data)
            else:
                break
    sock.close()
