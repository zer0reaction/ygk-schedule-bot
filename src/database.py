from sqlite3 import connect
from constants import *

# Fetches one row from database
def f_one(query: str) -> tuple:
    try:
        con = connect("db/base.db")
        data = con.execute(query).fetchone()
        con.close()
        return (OK, data)
    except Exception as e:
        print("Error in database:f_one")
        print("    {}".format(e))
        print("    Query: {}".format(query))
        con.close()
        return (ERROR_DATABASE, )

# Fetches all rows from database
def f_all(query: str) -> tuple:
    try:
        con = connect("db/base.db")
        data = con.execute(query).fetchall()
        con.close()
        return (OK, data)
    except Exception as e:
        print("Error in database:f_all")
        print("    {}".format(e))
        print("    Query: {}".format(query))
        con.close()
        return (ERROR_DATABASE, )

# Executes query and commits to database
def commit(query: str) -> int:
    try:
        con = connect("db/base.db")
        con.execute(query)
        con.commit()
        con.close()
        return OK
    except Exception as e:
        print("Error in database:commit")
        print("    {}".format(e))
        print("    Query: {}".format(query))
        con.close()
        return ERROR_DATABASE

# Returns True if user is present in database, false if not
def check_user_existence(telegram_id: int) -> tuple:
    exists = f_one("select exists(select 1 from users where telegram_id = {})".format(telegram_id))

    if exists[0] == ERROR_DATABASE or not type(exists[1]) == tuple:
        print("Error in database:check_user_existence")
        print("    Failed to get exists")
        print("    telegram_id: {}".format(telegram_id))
        return (ERROR_DATABASE, )

    return (OK, exists[1][0] == 1)

# Adds user to database
def add_user(telegram_id: int, group_id: int) -> int:
    return commit("insert into users values ({}, {})".format(telegram_id, group_id))

# Deletes specified user from database
def delete_user(telegram_id: int) -> int:
    return commit("delete from users where telegram_id = {}".format(telegram_id))

# Gets the group_id by telegram_id
def get_user_group_id(telegram_id: int) -> tuple:
    data = f_one("select * from users where telegram_id = {}".format(telegram_id))

    # Error if we can't find the user
    if  data[0] == ERROR_DATABASE or data[1] == None:
        print("Error in database:get_user_group_id")
        print("    Failed to get user's row")
        print("    group_id: {}".format(telegram_id))
        return (ERROR_DATABASE, )

    return (OK, data[1][1])

# Gets the group row by group id
def get_group_row(group_id: int) -> tuple:
    data = f_one("select * from groups where group_id = {}".format(group_id))

    # Error if we can't find the group
    if  data[0] == ERROR_DATABASE or data[1] == None:
        print("Error in database:get_group_row:")
        print("    Failed to get group's row")
        print("    group_id: {}".format(group_id))
        return (ERROR_DATABASE, )

    return (OK, data[1])
