import sqlite3


def set_data(client_user_id, offset, couples):
    con = sqlite3.connect("vk_id2.db")
    cursor = con.cursor()
    if cursor.execute(f'select user_id from users where user_id={client_user_id};').fetchall():
        cursor.execute("UPDATE users SET offset = ?, couples = ? WHERE user_id = ?;",
                       (offset, couples, client_user_id))
    else:
        cursor.execute("INSERT INTO users (user_id, offset, couples) VALUES (?, ?, ?);",
                       (client_user_id, offset, couples))
    con.commit()


def get_data(client_user_id, table):
    con = sqlite3.connect("vk_id2.db")
    cursor = con.cursor()
    try:
        cursor.execute(f"SELECT {table} FROM users where user_id={client_user_id};")
        result = cursor.fetchall()
        return result if result else None
    except:
        cursor.execute('create table users(user_id INTEGER, offset INTEGER, couples TEXT);')
        con.commit()
        return 0
