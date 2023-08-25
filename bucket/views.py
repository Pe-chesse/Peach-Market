import redis,base64,re,time,hashlib
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from user.firebase import FirebaseAuthentication


redis = redis.StrictRedis(host='localhost', port=6379, db=0)

class CacheMediaAPIView(APIView):
    
    def extract_content_type(self,base64_data):
        pattern = re.compile(r'data:image/([a-zA-Z]+);base64,')
        match = pattern.match(base64_data)
        
        if match:
            content_type = f'image/{match.group(1)}'
            return content_type
        
        return None

    def get(self, request):
        image_key = request.GET.get('key')
        base64_image_data = redis.get(image_key)
        image_data = base64.b64decode(base64_image_data)
        
        return FileResponse(image_data, content_type=self.extract_content_type(base64_image_data))
        
    
    def post(self, request):
        
        def generate_file_name(string):
            hash_object = hashlib.md5()
            hash_object.update(f'{string}{int(time.time())}'.encode())
            return hash_object.hexdigest()[:16]
            
        image_file = request.FILES['file']
        file_exp = image_file.name.split(".")[-1]
        
        image_data = image_file.read()
        base64_image_data = base64.b64encode(image_data).decode('utf-8')
        
        redis_key = f'image:{generate_file_name}.{file_exp}'
        redis.set(redis_key, base64_image_data)
        
        return Response(redis_key)