from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .firebase import FirebaseAuthentication
from .serializers import UserProfileSerializer

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
            


