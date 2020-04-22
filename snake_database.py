import mysql.connector

try:
	cnx = mysql.connector.connect(user='Your username', password='Your password',
								  host='select host', database='which database')

	if cnx.is_connected():
		print("Connected to MySQL database")
except Error as e:
	print(e)

cursor = cnx.cursor()


def insert_new_score(name, score):
	query = ("INSERT INTO highscores VALUES ('%s', %d);" % (name, score))
	cursor.execute(query)
	cnx.commit()

def get_high_score():
	query = ("SELECT * FROM highscores ORDER BY Score DESC LIMIT 1;")
	cursor.execute(query)

	for row in cursor:
		return row[1]
