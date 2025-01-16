from sqlite3 import connect

def f_one(query: str):
    con = connect("db/base.db")
    cur = con.cursor()
    cur.execute(query)
    data = cur.fetchone()
    con.close()
    return data

def f_all(query: str):
    con = connect("db/base.db")
    cur = con.cursor()
    cur.execute(query)
    data = cur.fetchall()
    con.close()
    return data

def commit(query: str):
    con = connect("db/base.db")
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()

def get_groups():
    return f_all("select * from groups")

def check_user_existence(id: int):
    return f_one("select exists(select 1 from users where telegram_id = {})".format(id))[0] == 1

def add_user(id: int, group_id: int):
    commit("insert into users values ({}, {})".format(id, group_id))

def delete_user(id: int):
    commit("delete from users where telegram_id = {}".format(id))

def get_user_group_id(id: int):
    return f_one("select * from users where telegram_id = {}".format(id))[1]

def get_user_group_name(id: int):
    group_id = get_user_group_id(id)
    return f_one("select * from groups where group_id = {}".format(group_id))[1]
