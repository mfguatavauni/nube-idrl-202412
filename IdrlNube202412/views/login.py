from datetime import timedelta
from flask import jsonify, make_response, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from models.models import User, db


class VistaLogin(Resource):

    def post(self):
        data = request.get_json()

        try:
            _user = User.query.filter_by(email=data["email"], password=data["password"]).first()
        
            if _user is None:
                return make_response(jsonify({"message": "Invalid credentials"}), 401)
            else:
                access_token = create_access_token(identity=_user.id, expires_delta=timedelta(hours=1))
                return make_response(jsonify({"access_token": access_token, "user.id": _user.id}), 200)
        except Exception as e:
            return make_response(jsonify({"message": "Invalid credentials"}), 401)