from flask_jwt_extended import jwt_required
import os
from flask_restful import Resource
from flask import current_app, send_from_directory
  
class ViewDownload(Resource):
    def get(self, filename):
        print(filename)
        directory = os.path.join(current_app.config['UPLOAD_FOLDER'], 'processed')
        try:
            return send_from_directory(directory, filename)
        except FileNotFoundError:
            abort(404)