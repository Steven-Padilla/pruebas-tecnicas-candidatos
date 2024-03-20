from extensions import db

def truncate_first_word(text, max_length):
    words = text.split()
    first_word = words[0]
    if len(first_word) > max_length:
        return first_word[:max_length-3] + '...'
    else:
        return first_word

def get_db_name_app():
    return db.engine.url.database