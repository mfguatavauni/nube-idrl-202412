import json
from flask import jsonify, make_response, request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource
import jwt
from werkzeug.utils import secure_filename
from google.cloud import storage
import os

from models.models import Task, TaskSchema, db

# from .process_video import process_video_task
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/soluciones-cloud-2024120/topics/idrl-pending-to-process'

task_schema = TaskSchema()

client = storage.Client()
bucket_name = 'idrl-bucket'
bucket = client.bucket(bucket_name)

class ViewTask(Resource):
    @jwt_required()
    def post(self):
        task = Task()
        
        try:
            if 'fileName' not in request.files:
                return make_response(jsonify({'error': 'No file part'}), 400)
            file = request.files['fileName']
            if file.filename == '':
                return make_response(jsonify({'error': 'No selected file'}), 400)
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov'}:
                filename = secure_filename(file.filename)
                blob = bucket.blob(filename)
                blob.upload_from_file(file, content_type=file.content_type)
                # save_path = os.path.join('/home/angelricardoracinimeza/remote_folder', filename)
                # file.save(save_path)

                task.status = 'UPLOADED'
                task.user_id = get_jwt_identity()
                task.path = filename

                db.session.add(task)
                db.session.commit()

                # process_video_task.delay(filename, task.id)

                data = json.dumps({
                    'filename': filename,
                    'task_id': task.id
                })
                publisher.publish(topic_name, data.encode('utf-8'))

                return make_response(jsonify({
                    'message': 'File uploaded successfully, processing will start shortly.',
                    'filename': filename,
                    'task_id': task.id
                }), 200)
            else:
                return make_response(jsonify({'error': 'Invalid file type'}), 400)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 400)

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
        
       
    
    