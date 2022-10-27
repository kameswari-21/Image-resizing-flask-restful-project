import json
from models.register_model import RegisterModel
from sqlalchemydb import db


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.BLOB, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(RegisterModel.id))

    
    def json(self):
        return {'image_name':self.name}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @staticmethod
    def find_images(id):
        return Img.query.filter_by(user_id=id).all()

    

