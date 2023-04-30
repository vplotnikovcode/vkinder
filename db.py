import sqlite3

def set_data(client_user_id, couple_id):


    con = sqlite3.connect("vk_id2.db")
    cursor = con.cursor()
    dt=(str(client_user_id),str(couple_id))
    cursor.execute("INSERT INTO searched_id (user_id, couple_id) VALUES (?, ?)",dt)

    con.commit()


def get_data(client_user_id):
    con = sqlite3.connect("metanit.db")
    cursor = con.cursor()
    cursor.execute("SELECT user_id, couple_id FROM searched_id where user_id='"+str(client_user_id)+"'")
    lst=[]
    for i in cursor.fetchall():
        lst.append(i[1])
