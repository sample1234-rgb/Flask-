from model.user import UserModel
from werkzeug.security import safe_str_cmp

def authenticate(username, password):
    u = UserModel.find_by_username(username)
    if u and safe_str_cmp(u.password, password):
        return u

def identity(payload):
    _id = payload['identity']
    return UserModel.find_by_id(_id)
