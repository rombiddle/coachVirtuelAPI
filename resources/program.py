import mysql.connector
from flask_restful import Resource , reqparse
from db import DB
from flask_jwt import jwt_required

class ProgramUtil(Resource):

	@jwt_required()
	def get(self):
		return {"message": "Route program."}, 200