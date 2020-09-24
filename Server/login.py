import jwt
from enum import Enum
from state import DecodeTokenState
from flask import request, jsonify
from functools import wraps
from schema import User
from constant import SECRET_KEY


class TokenMachine(object):
    def __init__(self, secret_key=SECRET_KEY):
        self.secret_key = secret_key
        self.current_auth_user = None
        self.payload = None

    def token_encode(self, **kwargs):
        return jwt.encode(kwargs, self.secret_key, algorithm='HS256')

    def token_decode(self, token):
        try:
            self.payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            if "username" in self.payload:
                self.current_auth_user = User.query.filter_by(username=self.payload["username"]).first()
                return DecodeTokenState.SUCCESS
            else:
                return DecodeTokenState.InvalidTokenError
        except:
            self.current_auth_user = None
            self.payload = None
            return DecodeTokenState.InvalidTokenError
            
TOKEN_MACHINE = TokenMachine()

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        proto = request.get_json()
        if TOKEN_MACHINE.token_decode(proto["token"]) == DecodeTokenState.SUCCESS:
            return func(*args, **kwargs)

        return jsonify({
            "STATE": "TOKEN_ERROR"
        })
    return decorated_view 