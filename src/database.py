from sqlite3 import connect

def get_groups():
    con = connect("db/base.db")
    cur = con.cursor()
    cur.execute("select * from groups")
    all = cur.fetchall()
    con.close()
    return all

def check_user_existence(id: int):
    con = connect("db/base.db")
    cur = con.cursor()
    cur.execute("select exists(select 1 from users where telegram_id = {})".format(id))
    result = cur.fetchone()[0] == 1
    con.close()
    return result

def add_user(id: int, group_id: int):
    con = connect("db/base.db")
    cur = con.cursor()
    cur.execute("insert into users values ({}, {})".format(id, group_id))
    con.commit()
    con.close()

def delete_user(id: int):
    con = connect("db/base.db")
    cur = con.cursor()
    cur.execute("delete from users where telegram_id = {}".format(id))
    con.commit()
    con.close()
