from flask import Flask, jsonify    #, request
from flask_restful import Api
from security import *
from flask_jwt import JWT
from resource.users import UserRegister
from resource.items import *
from resource.stores import *
from datetime import *
from db import db
app = Flask(__name__)

app.secret_key = 'I shall be successful'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_AUTH_URL_RULE'] = '/login'

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

api = Api(app)
# @app.before_first_request
# def create_table():
#     db.create_all()

jwt = JWT(app, authenticate, identity)  # automatically creates /auth : return Json Web Tools Token

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({'access_token': access_token.decode('utf-8'), 'user_id': identity.id})

# @jwt.error_handler
# def customized_error_handler(error):
#     return jsonify({'message': error.description, 'code': error.status_code }), error.status_code

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
