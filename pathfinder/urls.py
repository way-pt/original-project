"""pathfinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

import core.views
import frontend.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('map_view/', core.views.googleMapView, name='map-view'),
    path('', frontend.views.index, name="index"),
    path('api/map/<pk>', core.views.map_view, name='map-view'),
    path('api/all_maps/', core.views.AllMaps.as_view(), name="api-all"),
    path('api/user_maps/<user>', core.views.user_maps, name='api-user'),
    path('api/user_recents/', core.views.user_recents, name='api-user-recents'),
    # path('api/recent_map/', views.latest_map, name='api-recent'),
    path('api/new_map/filename=<filename>', csrf_exempt(core.views.GenerateMap.as_view()), name='api-new'),
    path('api/save_map/', core.views.save_map, name='api-save'),
    path('api/markers/', core.views.GetMarkers.as_view(), name='api-markers'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
