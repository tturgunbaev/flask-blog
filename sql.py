import sqlite3

with sqlite3.connect('blog.db') as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (title TEXT, post TEXT)")
    cursor.execute('INSERT INTO posts VALUES ("Good", "I\'m good.")')
    cursor.execute('INSERT INTO posts VALUES ("Well", "I\'m well.")')
    cursor.execute('INSERT INTO posts VALUES ("Excelent", "I\'m excelent.")')
    cursor.execute('INSERT INTO posts VALUES ("Okay", "I\'m okay.")')