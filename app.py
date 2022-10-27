import datetime
from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt


from sqlalchemydb import db
from resources.register import UserRegister, Token_refresh, UserList, Login
from resources.image import GetImagesbyId, UploadImage, GetImage, GetImagesbyId



app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['JWT_SECRET_KEY'] = 'Minister'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


#storing the blacklist tokens in set data structure
blacklist = set()


@app.before_first_request
def create_tables():
    db.create_all()

"""
`claims` are data we choose to attach to each jwt payload
and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
one possible use case for claims are access level control, which is shown below.
"""

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):  # Remember identity is what we define when creating the access token
    if identity == 1:   # instead of hard-coding, we should read from a config file or database to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': 'token has expired',
        'error': 'token_expired'
    })


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    })

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Required an access_token',
        'error': 'authorization_required'
    })

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'fresh token required',
        'error': 'fresh_token_required'})

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    # breakpoint()
    return jti in blacklist

class Logout(Resource):
    @jwt_required(verify_type=False)
    def delete(self):
        # breakpoint()
        jid = get_jwt()['jti']
        blacklist.add(jid)
        
        return {'msg':'loged out successfully'}

api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/userslist')
api.add_resource(Login, '/login')
api.add_resource(UploadImage, '/uploadimage')
api.add_resource(GetImage, '/getimage/<string:name>')
api.add_resource(GetImagesbyId, '/imagebyid/<int:id>')
api.add_resource(Token_refresh, '/refresh')
api.add_resource(Logout, '/logout')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, port=5002)

