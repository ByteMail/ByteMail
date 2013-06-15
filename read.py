import db
from rsa import *
import base64

def read(id, addr):
    data = db.messages.find("messages", {"to":addr})
    my_key = db.data.find("data", "all")[0]["privatekey"]
    if my_key.startswith("PrivateKey(") and my_key.endswith(")"):
        my_key = eval(my_key)
    else:
        return "You have an invalid key."
    for x in data:
        try:
            if x['id'] == id:
                msg = """

                ID: {0}
                From: {1}
                Title: {2}

                {3}


                """.format(x['id'], x['from'], x['title'], decrypt(base64.b64decode(x['message']), my_key))
                return msg

        except KeyError:
            continue

    return "Message with that ID doesn't exist"
