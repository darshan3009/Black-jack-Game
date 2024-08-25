import sqlite3 as sq


# getting connection to data.db
def get_connection() -> sq.Connection:
	return(sq.connect('data.db'))

# getting cursor for the data.db
def get_cursor(database= 'data.db') -> sq.Cursor:
	"""Get cursor of a database (data.db by default)"""
	con = sq.connect(database)
	cursor = con.cursor()
	return(cursor)

# getting username and password for the all current users
def get_user_login() -> list:
	"""Gives all username and password
	list[username,password]"""
	cursor = get_cursor()
	data = cursor.execute('select username,password from userdata').fetchall()
	return(data)

def insert_new_user(username: str, password: str) -> bool:
	con = get_connection()
	cursor = con.cursor()
	cursor.execute("insert into userdata VALUES('{}','{}',500,0,0,0)".format(username,password))
	con.commit()

def get_user_info(username: str) -> tuple:
	cur = get_cursor()
	data = cur.execute('select * from userdata where username = "{}"'.format(username)).fetchall()[0]
	return(data)

def game_won(username: str):
	con = get_connection()
	cur = con.cursor()
	cur.execute("update userdata set balance = balance+500 where username = '{}'".format(username))
	cur.execute("update userdata set won = won+1 where username = '{}'".format(username))
	cur.execute("update userdata set played = played+1 where username = '{}'".format(username))
	con.commit()

def game_loss(username: str):
	con = get_connection()
	cur = con.cursor()
	cur.execute("update userdata set balance = balance-100 where username = '{}'".format(username))
	cur.execute("update userdata set loss = loss+1 where username = '{}'".format(username))
	cur.execute("update userdata set played = played+1 where username = '{}'".format(username))
	con.commit()

def game_tie(username: str):
	con = get_connection()
	cur = con.cursor()
	cur.execute("update userdata set played = played+1 where username = '{}'".format(username))
	con.commit()