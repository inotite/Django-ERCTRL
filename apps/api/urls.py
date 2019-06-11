from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api.users.views import UserViewSet
from api.views import TokenValidateView
from api.room import views
from api.room.views import (RoomViewSet, get_room_event_and_actions,
                            tablet_room_list, guide_room_list, UserRoomCreate,
                            UserRoomDelete, setLightStatus,
                            get_remote_response)
# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'rooms', RoomViewSet, base_name='rooms')
urlpatterns = [
    # Escaprroom API
    url(r'^', include(router.urls)),
    # Include login URLs for the browseable API.
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^room/(?P<room_id>\d+)/event/(?P<event_name>\w+)$',
        get_room_event_and_actions,
        name='get_room_event_and_actions_list'),
    url(r'^token/validate/$', TokenValidateView.as_view(),
        name='token_validate'),
    url(r'^tablet-rooms/$', tablet_room_list),
    # all feauters of self guide room
    url(r'^guide_room_list/$', guide_room_list),
    url(r'^create-room', views.UserRoomCreate.as_view(),
        name='create_room'),
    url(r'^delete-room/(?P<room_id>\d+)', views.UserRoomDelete.as_view(),
        name='room_delete'),
    url(r'^(?P<username>\w+)/lights/(?P<light_id>\d+)/state/(?P<status>\w+)$',
        setLightStatus, name='set_light_status'),
    url(r'^get/remote/url/status$',
        get_remote_response, name='get_url_status'),

]
