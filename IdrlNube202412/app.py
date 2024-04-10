from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import db
from views.login import VistaLogin
from views.signup import ViewLoginUp
from views.task import ViewTask


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@172.17.0.2:5432/idrl"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "Seb7912Als89***.88.9Super"
    app.config["PROPAGATE_EXCEPTIONS"] = True

    app_context = app.app_context()
    app_context.push()
    add_urls(app)
    CORS(app)
    
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return ""
    
    return app

def add_urls(app):
    api = Api(app)
    api.add_resource(ViewLoginUp, "/auth/signup") 
    api.add_resource(VistaLogin, "/auth/login")
    api.add_resource(ViewTask, "/api/task/<int:id_task>", "/api/task")
    
    

app = create_app()
db.init_app(app)
db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)