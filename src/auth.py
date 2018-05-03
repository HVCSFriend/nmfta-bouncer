from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import UserModel

parser = reqparse.RequestParser()
parser.add_argument("username")
parser.add_argument("password")
parser.add_argument("grant_type")


#TESTING PURPOSSES ONLY!!!
class Register(Resource):
  def post(self):
    data = parser.parse_args()
    if UserModel.find_by_username(data['username']):
      return {'message':'user already exists'}
    new_user = UserModel(username = data['username'], password = UserModel.gen_hash(data['password']))
    try:
      new_user.save_to_db()
      return {'message':'all good with user creation'}
    except Exception as e:
      print e
      return {'message':'failed user creation'}, 500
#TESTING PURPOSSES ONLY!!!

class Login(Resource):
  def post(self):
    data = parser.parse_args()
    user = UserModel.find_by_username(data['username'])
    if not user:
      return {'message':'User does not exist'}
    
    if UserModel.verify_hash(data['password'], user.password) and data['grant_type'] == 'password':
      access_token = create_access_token(identity = data['username'])
      return {
        "access_token":access_token,
        "token_type":"bearer",
        "expires_in":3600,
        "claim_level":"complete"
      }
    else:
      return {'message':'failed to log in'}
  