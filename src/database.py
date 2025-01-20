from sqlite3 import connect

def f_one(query: str):
    try:
        con = connect("db/base.db")
        data = con.execute(query).cur.fetchone()
        con.close()
        return data
    except Exception as e:
        print("Error in database:f_one:")
        print("    {}".format(e))
        print("    Query: {}".format(query))
        return False

def f_all(query: str):
    try:
        con = connect("db/base.db")
        data = con.execute(query).fetchall()
        con.close()
        return data
    except Exception as e:
        print("Error in database:f_all:")
        print("    {}".format(e))
        print("    Query: {}".format(query))
        return False

def commit(query: str):
    try:
        con = connect("db/base.db")
        con.execute(query)
        con.commit()
        con.close()
        return True
    except Exception as e:
        print("Error in database:commit:")
        print("    {}".format(e))
        print("    Query: {}".format(query))
        return False

def get_groups():
    return f_all("select * from groups")

def check_user_existence(id: int):
    return f_one("select exists(select 1 from users where telegram_id = {})".format(id))[0] == 1

def add_user(id: int, group_id: int):
    return commit("insert into users values ({}, {})".format(id, group_id))

def delete_user(id: int):
    return commit("delete from users where telegram_id = {}".format(id))

def get_user_group_id(id: int):
    return f_one("select * from users where telegram_id = {}".format(id))[1]

def get_user_group_name(id: int):
    group_id = get_user_group_id(id)
    return f_one("select * from groups where group_id = {}".format(group_id))[1]
