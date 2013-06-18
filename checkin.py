import db

def checkin(obj, ip, data):
    check = False
    try:
        c = db.nodes.find("nodes", {"addr":data['addr']}) 
        if c:
            c = c[0]
            if c['port'] == data['port']:
                if c['ip'] == ip:
                    check = True
            elif data['addr'] == c['addr']:
                check = True
    except ValueError:
        pass
    else:
        if not check and len(data['addr']) == 32:
            if data['publickey'].startswith("PublicKey(") and data['publickey'].endswith(")"):
                db.nodes.insert("nodes", {"addr":data['addr'], 'ip':ip, 'port':data['port'], "publickey":data['publickey']})
            
