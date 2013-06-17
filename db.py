import landerdb

nodes = landerdb.Connect("nodes.db")
data = landerdb.Connect("data.db")
unsent = landerdb.Connect("unsent.db")
messages = landerdb.Connect("messages.db")
nonces = landerdb.Connect("nonces.db")
addressdb = landerdb.Connect("addressbook.db")
