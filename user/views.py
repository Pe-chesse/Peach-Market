from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .firebase import FirebaseAuthentication
from .serializers import UserProfileSerializer , FollowSerializer, PublicUserSerializer
from rest_framework import status
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
            

class FollowAPIView(APIView):

    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request, user_id):
        follow_method = request.GET.get('f',"")
        try:
            user = User.objects.get(pk = user_id)
            if follow_method:
                follow_users = PublicUserSerializer(user.followings,many=True)
            else:
                follow_users = PublicUserSerializer(user.followers,many=True)
            return Response(follow_users.data)
        except Exception as e:
            print(e)
            return Response("해당 유저를 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, user_id):
            me = request.user
            you = User.objects.get(pk=user_id)
            try:
                serializer = FollowSerializer(me)
                if me == you:
                    return Response("본인 팔로우 불가", status=status.HTTP_400_BAD_REQUEST)

                if me.followings.filter(pk=you.pk).exists():
                    me.followings.remove(you)
                else:
                    me.followings.add(you)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response("해당 유저를 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)
            