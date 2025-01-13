from sqlite3 import connect

def get_groups():
    con = connect("db/base.db")
    cur = con.cursor()

    cur.execute("select * from groups")
    all = cur.fetchall()

    con.close()
    return all

def add_user(id: int, group: str):
    con = connect("db/base.db")
    cur = con.cursor()

    cur.execute("insert into users values ({}, {})".format(id, group))

    con.commit()
    con.close()
