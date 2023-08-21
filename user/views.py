from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .firebase import FirebaseAuthentication
from .serializers import UserProfileSerializer , FollowSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import User

class ProtectedApiView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user 
        return Response({"message": f"Authenticated user: {user.username}"})
    
class UserApiView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serialized_user = UserProfileSerializer(user)
        return Response(serialized_user.data)
    
    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors, status=400)
            

class FollowView(APIView):
    def post(self, request, user_id):
        if request.user.is_authenticated:
            User = get_user_model()
            me = request.user
            you = User.objects.get(pk=user_id)
            serializer = FollowSerializer(me)
            if me != you:
                if you.followers.filter(pk=me.pk).exists():
                    you.followers.remove(me)
                else:
                    you.followers.add(me)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response('You must login first', status=status.HTTP_405_METHOD_NOT_ALLOWED )
        
            # if me in you.followers.all():
            #     you.followers.remove(me)
            #     return Response(f'unfollow {serializer.data}', status=status.HTTP_200_OK)
            # else:
            #     you.followers.add(me)
            #     return Response(f'follow {serializer.data}', status=status.HTTP_200_OK)
