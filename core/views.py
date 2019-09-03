from django.core.files import File
from django.core.files.images import ImageFile
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.pathfinder import Draw
from pathlib import Path
from PIL import Image
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.serializers import MapSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError


from core.models import Map
from core.forms import NewMapForm
# Create your views here.

def index(request):

    new_map = Map.objects.last()
    # data_file = new_map.data

    # file = open(Path(data_file.path))

    # test_map = Draw(file, new_map.pk)
    # file_path = test_map.draw_map()
    # print(file_path)
    # new_map_image_file = open(Path(file_path), 'rb')
    # f = File(new_map_image_file)
    # new_map.image.save(name="elevation_map3.png", content=f)
    # new_map.save()
    # print(new_map.image.path)
    # print(new_map.image.url)

    # f.close()
    # new_map_image_file.close()
    # file.close()

    return render(request, "base.html", {'map': new_map})

 
class AllMaps(generics.ListAPIView):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

@csrf_exempt
@api_view(['POST'])
def generate_new_map(request):
    parser_class = (FileUploadParser,)

    name = request.data['name']
    # user = request.user
    if 'data' not in request.data:
        raise ParseError("Empty content")

    f = request.data['data']

   
    data_file = request.data['data']
    
    file = open(Path(data_file), 'r')
    new_map = Map.objects.create(
        name=name
    )
    new_map.my_file_field.save(f.name, f, save=True)
    new_map.data.save(name='data' + str(new_map.pk) + '.txt', content=File(file))

    test_map = Draw(file, new_map.pk)
    file_path = test_map.draw_map()
    print(file_path)
    new_map_image_file = open(Path(file_path), 'rb')
    f = File(new_map_image_file)
    new_map.image.save(name="elevation_map3.png", content=f)
    new_map.save()
    print(new_map.image.path)
    print(new_map.image.url)

    f.close()
    new_map_image_file.close()
    file.close()

    r = {"created": {
        "name": new_map.name,
        "user": new_map.user,
        "data": new_map.data,
        "img": new_map.image
        }}
        
    return Response(r, status=status.HTTP_201_CREATED)

