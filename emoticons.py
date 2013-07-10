
def apply_emoticons(message):
    message = message.replace(":radioactive:",u"\u2622")
    message = message.replace(":pirate:",u"\uE023")
    message = message.replace(":smile:",u"\u263A")
    message = message.replace(":flag:",u"\u2691")
    message = message.replace(":devious",u"\u0CA0\u203F\u0CA0")
    message = message.replace(":love:",u"\u2665\u203F\u2665")
    return message
