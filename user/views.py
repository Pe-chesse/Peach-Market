from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserProfileSerializer , FollowSerializer, PublicUserSerializer
from bucket.utils.upload import upload_redis_to_bucket
from rest_framework import status
from .models import User
from post.utils.permissions import CustomPermission,CustomAuthentication

class ProtectedApiView(APIView):

    def get(self, request):
        user = request.user 
        return Response({"message": f"Authenticated user: {user.username}"})
    
class UserApiView(APIView):
    
    permission_classes = [CustomPermission]
    authentication_classes = [CustomAuthentication]

    def get(self, request):

        target = request.GET.get('user',"")
        if not target:
            user = request.user
        else:
            try:
                user = User.objects.get(nickname = target)
            except:
                return Response(status=404)
            
        serialized_user = UserProfileSerializer(user)
        return Response(serialized_user.data)
    
    def put(self, request):
        user = request.user
        data = request.data.copy()
        data.pop('email')
        if data['image_key']:
            image_key = data.pop('image_key')
            upload_redis_to_bucket(user,image_key)

        serializer = UserProfileSerializer(user,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors, status=400)
    

class FollowAPIView(APIView):
    
    permission_classes = [CustomPermission]
    authentication_classes = [CustomAuthentication]

    def get(self,request, nickname):
        follow_method = request.GET.get('f',"")
        try:
            user = User.objects.get(nickname=nickname)
            if follow_method:
                follow_users = PublicUserSerializer(user.followings,many=True)
            else:
                follow_users = PublicUserSerializer(user.followers,many=True)
            return Response(follow_users.data)
        except Exception as e:
            print(e)
            return Response("해당 유저를 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, nickname):
            me = request.user
            you = User.objects.get(nickname=nickname)
            try:
                serializer = FollowSerializer(me)
                if me == you:
                    return Response("본인 팔로우 불가", status=status.HTTP_400_BAD_REQUEST)

                if me.followings.filter(pk=you.pk).exists():
                    me.followings.remove(you)
                    return Response(status=204)
                else:
                    me.followings.add(you)
                return Response(serializer.data, status=201)
            except:
                return Response("해당 유저를 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)
            