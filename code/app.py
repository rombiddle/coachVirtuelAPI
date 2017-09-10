from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import mysql.connector
from security import authenticate, identity
from resources.user import UserRegister, UserList, UserUtil, UserTest
from resources.question import QuestionList
from resources.program import ProgramUtil
from resources.exercice import ExerciceList, ExerciceUtil


app = Flask(__name__)

app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(UserUtil, '/user/<identifiant>')
api.add_resource(UserTest, '/test')
api.add_resource(QuestionList, '/questions')
api.add_resource(ExerciceList, '/exercices')
api.add_resource(ExerciceUtil, '/exercice/<identifiant>')
api.add_resource(ProgramUtil, '/program')

if __name__ == '__main__':
	app.run(port=5000, debug=True)
