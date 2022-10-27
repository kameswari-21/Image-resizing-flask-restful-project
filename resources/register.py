import datetime
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from models.register_model import RegisterModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('email', type=str, required=True, help='This field is cannot be blank')

    def post(self):
        data = UserRegister.parser.parse_args() 

        if RegisterModel.find_by_username(data['username']):
            return {'message': 'username is already exists'}
        
        
        user = RegisterModel(data['username'], data['password'], data['email'])
        user.save_to_db()
        
        return {'message': 'User created successfull'}, 201

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be blank')

    def post(self):
        data = Login.parser.parse_args()
        
        user = RegisterModel.find_by_username(data['username'])
        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=datetime.timedelta(minutes=20))
            refresh_token = create_refresh_token(user.id, expires_delta=datetime.timedelta(hours=2))
            return {'access_token': access_token,
                    'refresh_token':refresh_token}
        
        return {'message': 'invalid credentails'}



class UserList(Resource):
    def get(self):
        users = [user.json() for user in RegisterModel.find_all()]
        return {'users': users}

class Token_refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': access_token}, 200

