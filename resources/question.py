import mysql.connector
from flask_restful import Resource
from db import DB
from flask_jwt import jwt_required
# import redis

class QuestionList(Resource):

	@jwt_required()
	def get(self):
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()

		query = "SELECT * FROM coachV_questions"
		cursor.execute(query)

		questions = []

		for (id_question, typeQouC, texte) in cursor:
			questions.append({'id_question': id_question, 'typeQouC': typeQouC, 'texte': texte})

		cursor.close()
		cnx.close()

		return questions

	# def get(self):
	# 	r = redis.Redis(host='localhost',port=6379, db=0)

	# 	r.set('foo', 'bar')
	# 	return {'message': 'ok'}

	# def post(self):
	# 	r = redis.Redis(host='localhost',port=6379, db=0)

	# 	return {'result': r.get('foo').decode("utf-8")}