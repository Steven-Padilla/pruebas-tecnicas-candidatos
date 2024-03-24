from decouple import config
import datetime
import jwt
from jwt import ExpiredSignatureError
import pytz
from calendar import timegm

class Security():

    secret = config('JWT_KEY')
    tz = pytz.timezone("America/Mexico_City")

    @classmethod
    def generate_token(cls, authenticated_user, service_code, is_user_system_central, user_type):

        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=60*3),
            'user_id': authenticated_user.id,
            'username': authenticated_user.username,
            'user_type': user_type,
            'service_code': service_code,
            'is_user_system_central': is_user_system_central,
            'roles': ['Administrator', 'Editor']
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")

    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]
            if (len(encoded_token) > 0):
                try:
                    payload = cls.decode_token(encoded_token)

                    if cls.validate_exp(payload):
                        raise ExpiredSignatureError("Signature has expired")
                    roles = list(payload['roles'])
                    if 'Administrator' in roles:
                        return True
                    return False
                except ExpiredSignatureError:
                    return False
                except jwt.InvalidSignatureError:
                    return False
        return False

    @classmethod
    def validate_exp(cls, payload):
        exp = payload["exp"]
        now = timegm(datetime.datetime.now(tz=cls.tz).utctimetuple())
        return exp <= now

    @classmethod
    def decode_token(cls, token):
        return jwt.decode(token, cls.secret, algorithms=["HS256"])

    @classmethod
    def get_payload_token(cls, headers):
        authorization = headers['Authorization']
        encoded_token = authorization.split(" ")[1]
        payload = cls.decode_token(encoded_token)
        if cls.validate_exp(payload):
            return {}
        return payload

    @classmethod
    def renew_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]
            if (len(encoded_token) > 0):
                    payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                    roles = list(payload['roles'])
                    if 'Administrator' in roles:
                        payload = {
                        'iat': datetime.datetime.now(tz=cls.tz),
                        'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=60),
                        'username': payload['username'],
                        'roles': ['Administrator', 'Editor']
                        }
                        return jwt.encode(payload, cls.secret, algorithm="HS256")
        return None
