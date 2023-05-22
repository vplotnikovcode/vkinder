import sqlite3


def set_data(client_user_id, offset):
    con = sqlite3.connect("vk_id2.db")
    cursor = con.cursor()
    if cursor.execute(f'select user_id from users where user_id={client_user_id};').fetchall():
        cursor.execute(f"UPDATE users SET offset = {offset} WHERE user_id = {client_user_id};")
    else:
        cursor.execute("INSERT INTO users (user_id, offset) VALUES (?, ?);", (client_user_id, offset))
    con.commit()


def get_data(client_user_id):
    con = sqlite3.connect("vk_id2.db")
    cursor = con.cursor()
    try:
        cursor.execute(f"SELECT offset FROM users where user_id={client_user_id};")
        result = cursor.fetchall()
        return result[0][0] if result else 0
    except:
        cursor.execute('create table users(user_id INTEGER, offset INTEGER);')
        con.commit()
        return 0
