from pathlib import Path

from django.core.files import File
from django.core.files.images import ImageFile
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from PIL import Image

from core.forms import NewMapForm
from core.models import Map
from core.pathfinder import Draw
from core.serializers import MapSerializer
from rest_framework import generics, status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

def index(request):

    new_map = Map.objects.last()
    print(request.user.get_username())
    return render(request, "base.html", {'map': new_map})

 


### API Views ###


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class AllMaps(generics.ListAPIView):
    queryset = Map.objects.all()
    serializer_class = MapSerializer


class GenerateMap(APIView):
    parser_classes = [FileUploadParser]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, filename, format=None):
        data_file = request.data['file']
        # file = open(Path(data_file, 'r'))
        file = data_file.open(mode='r')
        new_map = Map.objects.create()
        new_map.data.save(name='data' + str(new_map.pk) + '.txt', content=file)

        saved_file = new_map.data

        usableData = open(Path(saved_file.path))

        test_map = Draw(usableData, new_map.pk)
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
        usableData.close()

        r = {"newMap": {
            "pk": str(new_map.pk),
            "image": new_map.image.url
            }}
            
        return Response(r, status=status.HTTP_201_CREATED)
