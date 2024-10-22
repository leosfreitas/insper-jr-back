from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import pymongo
import certifi 
from config import CONFIG

app = Flask(__name__)
CORS(app)

app.config.from_object(CONFIG)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

client = pymongo.MongoClient(CONFIG.MONGO_URI, tlsCAFile=certifi.where())


from routes.auth import auth_bp
from routes.users import users_bp
from routes.avisos import avisos_bp
from routes.alunos import alunos_bp

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(avisos_bp)
app.register_blueprint(alunos_bp)


if __name__ == '__main__':
    app.run(debug=True)
