import json

class Muscle:
	def __init__(self,id_muscle,nom):
		self.id_muscle = id_muscle
		self.nom = nom

	@classmethod
	def get_muscle(cls, id_muscle):
		with open('json/coachV_muscles.json') as data_file:
			data = json.load(data_file)
		for muscle in data:
			if int(muscle['id_muscle']) == id_muscle:
				return Muscle(muscle['id_muscle'], muscle['nom'])
		return Muscle("","")

	@classmethod
	def get_muscles(cls):
		muscles = []
		with open('json/coachV_muscles.json') as data_file:
			data = json.load(data_file)
		for muscle in data:
			muscles.append({'id_muscle': muscle['id_muscle'], 'nom': muscle['nom']})
		return muscles

