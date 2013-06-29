from flask import Flask, redirect, render_template, request
import db
import message
import random
import read
import delete

app = Flask(__name__)
try:
    addr = db.data.find("data", "all")[0]['addr']
except TypeError:
    addr = "Unknown"

def check():
    c = db.messages.find("messages", "all")
    messages = []
    for x in c:
        if 'to' in x:
            if x['to'] == addr:
                messages.append(x)
    return messages


@app.route("/")
def index():
    message = check()
    message.reverse()
    return render_template("index.html", messages=message, num=str(len(message)), addr=addr)

@app.route("/sent/")
def sent():
    c = db.sent.find("sent", "all")
    message = []
    for x in c:
        message.append(x)
    message.reverse()
    return render_template("sent.html", messages=message, num=str(len(check())), addr=addr)
@app.route("/read/<id>")
def read_(id):
    data = read.read(id, addr).split()
    id = data[1]
    date = data[3]
    time = data[4]
    title = data[8]
    from_ = data[6]
    message = ' '.join(data[9:])
    num = check()
    return render_template("read.html", num=str(len(num)), id=id, time=time, from_=from_, message=message, title=title)

@app.route("/send/", methods=['GET', 'POST'])
def send():
    num = check()
    if request.method == 'POST':
        to = request.form['to']
        if len(to) != 32:
            check_ = db.addressdb.find("addresses", "all")
            for x in check_:
                for y in x:
                    if y == to:
                        to = x[y]
        title = request.form['title']
        msg = request.form['message']
        check_ = message.send_msg(msg, title, to, addr)
        check_ = """<script>alert("{0}");window.location = '/';</script>""".format(check_)
        return check_
    return render_template("send.html", addr=addr, num=str(len(num)))

@app.route("/delete/<id>")
def delete_(id):
    check = delete.send_delete(id, addr)
    return redirect("/")

def run():
    app.run(port=5334)


if __name__ == "__main__":
    app.run(debug=True, port=5044)
