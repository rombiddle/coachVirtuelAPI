import mysql.connector
from flask_restful import Resource, reqparse
from db import DB
from werkzeug.security import generate_password_hash, check_password_hash

class User:
	def __init__(self, _id, identifiant, email, password):
		self.id = _id
		self.identifiant = identifiant
		self.email = email
		self.password = password
	
	@classmethod
	def find_by_username(cls, username):
		
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()

		query = "SELECT id_user, identifiant, email, password FROM coachV_users WHERE identifiant=%s"
		cursor.execute(query, (username,))

		identifiantV = ""
		emailV = ""
		passwordV = ""
		id_userV = ""
		for (id_user, identifiant, email, password) in cursor:
			identifiantV = "{}".format(identifiant)
			emailV = "{}".format(email)
			passwordV = "{}".format(password)
			id_userV = "{}".format(id_user)
		if identifiantV:
			user = User(id_user, identifiantV, emailV, passwordV)
		else:
			user = None
		
		cursor.close()
		cnx.close()
		return user

	@classmethod
	def find_by_id(cls, _id):
		
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()

		query = "SELECT * FROM coachV_users WHERE id_user=%s"
		cursor.execute(query, (_id,))
		identifiantV = ""
		emailV = ""
		passwordV = ""
		id_userV = ""
		for (id_user, identifiant, email, password) in cursor:
			identifiantV = "{}".format(identifiant)
			emailV = "{}".format(email)
			passwordV = "{}".format(password)
			id_userV = "{}".format(id_user)
		if identifiantV:
			user = User(id_user, identifiantV, emailV, passwordV)
		else:
			user = None

		cursor.close() 
		cnx.close()
		return user

	@classmethod
	def updateWithPassword(cls, item):
		
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()

		print(item)

		query = "UPDATE coachV_users SET email=%s, password=%s WHERE identifiant=%s"
		cursor.execute(query, (item['email'], item['password'],item['identifiant']))

		cnx.commit()
		cursor.close()
		cnx.close()

	@classmethod
	def updateWithoutPassword(cls, item):
		
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()

		print(item)

		query = "UPDATE coachV_users SET email=%s WHERE identifiant=%s"
		cursor.execute(query, (item['email'],item['identifiant']))

		cnx.commit()
		cursor.close()
		cnx.close()

	@classmethod
	def set_password(cls, password):
		return generate_password_hash(password)
	
	@classmethod
	def check_password(cls, pw_hash, password):
		return check_password_hash(pw_hash, password)

