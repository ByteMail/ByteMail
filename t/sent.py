import db

def sent():
    try:
        data = db.sent.find("sent", "all")
    except:
        return "You haven't sent any messages."
    else:
        if data:
            data_ = "\n"
            for x in data:
                if "time" in x:
                    check = "\tID: {0} \n\tTime: {3} \n\tTo: {1} \n\tTitle: {2}".format(x['id'], x['to'], x['title'], x['time'])
                    data_ = data_ + check+"\n\n"
                else:
                    check = "\tID: {0} \n\tTo: {1} \n\tTitle: {2}".format(x['id'], x['to'], x['title'])
                    data_ = data_ + check+"\n\n"
            return data_
        else:
            return "You haven't sent any messages."


def sent_delete(id):
    try:
        data = db.sent.find("sent", {"id":id})[0]
    except:
        return "Message with that ID does not exist"
    else:
        db.sent.remove("sent", data)
        return "Message Removed!"

