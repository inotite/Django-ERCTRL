# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import statistics
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Max
from erm_room.models import (Room, Clue, RoomImages, Sounds, Videos, Puzzles,
                             LiveViewFont, PuzzlesSummary, Scoring, PuzzleClue,
                             PhilipGroupsAndScenes)
from erm_auth.views import BaseLoginRequired
from erm_room.forms import (RoomCreateForm, RoomClueForm, RoomImagesForm,
                            SoundsForm, VideosForm, PuzzlesForm,
                            UserRoomCreateForm, TabletRoomCreateForm,
                            GuideRoomCreateForm, GuideRoomEditForm,
                            ScoringForm, EndingGameForm)
from custom_weasyprint import WeasyTemplateResponseMixin
from erm_room.managers import RoomManager
from helpers.decorators import administration_required


@method_decorator(administration_required, name='dispatch')
class RoomCreate(BaseLoginRequired, CreateView):
    """
    Room view for creating an new object instance.
    """
    template_name = "rooms/create_room.html"
    form_class = UserRoomCreateForm
    success_url = reverse_lazy('dashboard_rooms')

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        response = super(RoomCreate, self).form_valid(form)
        return response


@method_decorator(administration_required, name='dispatch')
class RoomUpdate(BaseLoginRequired, UpdateView):
    """
    Updating an room object.
    """
    template_name = "rooms/edit_room.html"
    model = Room
    success_url = reverse_lazy('dashboard_rooms')
    fields = '__all__'

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        response = super(RoomUpdate, self).form_valid(form)
        return response


@method_decorator(administration_required, name='dispatch')
class RoomList(BaseLoginRequired, ListView):
    template_name = "rooms/room-list.html"
    model = Room

    def get_queryset(self):
        """Returns Polls that belong to the current user"""
        parent_users = self.request.user.profile.user_employees.values_list(
            "parent__user", flat=True)
        rooms = Room.objects.filter(
            user__in=parent_users, is_tablet_room=False, is_guide_room=False,
            user__is_superuser=False)
        current_user_rooms = Room.objects.filter(
            user=self.request.user, is_tablet_room=False, is_guide_room=False)
        if rooms:
            return rooms | current_user_rooms
        return current_user_rooms


class RoomDetailView(BaseLoginRequired, DetailView):
    template_name = "rooms/room_details.html"
    model = Room

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user.profile.is_administrator():
            base_portal = "portals/base_administration_portal.html"
            context['isAdmin'] = True
        else:
            base_portal = "portals/base_user_portal.html"
            context['isAdmin'] = False
        context['eventList'] = self.get_object().event_and_action_json('json')
        context['customActions'] = self.get_object().custom_event_of_actions()
        context['base_portal'] = base_portal
        phSetting, phGroups, phScenes = self.get_object().get_groups_and_scenes_by_ph_settings()
        context['phSetting'] = phSetting
        context['phGroups'] = phGroups
        context['phScenes'] = phScenes

        return context


@method_decorator(administration_required, name='dispatch')
class RoomCreateView(BaseLoginRequired, CreateView):
    """
    Room view for creating an new object instance.
    """
    form_class = RoomCreateForm
    template_name = "rooms/dashboards/room_create.html"
    success_url = reverse_lazy('dashboard_rooms')
    eventsList = []

    initial = RoomManager.get_room_initial_dict()

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        response = super(RoomCreateView, self).form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super(RoomCreateView, self).get_context_data(**kwargs)
        context['live_view_fonts'] = LiveViewFont.objects.all()
        context['form_action'] = 'dashboard_rooms_create'
        return context


@administration_required
@login_required
def create_clue(request):
    """
    Clue view for creating an new object instance,
    with a response rendered by template.
    """
    clue_form = RoomClueForm(request.POST or None)
    if clue_form.is_valid():
        clue_form.save()
    clues = Clue.objects.filter(room=request.POST.get('room'))
    clue_name = request.POST.get('name')
    html_content = render_to_string(
        "rooms/clues/include/_clue_table.html",
        {'clues': clues})

    return HttpResponse(
        json.dumps({'clue_data': html_content, 'clue_name': clue_name}),
        status=200, content_type="application/json")


@administration_required
@login_required
@csrf_exempt
def delete_clue(request, clue_id=None):
    """Clue view for deleting an clue object."""
    if not request.is_ajax():
        return HttpResponse(content="Invalid Request Method.", status=400)
    clue_id = request.POST.get('clue_id', None)

    clue = Clue.objects.get(id=clue_id)
    clue.delete()

    return HttpResponse(content=json.dumps({'success': True}), status=200)


@administration_required
@csrf_exempt
def edit_clue(request):
    """
    Updating an clue object,
    with a response rendered by template.
    """
    if not request.is_ajax():
        return HttpResponse(content="Invalid Request Method.", status=400)
    clue_id = request.POST.get("id", None)
    if clue_id:
        clue = Clue.objects.get(id=clue_id)
        clue.name = request.POST.get("name", None)
        clue.save()
    return HttpResponse(content=json.dumps({'success': True}), status=200)


@administration_required
@login_required
def edit_room(request, room_id=None):
    """
    Updating an room object.
    """
    initial_dict = {}
    live_view_fonts = LiveViewFont.objects.all()
    try:
        room = Room.objects.get(id=room_id)
        initial_dict = RoomManager.get_room_edit_initial_dict(room)
        form = RoomCreateForm(
            request.POST or None, request.FILES or None, initial=initial_dict, instance=room)
    except Room.DoesNotExist:
        room = None
        form = RoomCreateForm(request.POST or None, request.FILES or None)
    clue_form = RoomClueForm()
    image_form = RoomImagesForm()
    sound_form = SoundsForm()
    video_form = VideosForm()
    puzzle_form = PuzzlesForm()
    clues = Clue.objects.filter(room=room)
    images = RoomImages.objects.filter(room=room)
    sounds = Sounds.objects.filter(room=room)
    videos = Videos.objects.filter(room=room)
    puzzles = Puzzles.objects.filter(room=room)
    if form.is_valid():
        room_obj = form.save(commit=False)
        room_obj.user = request.user
        room_obj.save()
        return redirect('dashboard_rooms')

    if room_id:
        return render(request, 'rooms/dashboards/room_edit.html',
                      {'form': form, 'room_id': room.id, 'room': room,
                       'clue_form': clue_form, 'clues': clues,
                       'image_form': image_form, 'images': images,
                       'sound_form': sound_form, 'sounds': sounds,
                       'video_form': video_form, 'videos': videos,
                       'puzzle_form': puzzle_form, 'puzzles': puzzles,
                       'live_view_fonts': live_view_fonts, 'is_tablet': False,
                       'action_url': 'dashboard_rooms_update'})


@administration_required
@login_required
@csrf_exempt
def create_image(request):
    """
    Image view for creating an new object instance,
    with a response rendered by template.
    """
    room = request.POST.get('room')
    images = RoomImages.objects.filter(room=room)
    image_form = RoomImagesForm(request.POST or None, request.FILES or None)
    if image_form.is_valid():
        image_form.save()
        messages = 'Successfully saved'
        status = "ok"
    else:
        messages = image_form.errors['img_name']
        status = 'error'

    html_content = render_to_string(
        "rooms/room_images/image_create.html",
        {'images': images})

    return HttpResponse(
        json.dumps({'images_data': html_content, 'messages': messages,
                    'status': status}),
        status=200, content_type="application/json")


@administration_required
@login_required
@csrf_exempt
def delete_image(request, clue_id=None):
    """Image view for deleting an image object."""
    if not request.is_ajax():
        return HttpResponse(content="Invalid Request Method.", status=400)
    image_id = request.POST.get('image_id', None)

    image = RoomImages.objects.get(id=image_id)
    image.delete()

    return HttpResponse(content=json.dumps({'success': True}), status=200)


class RoomPuzzlePrintView(DetailView):
    model = Room
    template_name = 'rooms/puzzles/puzzle_details.html'


class RoomPuzzleViewPrintView(WeasyTemplateResponseMixin, RoomPuzzlePrintView):
    pass


class RoomPuzzleGmStatView(DetailView):
    model = Room
    template_name = 'rooms/puzzles/room_puzzle_gm_stat_details.html'

    def get_context_data(self, **kwargs):
        context = super(RoomPuzzleGmStatView, self).get_context_data(**kwargs)
        context['base_portal'] = self.request.user.profile.get_base_portal()
        return context


class UserRoomList(BaseLoginRequired, ListView):
    template_name = "rooms/user_dashboards/room-list.html"
    model = Room

    def get_queryset(self):
        parent_users = self.request.user.profile.user_employees.values_list(
            "parent__user", flat=True)
        rooms = Room.objects.filter(user__in=parent_users, is_tablet_room=False)
        return rooms


class RoomLiveViewmDetail(BaseLoginRequired, DetailView):
    model = Room

    def get_template_names(self):
        try:
            theme_name = self.get_object().theme.theme_name.lower()
            template_name = 'rooms/include/open_live_' + theme_name + '.html'
        except AttributeError:
            template_name = 'rooms/include/open_live_window.html'

        return template_name


# class NewRoomLiveViewmDetail(BaseLoginRequired, View):
#     model = Room

#     def get_template_name(self, room):
#         try:
#             theme_name = room.theme.theme_name.lower()
#             template_name = 'rooms/include/open_live_' + theme_name + '.html'
#         except AttributeError:
#             template_name = 'rooms/include/open_live_window.html'

#         return template_name

#     def get(self, request, *args, **kwargs):
#         room_id = kwargs.get('pk')
#         second = int(kwargs.get('second'))
#         room = Room.objects.get(pk=room_id)
#         return render(request, self.get_template_name(room), {
#             'room': room, 'second': second})


class RoomPuzzleGmPlayerStatusView(BaseLoginRequired, DetailView):
    model = Room
    template_name = 'rooms/puzzles/room_puzzle_gm_player_stat_details.html'

    def get_context_data(self, **kwargs):
        context = super(RoomPuzzleGmPlayerStatusView, self).get_context_data(**kwargs)

        if self.request.user.is_superuser or self.request.user.profile.is_administrator():
            base_portal = "portals/base_administration_portal.html"
        else:
            base_portal = "portals/base_user_portal.html"
        context['base_portal'] = base_portal

        rooms_puzzle = Puzzles.objects.filter(room=kwargs['object'])
        recent_puzzle = []
        recent_puzzle_parse = []
        result_list = []
        for rmp in rooms_puzzle:
            try:
                latest_object = PuzzlesSummary.objects.filter(play_user=self.request.user, puzzle_id=rmp.id,play_count=-1).first()
                recent_puzzle.append(latest_object)
                recent_puzzle_parse.append({'name': rmp.puzzle_name,'solved_time':latest_object.solved_time})
            except:
                recent_puzzle_parse.append({'name': rmp.puzzle_name,'solved_time':'NA'})

                #If no latest object found then take the recent most recent value
                most_recent_count = PuzzlesSummary.objects.filter(play_user=self.request.user, puzzle_id=rmp.id).aggregate(Max('play_count'))
                latest_object =  PuzzlesSummary.objects.filter(play_user=self.request.user, puzzle_id=rmp.id,play_count=most_recent_count['play_count__max']).first()

            sloved_time_list = []
            # calcualte the mean for each puzzle of room
            for pzm in PuzzlesSummary.objects.filter(play_user=self.request.user, puzzle_id=rmp.id):
                sloved_time_list.append(pzm.solved_time)

            mean = statistics.mean(sloved_time_list)
            median = statistics.median(sloved_time_list)

            result_list.append({'name': latest_object.puzzle.puzzle_name,'min':latest_object.min_time,'max':latest_object.max_time,'mean':mean,'median':median})

        context['latest_result'] = recent_puzzle_parse
        context['total_summery'] = result_list

        # add the count and repalce it by -1
        for pz in recent_puzzle:
            try:
                max_count = PuzzlesSummary.objects.filter(play_user=pz.play_user, puzzle_id=pz.puzzle_id).aggregate(Max('play_count'))
                no_count = PuzzlesSummary.objects.filter(play_user=pz.play_user, puzzle_id=pz.puzzle_id,play_count=-1)
                if max_count['play_count__max'] == -1:
                    count = 1
                else:
                    count = max_count['play_count__max'] + 1
                amend_object = no_count.first()
                amend_object.play_count = count
                amend_object.save()
            except:
                pass
        return context


class RoomPuzzleGmPlayerStatusViewPrintView(WeasyTemplateResponseMixin, RoomPuzzleGmPlayerStatusView):
    pass


@method_decorator(login_required, name='dispatch')
class TabletRoomListView(BaseLoginRequired, ListView):
    template_name = "rooms/tablets/room_list.html"
    model = Room

    def get_context_data(self, **kwargs):
        context = super(TabletRoomListView, self).get_context_data(**kwargs)
        context['base_portal'] = self.request.user.profile.get_base_portal()
        return context

    def get_queryset(self):
        rooms = Room.objects.filter(is_tablet_room=True)
        if self.request.user.is_superuser:
            return rooms
        if self.request.user.profile.is_normal_user():
            parent_users = self.request.user.profile.user_employees.values_list(
                "parent__user", flat=True)
            return rooms.filter(user__in=parent_users)

        return rooms.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class TabletRoomDetailsView(BaseLoginRequired, DetailView):
    template_name = "rooms/tablets/room_details.html"
    model = Room

    def get_context_data(self, **kwargs):
        context = super(TabletRoomDetailsView, self).get_context_data(**kwargs)
        context['base_portal'] = self.request.user.profile.get_base_portal()
        alert_tone = self.object.audio_alert
        alert_tone_url = alert_tone.url if alert_tone else "/static/audios/alert_tone.mp3"
        room_data = {
            'room_id': self.object.id,
            'userToken': self.request.session.session_key,
            'defaultTimeLimit': self.object.default_time_limit,
            'initialDataFeedText': self.object.display_timer_milliseconds,
            'relayPort': 4200,
            'audioAlertUrl': alert_tone_url,
            'audioAlertOnClueSend': self.object.audio_alert_on_clue_send,
            'displayMs': self.object.display_timer_milliseconds,
        }
        context["room_data"] = json.dumps(room_data)
        return context


@method_decorator(login_required, name='dispatch')
class TabletRoomLiveView(BaseLoginRequired, DetailView):
    template_name = "rooms/tablets/room_live.html"
    model = Room

    def get_context_data(self, **kwargs):
        context = super(TabletRoomLiveView, self).get_context_data(**kwargs)
        alert_tone = self.object.audio_alert
        alert_tone_url = alert_tone.url if alert_tone else "/static/audios/alert_tone.mp3",
        context['base_portal'] = self.request.user.profile.get_base_portal()
        room_data = {
            'room_id': self.object.id,
            'userToken': self.request.session.session_key,
            'defaultTimeLimit': self.object.default_time_limit,
            'initialDataFeedText': self.object.display_timer_milliseconds,
            'relayPort': 4200,
            'audioAlertUrl': alert_tone_url,
            'audioAlertOnClueSend': self.object.audio_alert_on_clue_send,
            'displayMs': self.object.display_timer_milliseconds,
        }
        context["room_data"] = json.dumps(room_data)
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TabletRoomLiveListView(BaseLoginRequired, ListView):
    template_name = "rooms/tablets/room_live_list.html"
    model = Room

    def get_context_data(self, **kwargs):
        context = super(TabletRoomLiveListView, self).get_context_data(
            **kwargs)
        return context

    def get_queryset(self):
        rooms = Room.objects.filter(is_tablet_room=True)
        if self.request.user.is_superuser:
            return rooms
        if self.request.user.profile.is_normal_user():
            parent_users = self.request.user.profile.user_employees.values_list(
                "parent__user", flat=True)
            return rooms.filter(user__in=parent_users)

        return rooms.filter(user=self.request.user)


@method_decorator(administration_required, name='dispatch')
class TabletRoomCreateView(BaseLoginRequired, CreateView):
    """
    Room view for creating an new object instance.
    """
    form_class = TabletRoomCreateForm
    template_name = "rooms/dashboards/room_create.html"
    success_url = reverse_lazy('tablet_rooms')
    eventsList = []

    initial = RoomManager.get_room_initial_dict()

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.is_tablet_room = True
        response = super(TabletRoomCreateView, self).form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super(TabletRoomCreateView, self).get_context_data(**kwargs)
        context['live_view_fonts'] = LiveViewFont.objects.all()
        context['form_action'] = 'tablet_dashboard_rooms_create'
        return context


@administration_required
@login_required
def edit_tablet_room(request, room_id=None):
    """
    Updating an room object.
    """
    initial_dict = {}
    live_view_fonts = LiveViewFont.objects.all()
    try:
        room = Room.objects.get(id=room_id)
        initial_dict = RoomManager.get_room_edit_initial_dict(room)
        form = TabletRoomCreateForm(
            request.POST or None, request.FILES or None, initial=initial_dict,
            instance=room)
    except Room.DoesNotExist:
        room = None
        form = TabletRoomCreateForm(request.POST or None, request.FILES or None)
    clue_form = RoomClueForm()
    clues = Clue.objects.filter(room=room)
    if form.is_valid():
        room_obj = form.save(commit=False)
        room_obj.user = request.user
        room_obj.is_tablet_room = True
        room_obj.save()
        return redirect('tablet_rooms')

    if room_id:
        return render(request, 'rooms/dashboards/room_edit.html',
                      {'form': form, 'room_id': room.id, 'room': room,
                       'clue_form': clue_form, 'clues': clues,
                       'live_view_fonts': live_view_fonts,
                       'is_tablet': True,
                       'action_url': 'dashboard_tablet_rooms_update'})


@method_decorator(login_required, name='dispatch')
class GuideRoomListView(BaseLoginRequired, ListView):
    template_name = "rooms/guides/room_list.html"
    model = Room

    def get_context_data(self, **kwargs):
        context = super(GuideRoomListView, self).get_context_data(**kwargs)
        context['base_portal'] = self.request.user.profile.get_base_portal()
        return context

    def get_queryset(self):
        rooms = Room.objects.filter(is_guide_room=True)
        if self.request.user.is_superuser:
            return rooms
        if self.request.user.profile.is_normal_user():
            parent_users = self.request.user.profile.user_employees.values_list(
                "parent__user", flat=True)
            return rooms.filter(user__in=parent_users)

        return rooms.filter(user=self.request.user)


@method_decorator(administration_required, name='dispatch')
class GuideRoomCreateView(BaseLoginRequired, CreateView):
    """
    Room view for creating an new object instance.
    """
    form_class = GuideRoomCreateForm
    template_name = "rooms/guides/room_create.html"
    success_url = reverse_lazy('dashboard_guide_rooms')

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.is_guide_room = True
        response = super(GuideRoomCreateView, self).form_valid(form)
        scoring = Scoring(score_title='Score', room=self.object)
        scoring.save()
        return response

    def get_context_data(self, **kwargs):
        context = super(GuideRoomCreateView, self).get_context_data(**kwargs)
        context['form_action'] = 'guide_dashboard_rooms_create'
        return context


@method_decorator(administration_required, name='dispatch')
class GuideRoomUpdate(BaseLoginRequired, UpdateView):
    """
    Updating an guide room object.
    """
    model = Room
    form_class = GuideRoomEditForm
    puzzles_form_class = PuzzlesForm
    scoring_form_class = ScoringForm
    ending_form_class = EndingGameForm
    template_name = "rooms/guides/room_edit.html"
    success_url = reverse_lazy('dashboard_guide_rooms')

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.is_guide_room = True
        response = super(GuideRoomUpdate, self).form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super(GuideRoomUpdate, self).get_context_data(**kwargs)
        context['action_url'] = 'guide_dashboard_rooms_update'
        context['scoring_action_url'] = 'guide_dashboard_rooms_update'
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'puzzles_form_class' not in context:
            context['puzzles_form'] = self.puzzles_form_class()
        if 'scoring_form_class' not in context:
            context['scoring_form'] = self.scoring_form_class(
                instance=self.object.room_scoring)
        context['puzzles'] = Puzzles.objects.filter(room=self.get_object())
        if self.request.session.has_key('guide_room_section'):
            context['tab_type_number'] = self.request.session.get('guide_room_section')
            self.request.session['guide_room_section'] = 1
        if 'ending_form_class' not in context:
            context['ending_form'] = self.ending_form_class(
                instance=self.get_object())
        return context


class TestPhilipsHueSetting(BaseLoginRequired, View):
    template_name = "rooms/phue_connection_settings.html"

    def get(self, request, *args, **kwargs):
        rooms = Room.objects.filter(
            user=request.user, is_tablet_room=False, is_guide_room=False)
        return render(request, self.template_name, {'rooms': rooms, 'room_id':rooms.first().id})


class PhilipsHueRoomSetting(BaseLoginRequired, View):

    def post(self, request, *args, **kwargs):
        philips_hue_settings = dict(request.POST)
        ph_settings_dict = {}
        try:
            json.loads(request.POST.get('settings'))
            ph_settings_dict = philips_hue_settings
        except TypeError:
            for ky, val in philips_hue_settings.items():
                ph_settings_dict = json.loads(ky)
        try:
            room_id = kwargs.get('room_id')
            philip_groups_and_scenes = PhilipGroupsAndScenes.objects.get(
                room_id=room_id)
            if philip_groups_and_scenes:
                philip_groups_and_scenes = PhilipGroupsAndScenes.objects.filter(
                    room_id=room_id, user=request.user)
                philip_groups_and_scenes.update(**ph_settings_dict)
            msg = "Data successfully update"
        except PhilipGroupsAndScenes.DoesNotExist:
            ph_settings_dict['room_id'] = kwargs.get('room_id')
            ph_settings_dict['user'] = request.user
            philip_groups_and_scenes = PhilipGroupsAndScenes.objects.create(
                **ph_settings_dict)
            msg = "Data successfully created"
        response_data = {'msg': msg}
        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")

    def get(self, request, *args, **kwargs):

        room_id = kwargs.get('room_id')
        philip_groups_and_scenes = PhilipGroupsAndScenes.objects.get(
            room_id=room_id, user=request.user)
        phSetting, _, _ = philip_groups_and_scenes.room.get_groups_and_scenes_by_ph_settings()
        is_connected = 1 if phSetting else 0
        philip_groups_and_scenes_obj = philip_groups_and_scenes.__dict__.copy()
        philip_groups_and_scenes_obj['is_connected'] = is_connected
        if '_room_cache' in philip_groups_and_scenes_obj:
            del philip_groups_and_scenes_obj['_room_cache']
        del philip_groups_and_scenes_obj['_state']
        return HttpResponse(json.dumps(philip_groups_and_scenes_obj),
                            content_type="application/json")
