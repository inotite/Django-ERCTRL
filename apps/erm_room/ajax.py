import json
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.contrib import messages
from erm_room.models import (Room, Clue, Sounds, Videos, Puzzles,
                             GameRecord, PuzzleClue)
from erm_room.forms import (RoomCreateForm, RoomClueForm,
                            RoomImagesForm, SoundsForm, VideosForm,
                            PuzzlesForm, GuideRoomCreateForm,
                            GuideRoomEditForm,
                            ScoringForm, EndingGameForm)
from erm_auth.views import BaseLoginRequired
from helpers.decorators import administration_required

class SoundsCreate(BaseLoginRequired, CreateView):
    """
    Sounds view for creating an new object instance,
    with a response rendered by template.
    """
    template_name = "rooms/sounds/sound_create.html"
    form_class = SoundsForm
    success_url = reverse_lazy('dashboard_rooms')

    def form_invalid(self, form):
        response = super(SoundsCreate, self).form_invalid(form)
        status = 'error'
        messages = form.errors['sound_img']
        if self.request.is_ajax():
            return HttpResponse(json.dumps({
                                'messages': messages, 'status': status}),
                                status=200, content_type="application/json")
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).

        self.object = form.save(commit=False)
        self.object.room_id = self.kwargs.get('room_id')
        response = super(SoundsCreate, self).form_valid(form)
        sounds = Sounds.objects.filter(room=self.object.room)
        status = "ok"
        if self.request.is_ajax():
            html_content = render_to_string(
                "rooms/sounds/sound-list.html",
                {'sounds': sounds, 'room_id': self.object.room})
            messages = 'Successfully saved'
            return HttpResponse(json.dumps({'sounds_data': html_content,
                                            'messages': messages, 'status': status}),
                                status=200, content_type="application/json")
        else:
            return response


class SoundsDelete(BaseLoginRequired, DeleteView):
    """Sounds view for deleting an sound object."""
    model = Sounds
    success_url = reverse_lazy('dashboard_rooms')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        resp = super(SoundsDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
        else:
            return resp


class VideosCreate(BaseLoginRequired, CreateView):
    """
    Videos view for creating an new object instance,
    with a response rendered by template.
    """
    template_name = "rooms/videos/video_create.html"
    form_class = VideosForm
    success_url = reverse_lazy('dashboard_rooms')

    def form_invalid(self, form):
        response = super(VideosCreate, self).form_invalid(form)
        status = 'error'
        messages = form.errors['video_img']
        if self.request.is_ajax():
            return HttpResponse(json.dumps({
                                'messages': messages, 'status': status}),
                                status=200, content_type="application/json")
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        status = "ok"
        self.object = form.save(commit=False)
        self.object.room_id = self.kwargs.get('room_id')
        response = super(VideosCreate, self).form_valid(form)
        videos = Videos.objects.filter(room=self.object.room)

        if self.request.is_ajax():
            html_content = render_to_string(
                "rooms/videos/video-list.html",
                {'videos': videos, 'room_id': self.object.room})
            messages = 'Successfully saved'
            return HttpResponse(json.dumps({'videos_data': html_content,
                                            'messages': messages, 'status': status}),
                                status=200, content_type="application/json")
        else:
            return response


class VideosDelete(BaseLoginRequired, DeleteView):
    """Videos view for deleting an Video object."""
    model = Videos
    success_url = reverse_lazy('dashboard_rooms')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        resp = super(VideosDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
        else:
            return resp


class PuzzlesCreate(BaseLoginRequired, CreateView):
    """
    Puzzles view for creating an new object instance,
    with a response rendered by template.
    """
    template_name = "rooms/puzzles/puzzle_create.html"
    form_class = PuzzlesForm
    success_url = reverse_lazy('dashboard_rooms')

    def form_invalid(self, form):
        response = super(PuzzlesCreate, self).form_invalid(form)
        status = 'error'
        messages = "Try again!!"
        if self.request.is_ajax():
            return HttpResponse(json.dumps({
                                'messages': messages, 'status': status}),
                                status=200, content_type="application/json")
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        self.object = form.save(commit=False)
        self.object.room_id = self.kwargs.get('room_id')
        response = super(PuzzlesCreate, self).form_valid(form)
        puzzles = Puzzles.objects.filter(room=self.object.room)
        status = "ok"
        messages = "Successfully saved"
        if self.object.room.is_guide_room:
            PuzzleClue.objects.bulk_create([
                PuzzleClue(puzzle=self.object, clue_type='Easy Clue'),
                PuzzleClue(puzzle=self.object, clue_type='Medium Clue'),
                PuzzleClue(puzzle=self.object, clue_type='Hard Clue')
            ])
            template_puzzle = "rooms/guides/puzzles-list.html"
        else:
            template_puzzle = "rooms/puzzles/puzzles-list.html"
        if self.request.is_ajax():
            html_content = render_to_string(
                template_puzzle,
                {'puzzles': puzzles, 'room_id': self.object.room})
            messages = 'Successfully saved'
            return HttpResponse(json.dumps({'puzzles_data': html_content,
                                            'messages': messages,
                                            'status': status}),
                                status=200, content_type="application/json")
        else:
            return response


class PuzzlesDelete(BaseLoginRequired, DeleteView):
    """Puzzle view for deleting an puzzle object."""

    model = Puzzles
    success_url = reverse_lazy('dashboard_rooms')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        resp = super(PuzzlesDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            Puzzles.objects.filter(id=kwargs['pk']).delete()
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
        else:
            return resp


@login_required
@csrf_exempt
def puzzles_update(request, room_id=None, puzzle_id=None):
    """
    Updating an puzzle object,
    with a response rendered by template.
    """
    try:
        puzzle = Puzzles.objects.get(id=puzzle_id)
        puzzle_form = PuzzlesForm(request.POST or None, instance=puzzle)
    except Room.DoesNotExist:
        puzzle = None
        puzzle_form = PuzzlesForm(request.POST or None)

    if request.method == 'POST':
        if puzzle_form.is_valid():
            puzzle_obj = puzzle_form.save(commit=False)
            puzzle_obj.room_id = room_id
            puzzle_obj.save()
            status = "ok"
            puzzles = Puzzles.objects.filter(room=room_id)
            html_content = render_to_string(
                "rooms/puzzles/puzzles-list.html",
                {'puzzles': puzzles})
            messages = 'Successfully updated'
            return HttpResponse(json.dumps({'puzzles_data': html_content,
                                            'messages': messages,
                                            'status': status}),
                                status=200, content_type="application/json")
        else:
            status = 'errors'
            messages = puzzle_form.errors
            return HttpResponse(json.dumps({'messages': messages,
                                            'status': status}),
                                status=200, content_type="application/json")
    else:

        return render(request, 'rooms/puzzles/_puzzle_create.html', {
            'puzzle_form': puzzle_form,
            'room_id': room_id, 'puzzle': puzzle
        })


class ClearCacheView(View):
    """ClearCache view for deleting an cache."""

    def get(self, request, *args, **kwargs):
        from django.core.cache import cache
        try:
            cache.clear()
            messages = 'Successfully clear cache'
        except AttributeError:
            messages = 'You have no cache configured!\n'
        response_data = {"messages": messages}
        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")


class RoomDelete(BaseLoginRequired, DeleteView):
    """Sounds view for deleting an sound object."""
    model = Room
    success_url = reverse_lazy('dashboard_rooms')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        resp = super(RoomDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
        else:
            return resp


class SaveGameResult(BaseLoginRequired, View):
    def post(self, request, *args, **kwargs):
        try:
            data_dict = request.POST.dict()
            data_dict.update({'room': Room.objects.get(id=data_dict['room'])})
            GameRecord.objects.create(**data_dict)
            return HttpResponse(json.dumps({'message': 'data udpated successfully'}),
                                content_type="application/json")
        except Exception as err:
            print(str(err))

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SaveGameResult, self).dispatch(*args, **kwargs)


class GuideRoomDelete(BaseLoginRequired, DeleteView):
    """GuideRoom view for deleting an room object."""
    model = Room
    success_url = reverse_lazy('dashboard_guide_rooms')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        resp = super(GuideRoomDelete, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
        else:
            return resp


@method_decorator(administration_required, name='dispatch')
class ScoringCreateAndUpdateView(BaseLoginRequired, View):
    """
    Scoring view for creating an new object instance.
    """
    form_class = ScoringForm
    template_name = "rooms/guides/scoring_create.html"

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            room_id = kwargs.get('room_id')
            room = Room.objects.get(pk=room_id)
            form = self.form_class(request.POST, instance=room.room_scoring)
            form.save()
            return render(request, self.template_name, {
                'scoring_form': form, 'object': room})


@method_decorator(administration_required, name='dispatch')
class EndingGameCreateAndUpdateView(BaseLoginRequired, View):
    """
    EndingGame view for creating an new object instance.
    """
    form_class = EndingGameForm
    template_name = "rooms/guides/ending_game_create.html"

    def post(self, request, *args, **kwargs):
        room_id = kwargs.get('room_id')
        room = Room.objects.get(pk=room_id)
        form = self.form_class(request.POST, request.FILES, instance=room)
        form.save()
        messages.success(
            request, 'Ending game setting was successfully updated!')
        request.session['guide_room_section'] = 4
        return redirect('guide_dashboard_rooms_update', pk=room_id)


@method_decorator(administration_required, name='dispatch')
class PuzzleClueCreateAndUpdateView(BaseLoginRequired, View):
    """
    PuzzleClue view for updating an new object instance.
    """
    template_name = "rooms/guides/puzzles-list.html"

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            clue_update_id = form = PuzzleClue.objects.get(
                id=request.POST['clue_id'])
            if 'clue_checkbox' in request.POST:
                form = PuzzleClue.objects.filter(id=clue_update_id.id).update(
                    clue_checkbox=True)
            else:
                form = PuzzleClue.objects.filter(id=clue_update_id.id).update(
                    clue_checkbox=False)
            if 'score_penatly' in request.POST:
                form = PuzzleClue.objects.filter(id=clue_update_id.id).update(
                    score_penatly=request.POST['score_penatly'])
            if 'clue_uploads_options' in request.POST:
                form = PuzzleClue.objects.filter(id=clue_update_id.id).update(
                    clue_uploads_options=request.POST['clue_uploads_options'])
            if 'clue_textarea' in request.POST:
                form = PuzzleClue.objects.filter(id=clue_update_id.id).update(
                    clue_textarea=request.POST['clue_textarea'])
                clue_value = PuzzleClue.objects.filter(
                    id=clue_update_id.id).first().clue_textarea
                return HttpResponse(json.dumps({'clue_id': clue_update_id.id,
                    'data': clue_value, 'file_upload_type': 'clue_textarea'}))
            if 'clue_icon' in request.FILES:
                form = PuzzleClue.objects.filter(id=clue_update_id.id).first()
                form.clue_icon = request.FILES['clue_icon']
                if not form.created:
                    form.created = timezone.now()
                form.updated = timezone.now()
                form.save()
                clue_value = PuzzleClue.objects.filter(
                    id=clue_update_id.id).first().clue_icon.url
                json_data = json.dumps({'clue_id': clue_update_id.id,
                    'data': clue_value, 'file_upload_type': 'clue_icon'})
                return HttpResponse(json_data, content_type='application/json')
            if 'clue_file_uploads' in request.FILES:
                form = PuzzleClue.objects.filter(id=clue_update_id.id).first()
                form.clue_file_uploads = request.FILES['clue_file_uploads']
                form.save()
                clue_value = PuzzleClue.objects.filter(
                    id=clue_update_id.id).first().clue_file_uploads.url
                json_data = json.dumps({'clue_id': clue_update_id.id,
                    'data': clue_value, 'file_upload_type': 'clue_file_upload'})
                return HttpResponse(json_data, content_type='application/json')
            return render(request, self.template_name, {'form': form})


@method_decorator(administration_required, name='dispatch')
class PuzzleClueOptionsView(BaseLoginRequired, View):
    """
    Puzzle Checkbox and Dashboard Icon view for updating an object instance.
    """
    template_name = "rooms/guides/puzzles-list.html"

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            puzzle_id = kwargs.get('puzzle_id')
            if 'enabled_puzzle_clue' in request.POST:
                form = Puzzles.objects.filter(id=puzzle_id).update(
                    enabled_puzzle_clue=True)
            else:
                form = Puzzles.objects.filter(id=puzzle_id).update(
                    enabled_puzzle_clue=False)
            if 'icon-clear' in request.POST:
                form = Puzzles.objects.filter(id=puzzle_id).first()
                form.dashboard_icon = None
                form.save()
                form_value = None
                json_data = json.dumps({
                    'data': form_value, 'puzzle_id': puzzle_id})
                return HttpResponse(json_data, content_type='application/json')
            if 'dashboard_icon' in request.FILES:
                form = Puzzles.objects.filter(id=puzzle_id).first()
                form.dashboard_icon = request.FILES['dashboard_icon']
                form.save()
                form_value = Puzzles.objects.filter(
                    id=puzzle_id).first().dashboard_icon.url
                json_data = json.dumps({
                    'data': form_value, 'puzzle_id': puzzle_id})
                return HttpResponse(json_data, content_type='application/json')
            return render(request, self.template_name, {'form': form})
