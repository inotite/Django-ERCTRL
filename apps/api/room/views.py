from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import permissions as new_permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from api.room.serializers import TabletRoomSerializer, UserRoomCreateSerializer
from erm_room.models import (
    Room, Puzzles, Scoring, PuzzleClue)
from erm_automation.models import (
    Automation, Event, Action, EventReference, ActionReference, EVENT_DICT)
from erm_room.managers import RoomManager
from . import serializers


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        This method return room list according to current user
        """
        user_type = self.request.user.is_superuser or self.request.user.profile.is_administrator()
        if user_type:
            rooms = Room.objects.filter(
                user=self.request.user,
                is_tablet_room=False, is_guide_room=False)
        else:
            parent_users = self.request.user.profile.user_employees.values_list(
                "parent__user", flat=True)
            rooms = Room.objects.filter(
                user__in=parent_users,
                is_tablet_room=False, is_guide_room=False)
        return rooms

    # def get_serializer_class(self):
    #     user = self.request.user
    #     if user.profile.is_administrator():
    #         return serializers.RoomSerializer
    #     return super(RoomViewSet, self).get_serializer()

    def to_room_json(self, room_data_type):
        room = self.get_object()
        user_room_json = {
            'room_id': room.id,
            'room_name': room.room_name,
            'room_' + room_data_type: {}
        }
        return user_room_json

    @detail_route()
    def clues(self, request, pk=None):
        """
        Returns a list of all the clues that the given
        room belongs to.
        """
        room = self.get_object()
        room_clue_json = self.to_room_json('clues')
        room_clues = room.room_clues.all()
        for clue in room_clues:
            room_clue_json['room_clues']['clue_id'] = clue.id
            room_clue_json['room_clues']['clue_name'] = clue.name
        return Response(room_clue_json)

    @detail_route()
    def images(self, request, pk=None):
        """
        Returns a list of all the images that the given
        room belongs to.
        """
        room = self.get_object()
        room_image_json = self.to_room_json('images')
        room_images = room.room_images.all()
        for image in room_images:
            room_image_json['room_images']['image_id'] = image.id
            room_image_json['room_images']['image_url'] = image.img_name.url
        return Response(room_image_json)

    @detail_route()
    def sounds(self, request, pk=None):
        """
        Returns a list of all the sounds that the given
        room belongs to.
        """
        room = self.get_object()
        room_sounds_json = self.to_room_json('sounds')
        room_sounds = room.room_sounds.all()
        for sound in room_sounds:
            room_sounds_json['room_sounds']['sound_id'] = sound.id
            room_sounds_json['room_sounds']['sound_url'] = sound.get_audio_url
            room_sounds_json['room_sounds']['sound_name'] = sound.name
        return Response(room_sounds_json)

    @detail_route()
    def videos(self, request, pk=None):
        """
        Returns a list of all the videos that the given
        room belongs to.
        """
        room = self.get_object()
        room_videos_json = self.to_room_json('videos')
        room_videos = room.room_videos.all()
        for video in room_videos:
            room_videos_json['room_videos']['video_id'] = video.id
            room_videos_json['room_videos']['video_url'] = video.get_video_url
            room_videos_json['room_videos']['video_name'] = video.name
        return Response(room_videos_json)

    @detail_route()
    def puzzles(self, request, pk=None):
        """
        Returns a list of all the puzzles that the given
        room belongs to.
        """
        room = self.get_object()
        room_puzzle_json = self.to_room_json('puzzles')
        room_puzzles = room.room_puzzles.all()
        for puzzle in room_puzzles:
            room_puzzle_json['room_puzzles']['puzzle_id'] = puzzle.id
            room_puzzle_json['room_puzzles'][
                'puzzle_name'] = puzzle.puzzle_name
            room_puzzle_json['room_puzzles'][
                'reset_instructions'] = puzzle.reset_instructions
            room_puzzle_json['room_puzzles'][
                'damage_or_notes'] = puzzle.damage_or_notes
        return Response(room_puzzle_json)

    @detail_route()
    def automations(self, request, pk=None):
        """
        Returns a list of all the automations that the given
        room belongs to.
        """
        room = self.get_object()
        room_automation_json = self.to_room_json('automations')
        room_automations = room.room_automations.all()
        room_automations_list = []
        for automation in room_automations:
            new_automations = {'event_reference': {}, 'action_reference': {}}
            action_reference_list = []
            event = automation.event_reference.event
            new_automations['automation_id'] = automation.id
            new_automations['event_reference']['event_id'] = event.id
            new_automations['event_reference']['event_name'] = event.event_name
            for action in automation.action_reference.all():
                action_reference_dict = {}
                action_reference_dict['action_id'] = action.id
                action_reference_dict[
                    'action_name'] = action.action.action_name
                action_reference_list.append(action_reference_dict)
            new_automations['action_reference'] = action_reference_list
            room_automations_list.append(new_automations)
        room_automation_json['room_automations'] = room_automations_list

        return Response(room_automation_json)


class UserRoomCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRoomCreateSerializer

    def post(self, request, format=None):
        room_data = request.data
        room_create_serializer_class = UserRoomCreateSerializer(
            data=request.data)
        if room_create_serializer_class.is_valid():
            room_name = room_data.get('room_name')
            new_room = Room(user=request.user, room_name=room_name)
            new_room.save()
            return Response(
                room_create_serializer_class.data,
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                room_create_serializer_class.errors,
                status=status.HTTP_400_BAD_REQUEST)


class UserRoomDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if request.user:
            try:
                room_id = kwargs['room_id']
                Room.objects.get(id=room_id).delete()
                return JsonResponse({'Message': "Room is Delete"}, safe=False)
            except Exception:
                return Response(
                    {'Error': "Room is Not delete"},
                    status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'Error': 'Invalid Token'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((new_permissions.AllowAny,))
def get_room_event_and_actions(request, room_id=None, event_name=None):
    actions = list(RoomManager.get_room_event_and_actions(room_id, event_name))
    return Response(actions)


def tablet_room_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        rooms = Room.objects.filter(is_tablet_room=False)
        serializer = TabletRoomSerializer(rooms, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def guide_room_list(request):
    """
    List all self guide room feauters.
    """
    user_type = request.user.is_superuser or request.user.profile.is_administrator()
    if user_type:
        room_objs = Room.objects.filter(
            is_guide_room=True, user=request.user).all()
    else:
        parent_users = request.user.profile.user_employees.values_list(
            "parent__user", flat=True)
        room_objs = Room.objects.filter(
            is_guide_room=True, user__in=parent_users).all()
    main_list = []
    for room_obj in room_objs:
        data_list = []
        data_dict = {}
        scoring_obj = room_obj.room_scoring
        puzzle_obj = room_obj.room_puzzles.all()
        data_dict['room'] = {
            'id': room_obj.id,
            'room_name': room_obj.room_name,
            'logo': room_obj.logo.url if room_obj.logo else "",
            'default_time_limit': room_obj.default_time_limit,
            'display_timer_milliseconds':
            room_obj.display_timer_milliseconds,
            'video_brief':
            room_obj.video_brief.url if room_obj.video_brief else "",
            'start_timer_after_video_brief':
            room_obj.start_timer_after_video_brief,
            'admin_pin': room_obj.admin_pin,
            'background_image':
            room_obj.background_image.url if room_obj.background_image else "",
            'background_color': room_obj.background_color,
            'font_color': room_obj.font_color,
            'widget_header_color': room_obj.widget_header_color,
            'hide_timer': room_obj.hide_timer,
            'hint': room_obj.hint,
            'final_code':
            room_obj.final_code if room_obj.final_code else "",
            'hint_tap_exit': room_obj.hint_tap_exit,
            'hints_full_screen': room_obj.hints_full_screen,
        }
        data_dict['ending'] = {
            'success_ending_type': room_obj.success_ending_type,
            'success_video':
            room_obj.success_video.url if room_obj.success_video else "",
            'success_ending_type': room_obj.success_ending_type,
            'success_screen_header':
            room_obj.success_screen_header,
            'success_screen_footer':
            room_obj.success_screen_footer,
            'end_game_success_background':
            room_obj.end_game_success_background.url if room_obj.end_game_success_background else "",
            'game_end_screen_background_color':
            room_obj.game_end_screen_background_color,
            'game_end_screen_font_color':
            room_obj.game_end_screen_font_color,
            'timer_font_size':
            room_obj.timer_font_size if room_obj.timer_font_size else "",
            'success_timer_size':
            room_obj.success_timer_size if room_obj.success_timer_size else "",
            'success_hide_timer': room_obj.success_hide_timer,
            'fail_ending_type': room_obj.fail_ending_type,
            'fail_video':
            room_obj.fail_video.url if room_obj.fail_video else "",
            'fail_ending_type': room_obj.fail_ending_type,
            'failure_screen_header': room_obj.failure_screen_header,
            'failure_screen_footer':
            room_obj.failure_screen_footer,
            'end_game_failure_background':
            room_obj.end_game_failure_background.url if room_obj.end_game_failure_background else "",
            'game_end_screen_background_color':
            room_obj.game_end_screen_background_color,
            'game_end_screen_font_color':
            room_obj.game_end_screen_font_color,
            'fail_font_size':
            room_obj.fail_font_size if room_obj.fail_font_size else "",
            'fail_timer_size':
            room_obj.fail_timer_size if room_obj.fail_timer_size else "",
            'fail_hide_timer': room_obj.hide_time_remaining_on_failure
        }
        data_dict['scoring'] = {
            'enable_scoring': scoring_obj.enable_scoring,
            'starting_score':
            scoring_obj.starting_score if scoring_obj.starting_score else "",
            'score_title': scoring_obj.score_title,
            'always_reduce': scoring_obj.always_reduce,
            'penalty_per_minute':
            scoring_obj.penalty_per_minute if scoring_obj.penalty_per_minute else "",
            'is_penalize': scoring_obj.is_penalize,
            'end_game_at_zero': scoring_obj.end_game_at_zero
        }
        puzzle_list = []
        for puzzle in puzzle_obj:
            # import pdb;pdb.set_trace()
            temp = {
                'room_id': room_obj.id,
                'puzzle_id': puzzle.id,
                'puzzle_name': puzzle.puzzle_name,
                'enabled_puzzle_clue': puzzle.enabled_puzzle_clue,
                'dashboard_icon':
                puzzle.dashboard_icon.url if puzzle.dashboard_icon else "",
            }
            clue_list = []
            clue_set_obj = puzzle.puzzleclue_set.all()
            for clue in clue_set_obj:
                clue_temp = {
                    'room_id': room_obj.id,
                    'clue_id': clue.id,
                    'clue_created': clue.created,
                    'clue_updated': clue.updated,
                    'clue_type': clue.clue_type,
                    'clue_uploads_options':
                    clue.clue_uploads_options if clue.clue_uploads_options else "",
                    'clue_textarea':
                    clue.clue_textarea if clue.clue_textarea else "",
                    'clue_file_uploads':
                    clue.clue_file_uploads.url if clue.clue_file_uploads else "",
                    'clue_icon':
                    clue.clue_icon.url if clue.clue_icon else "",
                    'clue_checkbox': clue.clue_checkbox,
                    'score_penatly':
                    clue.score_penatly if clue.score_penatly else ""
                }
                clue_list.append(clue_temp)
            temp['puzzle_clue'] = clue_list
            puzzle_list.append(temp)
        data_dict['puzzle'] = puzzle_list
        data_list.append(data_dict)
        main_list.append(data_list)
    return JsonResponse(main_list, safe=False)


@api_view(['GET'])
@permission_classes((new_permissions.AllowAny,))
def setLightStatus(request, username=None, light_id=None, status=False):
    from phue import Bridge
    # ip_address = '127.0.0.1:9000'
    ip_address = request.data.get('ip_address')
    b = Bridge(ip_address, username=username)
    b.connect()
    print(b.get_api())
    new_status = True if status == '1' else False
    b.set_light(int(light_id), 'on', new_status)
    ctx = {'on': new_status}
    return Response(ctx)


@api_view(['POST'])
@permission_classes((new_permissions.AllowAny,))
def get_remote_response(request):
    import requests
    import json
    remote_url = request.POST.get('url')
    try:
        remote_content = requests.get(remote_url, stream=True, timeout=30)
        remote_content.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("HTTP exception error: {}".format(err))
        return
    except requests.exceptions.RequestException as e:
        print("Exception error {}".format(e))
        return
    data = json.loads(remote_content.text)
    return Response(data)