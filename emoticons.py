
def apply_emoticons(message):
    message = message.replace(":radioactive:",u"\u2622")
    message = message.replace(":pirate:",u"\uE023")
    message = message.replace(":smile:",u"\u263A")
    message = message.replace(":frown:",u"\u2639")
    message = message.replace(":flag:",u"\u2691")
    message = message.replace(":disapproval:",u"\u0CA0_\u0CA0")
    message = message.replace(":wink:",u"\u25D5\u203F\u21BC")
    return message
