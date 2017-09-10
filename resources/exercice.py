import mysql.connector
from flask_restful import Resource, reqparse
from db import DB
from flask_jwt import jwt_required
from models.exercice import Muscle


class ExerciceList(Resource):

	@jwt_required()
	def get(self):
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()

		query = "SELECT * FROM coachV_exercices"
		cursor.execute(query)

		exercices = []

		for (id_exercice, nom, muscle1,muscle2,muscle3,muscle4,muscle5,muscle6,muscle7,muscle8,muscle9,muscle10,niveau,description,materiel,_type,sport,id_user_created) in cursor:
			exercices.append({
				'id_exercice': id_exercice,
				'nom': nom,
				'muscle1': Muscle.get_muscle(muscle1).nom,
				'muscle2': Muscle.get_muscle(muscle2).nom,
				'muscle3': Muscle.get_muscle(muscle3).nom,
				'muscle4': Muscle.get_muscle(muscle4).nom,
				'muscle5': Muscle.get_muscle(muscle5).nom,
				'muscle6': Muscle.get_muscle(muscle6).nom,
				'muscle7': Muscle.get_muscle(muscle7).nom,
				'muscle8': Muscle.get_muscle(muscle8).nom,
				'muscle9': Muscle.get_muscle(muscle9).nom,
				'muscle10': Muscle.get_muscle(muscle10).nom,
				'niveau': niveau,
				'description': description,
				'materiel': materiel,
				'type': _type,
				'sport': sport})

		cursor.close()
		cnx.close()
		return exercices

class ExerciceUtil(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('nom',
		type=str,
		required=True,
		help="The nom field cannot be left blank!"
	)
	parser.add_argument('muscle1',
		type=int,
		required=True,
		help="The muscle1 field cannot be left blank!"
	)
	parser.add_argument('muscle2',
		type=int,
		required=True,
		help="The muscle2 field cannot be left blank!"
	)
	parser.add_argument('muscle3',
		type=int,
		required=True,
		help="The muscle3 field cannot be left blank!"
	)
	parser.add_argument('muscle4',
		type=int,
		required=True,
		help="The muscle4 field cannot be left blank!"
	)
	parser.add_argument('muscle5',
		type=int,
		required=True,
		help="The muscle5 field cannot be left blank!"
	)
	parser.add_argument('muscle6',
		type=int,
		required=True,
		help="The muscle6 field cannot be left blank!"
	)
	parser.add_argument('muscle7',
		type=int,
		required=True,
		help="The muscle7 field cannot be left blank!"
	)
	parser.add_argument('muscle8',
		type=int,
		required=True,
		help="The muscle8 field cannot be left blank!"
	)
	parser.add_argument('muscle9',
		type=int,
		required=True,
		help="The muscle9 field cannot be left blank!"
	)
	parser.add_argument('muscle10',
		type=int,
		required=True,
		help="The muscle10 field cannot be left blank!"
	)
	parser.add_argument('niveau',
		type=str,
		required=True,
		help="The niveau field cannot be left blank!"
	)
	parser.add_argument('description',
		type=str,
		required=True,
		help="The description field cannot be left blank!"
	)
	parser.add_argument('materiel',
		type=int,
		required=True,
		help="The materiel field cannot be left blank!"
	)
	parser.add_argument('type',
		type=int,
		required=True,
		help="The type field cannot be left blank!"
	)
	parser.add_argument('sport',
		type=int,
		required=True,
		help="The sport field cannot be left blank!"
	)
	

	@jwt_required()
	def post(self, identifiant):

		data = ExerciceUtil.parser.parse_args()
		
		
		cnx = mysql.connector.connect(user=DB.db_user(), password=DB.db_password(),
                              host=DB.db_host(),
                              database=DB.db_database())
		cursor = cnx.cursor()

		try:
			query = "INSERT INTO coachV_exercices(nom, muscle1,muscle2,muscle3,muscle4,muscle5,muscle6,muscle7,muscle8,muscle9,muscle10,niveau,description,materiel,type,sport,id_user_created) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(query, (
				data['nom'],
				data['muscle1'],
				data['muscle2'],
				data['muscle3'],
				data['muscle4'],
				data['muscle5'],
				data['muscle6'],
				data['muscle7'],
				data['muscle8'],
				data['muscle9'],
				data['muscle10'],
				data['niveau'],
				data['description'],
				data['materiel'],
				data['type'],
				data['sport'],
				identifiant))

			cnx.commit()
		except mysql.connector.Error as err:
			return {'message':'An error occured creating the exercice. {}'.format(err)}, 500
		cursor.close()
		cnx.close()

		return {"message": "Exercice created successfully."}, 201
		
	def get(self, identifiant):	
		return Muscle.get_muscles()
