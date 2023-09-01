from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserProfileSerializer, PublicUserSerializer
from bucket.utils.upload import upload_redis_to_bucket
from rest_framework import status
from .models import User
from post.models import Post
from post.serializers import PostListSerializer
from post.utils.permissions import CustomPermission,CustomAuthentication
from django.db.models import Q

class ProtectedApiView(APIView):

    def get(self, request):
        try:
            serialized_user = UserProfileSerializer(request.user)
            return Response(serialized_user.data,200)
        except Exception as e:
            return Response({'error' : e},403)

class NicknameVerifyApiView(APIView):
    permission_classes = [CustomPermission]
    authentication_classes = [CustomAuthentication]

    def get(self, request):
        try:
            nickname = request.GET.get('nickname',"")
            User.objects.get(nickname = nickname)
            return Response({"message": "사용 할 수 없는 닉네임입니다."},200)

        except:
            return Response({"message": "사용 가능한 닉네임입니다."},204)
    
class UserApiView(APIView):
    
    permission_classes = [CustomPermission]
    authentication_classes = [CustomAuthentication]

    def get(self, request):

        try:
            target = request.GET.get('user',"")
            if not target:
                return Response(status = 404)
            try:
                user = User.objects.get(nickname = target)
                posts = Post.objects.filter(user = user.pk)

                serialized_user = UserProfileSerializer(user)
                serialized_posts = PostListSerializer(posts,many = True,context={'request': request})
                return Response({
                    'user': serialized_user.data,
                    'post': serialized_posts.data,
                })
            except:
                return Response(status = 400)
                
        except Exception as e:
            return Response(str(e),400)
    
    def put(self, request):
        user = request.user
        data = request.data.copy()
        if data.get('email',''):
            data.pop('email')
            
        if data.get('nickname',''):
            
            try:
                nickname = request.GET.get('nickname',"")
                User.objects.get(nickname = nickname)
                return Response({"message": "사용 할 수 없는 닉네임입니다."},200)

            except:
                pass
            
        
        if data.get('image_key',''):
            upload_redis_to_bucket(user,data['image_key'])

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
        try:
            me = request.user
            you = User.objects.get(nickname=nickname)
            if me == you:
                return Response("본인 팔로우 불가", status=status.HTTP_400_BAD_REQUEST)
            try:
                if me.followings.filter(pk=you.pk).exists():
                    me.followings.remove(you)
                    serializer = PublicUserSerializer(me.followings.followers,many=True)
                    return Response(serializer.data,status=200)
                else:
                    me.followings.add(you)
                    serializer = PublicUserSerializer(me.followings.followers,many=True)
                return Response(serializer.data, status=201)
            except:
                return Response("올바르지 않은 요청 또는 오류", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("해당 유저를 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)
            

class UserSearchAPIView(APIView):
    
    permission_classes = [CustomPermission]
    authentication_classes = [CustomAuthentication]

    def get(self,request):
        user = request.GET.get('user',"")
        try:
            users = User.objects.filter(Q(nickname__icontains=user))
            serializer = PublicUserSerializer(users,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response("해당 유저를 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)