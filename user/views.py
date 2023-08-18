from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .firebase import FirebaseAuthentication

class ProtectedApiView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,):
        user = request.user 
        return Response({"message": f"Authenticated user: {user.username}"})