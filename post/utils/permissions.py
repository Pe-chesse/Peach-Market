from rest_framework.permissions import BasePermission
from rest_framework import authentication
from user.firebase import FirebaseAuthentication


class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True 
        else:
            return bool(request.user and request.user.is_authenticated)
        
class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if request.method == 'GET':
            pass
        else:
            return FirebaseAuthentication.authenticate(self,request)