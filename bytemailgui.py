from flask import Flask, redirect, render_template, request
import db
import message
import random
import read
import delete
import addressbook
import sent as sent_

app = Flask(__name__)

def check():
    while True:
        try:
            c = db.messages.find("messages", "all")
            break
        except:
            continue
    messages = []
    for x in c:
        if 'to' in x:
            if x['to'] == addr:
                messages.append(x)
    return messages


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        for x in request.form.getlist("delete"):
            delete_(x.replace("/", ''))
    message = check()
    message.reverse()
    return render_template("index.html", messages=message, num=str(len(message)), addr=addr)

def empty_sent(id):
    sent_.sent_delete(id)

@app.route("/sent/", methods=['GET', 'POST'])
def sent():
    try:
        if request.method == 'POST':
            for x in request.form.getlist("delete"):
                empty_sent(x.replace("/", ''))
        c = db.sent.find("sent", "all")
        message = []
        for x in c:
            message.append(x)
        message.reverse()
        return render_template("sent.html", messages=message, num=str(len(check())), addr=addr)
    except:
        return "<script>alert('You have not sent any messages yet.');window.location = '/';</script>" 
@app.route("/read/<id>")
def read_(id):
    data = read.read(id, addr).split("\n")
    id = data[2]
    time = data[3]
    title = data[4]
    from_ = data[5]
    message = ' '.join(data[7:])
    num = check()
    to_ = title.split()[1]
    title_ = from_.split()[1]
    return render_template("read.html", title_=title_, to_=to_, num=str(len(num)), id=id, time=time, from_=from_, message=message, title=title, addr=addr)

@app.route("/addressbook/", methods=['GET', 'POST'])
def addressbook_():
    if request.method == "POST":
        name = request.form['name']
        address = request.form['addr']
        addressbook.add_entry(name, address)
        delete = request.form.getlist("delete")
        if delete:
            for x in delete:
                address_delete(x)
        return redirect("/addressbook/")
    try:
        addr_ = []
        addresses = addressbook.addresses().replace("\t", '').split("\n")
        for x in addresses:
            try:
                if x != '':
                    x = x.split()
                    name = x[0]
                    addre = x[1]
                    addr_.append({"name":name, "addr":addre})
            except IndexError:
                continue
        addresses = addr_
        return render_template("addressbook.html", addresses=addresses, num=str(len(check())), addr=addr)
    except Exception, error:
        return render_template("addressbook.html", num=str(len(check())), addr=addr)
@app.route("/reply/<to>/<title>/", methods=['GET', 'POST'])
def reply(to, title):
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
    
    return render_template("reply.html", title=title, to=to, addr=addr, num=str(len(num)))

def address_delete(name):
    addressbook.remove_address(name)

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
    
def delete_(id):
    check = delete.send_delete(id, addr)

def run():
    global addr
    addr = db.data.find("data", "all")[0]['addr']
    app.run(port=5334, debug=True)


if __name__ == "__main__":
    app.run(debug=True, port=5044)
