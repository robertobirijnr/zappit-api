import jwt
import datetime
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from jwt.exceptions import DecodeError, ExpiredSignatureError

def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    token = token.decode('utf-8')  # Decode the token to string
    print(f"Generated Token: {token}")  # Debug print
    return token

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            return None
        
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        print(f"Retrieved Token: {token}")  # Debug print

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print(f"Decoded Payload: {payload}")  # Debug print
        except ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except DecodeError as e:
            raise exceptions.AuthenticationFailed(f'Decode error: {str(e)}')

        user = get_user_model().objects.filter(id=payload['user_id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        
        return (user, None)
