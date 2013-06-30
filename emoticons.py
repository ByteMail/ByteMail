
def apply_emoticons(message):
    message = message.replace(":radioactive:",u"\u2622")
    message = message.replace(":pirate:",u"\uE023")
    message = message.replace(":smile:",u"\u263A")
    message = message.replace(":flag:",u"\u2691")
    return message
