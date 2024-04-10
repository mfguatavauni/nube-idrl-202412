from flask import jsonify, make_response, request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource

from models.models import User, db


class ViewLoginUp(Resource):
    
    def post(self):
        nuevo_usuario = User(**request.json)
        
        try:
            #Consultar si no existe 
            _user = User.query.filter_by(email=nuevo_usuario.email).first()
            _userName = User.query.filter_by(user=nuevo_usuario.user).first()

            if _user is not None:
                return make_response(jsonify({"message": "Mail ya registrado"}), 400)
            else:
                if _userName is not None:
                    return make_response(jsonify({"message": "Usuario ya registrado"}), 400)    
                else:
                    #Crearlo
                    db.session.add(nuevo_usuario)
                    db.session.commit()
                    return make_response(jsonify({"message": "Usuario creado"}), 201)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 400)

        
        
        

