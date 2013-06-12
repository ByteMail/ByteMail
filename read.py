import db

def read(id, addr):
    data = db.messages.find("messages", {"to":addr})
    for x in data:
        try:
            if x['id'] == id:
                msg = """

                ID: {0}
                From: {1}
                Title: {2}

                {3}


                """.format(x['id'], x['from'], x['title'], x['message'])
                return msg

        except KeyError:
            continue

    return "Message with that ID doesn't exist"
