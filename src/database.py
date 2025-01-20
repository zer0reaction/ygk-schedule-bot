from sqlite3 import connect

# Fetches one row from database
def f_one(query: str):
    try:
        con = connect("db/base.db")
        data = con.execute(query).fetchone()
        con.close()
        return data
    except Exception as e:
        print("Error in database:f_one:")
        print("    {}".format(e))
        print("    Query: {}".format(query))
        return False

# Fetches all row from database
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

# Executes query and commits to database
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

# Returns all the groups from database
# (group_id, group_name, file_name)
def get_groups():
    return f_all("select * from groups")

# Returns True if user is present in database, false if not
def check_user_existence(telegram_id: int):
    exists = f_one("select exists(select 1 from users where telegram_id = {})".format(telegram_id))

    if exists == None:
        print("Error in database:check_user_existence:")
        print("    Failed to get exists")
        print("    telegram_id: {}".format(telegram_id))
        return False

    return exists[0] == 1

# Adds user to database
def add_user(telegram_id: int, group_id: int):
    return commit("insert into users values ({}, {})".format(telegram_id, group_id))

# Deletes specified user from database
def delete_user(telegram_id: int):
    return commit("delete from users where telegram_id = {}".format(telegram_id))

# Gets user's group database row by telegram id
def get_user_group(telegram_id: int):
    user_row = f_one("select * from users where telegram_id = {}".format(telegram_id))

    # Returning False if we can't find the user
    if user_row == None:
        print("Error in database:get_user_group:")
        print("    Failed to get user's row")
        print("    telegram_id: {}".format(telegram_id))
        return False

    user_group_id = user_row[1]
    return f_one("select * from groups where group_id = {}".format(user_group_id))
