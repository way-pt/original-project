from pathlib import Path

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from core.models import Map
from core.pathfinder import Draw
from core.serializers import MapSerializer
from rest_framework import generics, status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from pathfinder.settings import GCP_SECRET_KEY

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('auth_login'))
    
    context = {'google_key': GCP_SECRET_KEY}
    return render(request, "base.html", context)


def map_detail_view(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('auth_login')
    m = get_object_or_404(Map, pk=pk)
    context = {
        'name': m.name,
        'user': m.user.pk,
        'user_username': m.user.get_username(),
        'data_file': m.data.name,
        'image': m.image.url,
        'date': str(m.date),
        'pk': m.pk
    }

    return render(request, 'map_view.html', context)

 
def googleMapView(request):
    secret_key = f"https://maps.googleapis.com/maps/api/js?key={GCP_SECRET_KEY}&callback=initMap"
    context = {'secret_key': secret_key}

    return render(request, 'google_maps.html', context)





#################
### API Views ###
#################



# for use in development only

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # prevent csrf check




class AllMaps(generics.ListAPIView):
    queryset = Map.objects.all()
    serializer_class = MapSerializer


# class MostRecentMap(generics.ListAPIView):
#     serializer_class = MapSerializer
#     queryset = Map.objects.last()




@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@api_view(['GET'])
def user_maps(request, user):
    if not request.user.is_authenticated:
        raise PermissionDenied

    maps = Map.objects.filter(user=request.user)
    r = []

    for m in maps:
        dic = {
            'name': m.name,
            'image': m.image.url,
            'date': str(m.date),
            'pk': m.pk
        }
        r.append(dic)

    return Response(r)
     

# 5 most recent maps, shown on home page

@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@api_view(['GET'])
def user_recents(request):
    if not request.user.is_authenticated:
        raise PermissionDenied

    maps = Map.objects.filter(user=request.user)[:5]
    r = []

    for m in maps:
        dic = {
            'name': m.name,
            'image': m.image.url,
            'date': str(m.date),
            'pk': m.pk
        }
        r.append(dic)

    return Response(r)


# search endpoint *IN PROGRESS*

# @authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
# @api_view(['GET'])
# def search_maps(request, query):
#     if not request.user.is_authenticated:
#         raise PermissionDenied
    
#     maps = Map.objects.filter(user=request.user, )



# map detail view

@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@api_view(['GET'])
def map_view(request, pk):
    # if not request.user.is_authenticated:
    #     raise PermissionDenied

    m = Map.objects.get(pk=pk)

    # if not m.user == request.user:
    #     raise PermissionDenied

    r = {
            'name': m.name,
            'user': m.user.pk,
            'user_username': m.user.get_username(),
            'data_file': m.data.name,
            'image': m.image.url,
            'date': str(m.date),
            'pk': m.pk
        }

    return Response(r)


# used in development
@api_view(['GET'])
def latest_map(request):
    latest = Map.objects.last()

    r = {'map' : {
        'name': latest.name,
        'user': latest.user.get_username(),
        'data_url': latest.data.name,
        'image': latest.image.url,
        'date': str(latest.date),
        'pk': latest.pk

    }}
    return Response(r)




# endpoint that parses uploaded data file and generates .png map image.
# this view DOES NOT save the map to the user

class GenerateMap(APIView):
    parser_classes = [FileUploadParser]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, filename, format=None):
        data_file = request.data['file']
        # file = open(Path(data_file, 'r'))
        file = data_file.open(mode='r+b')
        new_map = Map.objects.create()
        new_map.data.save(name='data' + str(new_map.pk) + '.txt', content=file)

        saved_file = new_map.data

        print("file: ", file)
        print('data_file: ', data_file)

        # usableData = open(Path(saved_file.url))
        # usableData = data_file.read()
        # usableData.open()
        usableData = new_map.data.open(mode='r+b')
        print(usableData)
        # usableData = open(new_map.data.file, 'rb')


        test_map = Draw(usableData, new_map.pk)
        file_path = test_map.draw_map()
        print(file_path)
        new_map_image_file = open(Path(file_path), 'rb')
        f = File(new_map_image_file)
        new_map.image.save(name='elevation_map' + str(new_map.pk) + '.png', content=f)
        new_map.save()
        # print(new_map.imagegit )
        print(new_map.image.url)

        f.close()
        new_map_image_file.close()
        usableData.close()

        r = {"newMap": {
            "pk": str(new_map.pk),
            "image": new_map.image.url
            }}
            
        return Response(r, status=status.HTTP_201_CREATED)


# endpoint for saving a map to a user

@authentication_classes([CsrfExemptSessionAuthentication])
@api_view(['PATCH'])
def save_map(request):
    print(request.user)
    pk = request.data['pk']
    userPK = request.data['user']
    name = request.data['name']
    try:
        map_to_save = Map.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise NotFound({'map not found': {'pk': pk}})
    try:
        user = User.objects.get(pk=userPK)
    except ObjectDoesNotExist:
        raise NotFound({'User not found': {'pk': pk}})
    
    if(not name or len(name) > 50):
        raise ValidationError({'Invalid name entered. Must be within 1 and 50 characters'})
    
    map_to_save.user = user
    map_to_save.name = name
    map_to_save.save()
    user_username = user.get_username()
    data_file_name = map_to_save.data.name
    image_url = map_to_save.image.url

    r = {'map':{
        'name': name,
        'user': map_to_save.user.get_username(),
        'user_username': user_username,
        'data_file': data_file_name,
        'image': image_url,
        'date': str(map_to_save.date),
        'pk': pk}
    }

    return Response(r, status=status.HTTP_201_CREATED)



class GetMarkers(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied
        
        pts = []
        maps = Map.objects.filter(user=request.user)
        for m in maps:
            if m.lat:
                pts.append({
                    'pk': m.pk,
                    'name': m.name,
                    'points': [m.lat, m.lng]
                    })
        
        r = pts

        return Response(r)
