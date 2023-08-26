import time,hashlib
from django.http import HttpResponse
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from post.utils.permissions import CustomPermission,CustomAuthentication


class CacheMediaAPIView(APIView):

    permission_classes = [CustomPermission]
    authentication_classes = [CustomAuthentication]

    def post(self, request):
        def generate_file_name(string):
            hash_object = hashlib.md5()
            hash_object.update(f'{string}{int(time.time()* 1000)}'.encode())
            return hash_object.hexdigest()[:32]
            
        image = request.FILES['file']
        image_hash = generate_file_name(request.user.nickname)
        image.name = f'user-{image_hash}.{image.name.split(".")[-1]}'
        image_key = f'image:{image_hash}'
        cache.set(image_key, image, timeout=3600) 
        
        return Response(image_key)
    
    def get(self, request):
        
        image_key = request.GET.get('key')
        content_type = request.GET.get('content_type')

        if not image_key.startswith("image:"):
            return Response("포맷이 올바르지 않습니다", status=400)
        
        image_data = cache.get(image_key)
        if image_data:
            return HttpResponse(image_data.read(), content_type=image_data.content_type)
        else:
            return HttpResponse(status=404)
        
