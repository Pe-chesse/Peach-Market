from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.common import MiddlewareMixin
from firebase_admin import auth
import firebase_admin
from django.contrib.auth import login
from peach_market.settings import env
from rest_framework import authentication
from .exceptions import FirebaseError
from .exceptions import InvalidAuthToken
from .exceptions import NoAuthToken
from .models import User
# import pyrebase

if not firebase_admin._apps:
    cred = firebase_admin.credentials.Certificate(env('FIREBASE_KEY_PATH'))
    firebase_admin.initialize_app(cred)
        
class FirebaseAuthentication(authentication.BaseAuthentication):
    
    def __init__(self, get_response):
        self.get_response = get_response

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            print(e)
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
            
        except Exception:
            raise FirebaseError()
        try:
            user = User.objects.get(username=uid)
        except :
            user = User.objects.create_user(
                username = uid,
                email=decoded_token.get("email")
            )
        request.user = user
        session_middleware = SessionMiddleware(self.get_response)
        session_middleware.process_request(request)
        return (user, None)
    

