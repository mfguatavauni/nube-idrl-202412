import json
from flask import jsonify, make_response, request, current_app
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
import jwt

from models.models import Task, TaskSchema, db

task_schema = TaskSchema()

class ViewTask(Resource):
    
    @jwt_required()
    def post(self):
        #task = Task(**request.json)
        #Se reciben losparametros de la tarea
        task = Task()
        task.user_id = request.json['user_id']
        task.status = request.json['status']
        #Se recibe el archivo en base64
        _FileBase64 = request.json['fileBase64']
        
        
        try:
            ##Almacenar la tarea
            db.session.add(task)
            db.session.commit()
            ##Almacenar el archivo para ser procesado

            ##Retornar el id de la tarea
            return make_response(jsonify({"message": "Tarea creada Id: " + str(task.id) }), 201)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 400)


    @jwt_required()
    def get(self):
        #Se retornan todas las tareas del usuario
        auth_header = request.headers.get('Authorization')
        if auth_header: 
            try:
                token = auth_header.split(" ")[1]
                payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                user_id = str(payload['sub'])
                taskR = db.session.query(Task).filter(Task.user_id == user_id).all()
                return task_schema.dump(taskR, many=True)
            except Exception as e:
                return make_response(jsonify({"message": "Invalid token"}), 401)
        else:
            return make_response(jsonify({"message": "Unauthorized"}), 401)
            

    @jwt_required()
    def get(self, id_task):
        taskR = db.session.query(Task).filter(Task.id == id_task).all()
        return task_schema.dump(taskR, many=True)

        
    @jwt_required()
    def delete(self, id_task):
        taskR = db.session.query(Task).filter(Task.id == id_task).delete()
        db.session.commit()
        return make_response(jsonify({"message": "Tarea eliminada"}), 200)
        
       
    
    