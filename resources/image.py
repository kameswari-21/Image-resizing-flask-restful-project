import base64
from fileinput import filename
import io
import json
from tkinter import N
from flask_restful import Resource, reqparse
from flask import request
from PIL import Image
from flask_jwt_extended import jwt_required, get_jwt


from models.image_model import Img
from sqlalchemydb import db

class UploadImage(Resource):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.split('.', 1)[1].lower() in UploadImage.ALLOWED_EXTENSIONS

    
    def post(self):
        pic = request.files['file']
        data = json.loads(request.form['data'])
        
        # check if the post request has the file part
        if not pic:
            return {'message': 'image not uploaded'}, 400
        
        if pic and UploadImage.allowed_file(pic.filename):
            img = Image.open(pic)
            img = img.resize((data['weidth'],data['height']))

        
        file = Img(img=img.tobytes(), name=pic.filename, mimetype=pic.mimetype, user_id=data['userid'])

        db.session.add(file)
        db.session.commit()

        rawBytes = io.BytesIO()
        img.save(rawBytes, "JPEG")
        rawBytes.seek(0)
        img_base64 = base64.b64encode(rawBytes.read())

        response = {
                    "image": img_base64.decode(),
                    "message":"Image is BASE 64 encoded"   
                    }
        return response,200      


class GetImage(Resource):
    @jwt_required()
    def get(self, name):
        jwt = get_jwt()
        if Img.find_by_name(name) and jwt.get("is_admin"):
            return {'Image found': name,
                    'msg':jwt.get("is_admin")}
            
        return {'message': 'image not found'}
        

class GetImagesbyId(Resource):
    @jwt_required()
    def get(self, id):
        if Img.find_by_id(id):
            images_list = []
            # breakpoint()
            for image in Img.find_images(id):
                images_list.append(image.json())
            return {'items': images_list}
    
        