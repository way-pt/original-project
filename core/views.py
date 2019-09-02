from django.core.files import File
from django.core.files.images import ImageFile
from django.shortcuts import render
from core.pathfinder import Draw
from pathlib import Path
from PIL import Image

from core.models import Map
# Create your views here.

def index(request):

    new_map = Map.objects.last()
    data_file = new_map.data

    file = open(Path(data_file.path))

    test_map = Draw(file, new_map.pk)
    file_path = test_map.draw_map()
    print(file_path)
    new_map_image_file = open(Path(file_path), 'rb')
    # new_map_image = Image.open(new_map_image_file)
    f = File(new_map_image_file)
    # new_map.image('elevation_map_paths3.png', f.read())
    # print(new_map_image)
    # new_map_image.save()
    # new_map.image = new_map_image.open()
    # new_map.image = new_map_image
    new_map.image.save(name="elevation_map3.png", content=f)
    new_map.save()
    print(new_map.image.path)

    f.close()
    new_map_image_file.close()
    file.close()

    return render(request, "index.html", {'map': test_map})
