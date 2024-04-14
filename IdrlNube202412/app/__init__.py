from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask_migrate import Migrate

from models import db
from views.login import VistaLogin
from views.signup import ViewLoginUp
from views.task import ViewTask
from views.download import ViewDownload

from app.celery_config import celery

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@db:5432/idrl'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    app.config['UPLOAD_FOLDER'] = '/app/uploads'

    app.config["JWT_SECRET_KEY"] = 'Seb7912Als89***.88.9Super'
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)

    api = Api(app)
    api.add_resource(ViewLoginUp, "/auth/signup") 
    api.add_resource(VistaLogin, "/auth/login")
    api.add_resource(ViewDownload, "/api/download/<string:filename>")
    api.add_resource(ViewTask, "/api/task/<int:id_task>", "/api/task")

    # ma.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)

    celery.conf.update(app.config)

    with app.app_context():
        db.create_all()

    return app
   