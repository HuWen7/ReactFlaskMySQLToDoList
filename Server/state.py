from enum import Enum


class LoginState(Enum):
    SUCCESS = 0
    FAIL = 1

class RegisterState(Enum):
    SUCCESS = 0
    ALREADY = 1
    EMPTY = 2
    UNKNOWN = 20

class DecodeTokenState(Enum):
    SUCCESS = 0
    ExpiredSignature = 1
    InvalidTokenError = 2
