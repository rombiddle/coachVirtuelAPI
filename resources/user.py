import mysql.connector
from flask_restful import Resource, reqparse
from models.user import User
from db import DB
import string
import random
from flask_jwt import jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('identifiant',
		type=str,
		required=True,
		help="The identifiant field cannot be left blank!"
	)
	parser.add_argument('email',
		type=str,
		required=True,
		help="The email field cannot be left blank!"
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help="The password field cannot be left blank!"
	)

	def post(self):
		data = UserRegister.parser.parse_args()
		
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()
		try:
			query = "INSERT INTO coachV_users(identifiant, email, password) VALUES (%s, %s, %s)"
			cursor.execute(query, (data['identifiant'],data['email'],generate_password_hash(data['password'])))

			cnx.commit()
		except:
			return {'message':'An error occured creating the user.'}, 500
		cursor.close()
		cnx.close()

		return {"message": "User created successfully."}, 201

class UserList(Resource):
	@jwt_required()
	def get(self):
		
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()

		query = "SELECT * FROM coachV_users"
		cursor.execute(query)

		items = []

		for (id_user, identifiant, email, password) in cursor:
			items.append({'identifiant': identifiant, 'email': email})

		cursor.close()
		cnx.close()

		return items

class UserUtil(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('email',
		type=str,
		required=True,
		help="The email field cannot be left blank!"
	)
	parser.add_argument('oldpassword',
		type=str,
		required=True,
		help="The password field cannot be left blank!"
	)
	parser.add_argument('newpassword',
		type=str,
		required=True,
		help="The password field cannot be left blank!"
	)

	@jwt_required()
	def get(self, identifiant):
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()

		query = "SELECT * FROM coachV_users WHERE identifiant=%s"
		cursor.execute(query,(identifiant,))

		item = ""
		for (id_user, identifiant, email, password) in cursor:
			item = {'identifiant': identifiant, 'email': email}

		cursor.close()
		cnx.close()

		return item

	@jwt_required()
	def put(self, identifiant):

		data = UserUtil.parser.parse_args()
		item = User.find_by_username(identifiant)
		updated_item = {'identifiant': identifiant, 'email': data['email']}

		if item is None:
			return {'message':'This user does not exist.'}, 500
		else:
			if data['oldpassword'] != '' and data['newpassword'] == '':
				return {'message':'The new password is empty.'}, 500
			if data['oldpassword'] == '' and data['newpassword'] != '':
				return {'message':'The old password is empty.'}, 500

			if (data['oldpassword'] != '' and data['newpassword'] != ''):
				if check_password_hash(item.password, data['oldpassword']):
					updated_item['password'] = generate_password_hash(data['newpassword'])
					try:
						User.updateWithPassword(updated_item)
					except:
						return {'message':'An error occured updating the user with new password.'}, 500
				else:
					return {'message':'An error occured updating the user. Your old password does not match.'}, 500
			else:
				try:
					User.updateWithoutPassword(updated_item)
				except:
					return {'message':'An error occured updating the user.'}, 500

		return updated_item

class UserTest(Resource):

	def get(self):
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()

		query = "INSERT INTO coachV_users(identifiant, email, password) VALUES (%s, %s, %s)"

		for x in range(0, 20000):
			test = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
			cursor.execute(query, (test,"romain","romain"))
			cnx.commit()

		cursor.close()
		cnx.close()

		return {'message':'test ok'}, 200





