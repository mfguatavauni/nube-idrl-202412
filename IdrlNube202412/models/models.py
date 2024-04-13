import enum
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


db = SQLAlchemy()

class StatusType(enum.Enum):
    PROCESSED = "PROCESSED"
    UPLOADED = "UPLOADED"
    FAIL = "FAIL"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=True)
    
class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(StatusType), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    processing_at = db.Column(db.DateTime, nullable=True)   
    path=db.Column(db.String(120), nullable=False)
    __table_args__ = (UniqueConstraint('id', 'user_id', name='_user_id_user_uc'),)

class TaskSchema(SQLAlchemyAutoSchema):
    id = fields.Integer()
    user_id = fields.Integer()
    status = fields.Enum(StatusType, by_value=True)
    created_at = fields.DateTime()
    processing_at = fields.DateTime()
    path = fields.String()
    
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
        




