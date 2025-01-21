from database import *
from constants import *
from creds import my_id

########## DATABASE TEST ##########

# --- f_one ---
print("testing f_one with correct input 1...")
data = f_one("select * from users")
if (data[0] == OK and type(data[1]) == tuple): print("PASSED!\n")
else: print("FAILED!\n")

print("testing f_one with correct input 2...")
data = f_one("select * from users where telegram_id = 0")
if (data[0] == OK and data[1] == None): print("PASSED!\n")
else: print("FAILED!\n")

print("testing f_one with wrong input...")
data = f_one("select * from users where teegram_id = 0")
if (data[0] == ERROR_DATABASE): print("PASSED!\n")
else: print("FAILED!\n")
# -------------

# --- f_all ---
print("testing f_all with correct input 1...")
data = f_all("select * from users")
if (data[0] == OK and type(data[1]) == list and len(data[1]) > 0): print("PASSED!\n")
else: print("FAILED!\n")

print("testing f_all with correct input 2...")
data = f_all("select * from users where telegram_id = 0")
if (data[0] == OK and type(data[1]) == list and len(data[1]) == 0): print("PASSED!\n")
else: print("FAILED!\n")

print("testing f_all with wrong input...")
data = f_all("select * from users where teegram_id = 0")
if (data[0] == ERROR_DATABASE): print("PASSED!\n")
else: print("FAILED!\n")
# -------------

# --- commit ---
print("testing commit with correct input...")
data = commit("insert into users values(1, 2)")
if (data == OK): print("PASSED!\n")
else: print("FAILED!\n")

print("testing commit with wrong input...")
data = commit("insert into users values(1, 2)")
if (data == ERROR_DATABASE): print("PASSED!\n")
else: print("FAILED!\n")
commit("delete from users where telegram_id = 1")
# --------------

# --- check_user_existence ---
print("testing check_user_existence with correct input 1...")
data = check_user_existence(my_id)
if (data[0] == OK and data[1] == True): print("PASSED!\n")
else: print("FAILED!\n")

print("testing check_user_existence with correct input 2...")
data = check_user_existence(0)
if (data[0] == OK and data[1] == False): print("PASSED!\n")
else: print("FAILED!\n")

print("testing check_user_existence with wrong input...")
data = check_user_existence("wrong")
if (data[0] == ERROR_DATABASE): print("PASSED!\n")
else: print("FAILED!\n")
# ----------------------------

# --- add_user ---
print("testing add_user with correct input...")
data = add_user(1, 1)
if (data == OK): print("PASSED!\n")
else: print("FAILED!\n")
commit("delete from users where telegram_id = 1")

print("testing add_user with wrong input...")
data = add_user("wrong", 1)
if (data == ERROR_DATABASE): print("PASSED!\n")
else: print("FAILED!\n")
# ----------------

# --- delete_user ---
add_user(1, 1)
print("testing delete_user with correct input 1...")
data = delete_user(1)
if (data == OK): print("PASSED!\n")
else: print("FAILED!\n")

print("testing delete_user with correct input 2...")
data = delete_user(1)
if (data == OK): print("PASSED!\n")
else: print("FAILED!\n")

print("testing delete_user with wrong input...")
data = delete_user("wrong")
if (data == ERROR_DATABASE): print("PASSED!\n")
else: print("FAILED!\n")
# -------------------

# --- get_user_group_id ---
print("testing get_user_group with correct input...")
data = get_user_group_id(my_id)
if (data[0] == OK and type(data[1]) == int): print("PASSED!\n")
else: print("FAILED!\n")

print("testing get_user_group with wrong input...")
data = get_user_group_id(1)
if (data[0] == ERROR_DATABASE): print("PASSED!\n")
else: print("FAILED!\n")
# ---------------------

# --- get_group_row ---
print("testing get_group_row with correct input...")
data = get_group_row(1)
if (data[0] == OK and type(data[1]) == tuple): print("PASSED!\n")
else: print("FAILED!\n")

print("testing get_group_row with wrong input 1...")
data = get_group_row(0)
if (data[0] == ERROR_DATABASE): print("PASSED!\n")
else: print("FAILED!\n")

print("testing get_group_row with wrong input 1...")
data = get_group_row("wrong")
if (data[0] == ERROR_DATABASE): print("PASSED!\n")
else: print("FAILED!\n")
# ---------------------
