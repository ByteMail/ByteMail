import db

def check(addr):
    messages = []
    b = db.messages.find("messages", {"to":addr})
    if b:
        for x in b:
            try:
                time_ = x['time']
            except Exception, error:
                time_ = "Unknown"

            if "message" in x:
                message = """
            
            ID: {2}
            Time: {3}
            From: {0}
            Title: {1}

                """.format(x['from'], x['title'], x['id'], time_)
                messages.append(message)
    return messages
