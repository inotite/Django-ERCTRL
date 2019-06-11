import json
import statistics
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.db.models import Min, Max
from django.http import HttpResponse
from erm_auth.views import BaseLoginRequired
from erm_room.models import PuzzlesSummary


class AjaxTrackerView(BaseLoginRequired, TemplateView):
    template_name = "users/tracker.html"
    model = User

    def dispatch(self, *args, **kwargs):
        resp = super(AjaxTrackerView,
                     self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            super(AjaxTrackerView, self).get_context_data(**kwargs)
            tracker_type = self.request.GET.get('tracker_type', None)
            start_date = self.request.GET.get('start_date', None)
            end_date = self.request.GET.get('end_date', None)
            user_profile = self.request.user.profile
            if tracker_type == "year":
                tracker_list = user_profile.get_year_graph_source_data()
            elif tracker_type == "month":
                tracker_list = user_profile.get_month_graph_source_data()
            elif tracker_type == "date_range":
                tracker_list = user_profile.get_range_graph_source_data(
                    start_date=start_date, end_date=end_date)
            else:
                tracker_list = user_profile.get_graph_source_data()
            return HttpResponse(json.dumps({'tracker_list': tracker_list}),
                                status=200, content_type="application/json")
        else:
            return resp


class UserStatusView(BaseLoginRequired, TemplateView):
    template_name = None

    def dispatch(self, *args, **kwargs):
        resp = super(UserStatusView,
                     self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            super(UserStatusView, self).get_context_data(**kwargs)
            status = self.request.POST.get('status', None)
            user_id = self.request.POST.get('user_id', None)
            user = User.objects.get(pk=user_id)
            if status == "Active":
                user.is_active = False
            else:
                user.is_active = True
            user.save()
            current_status = "Active" if user.is_active else "Deactive"
            return HttpResponse(json.dumps({'status': current_status, 'userId': user.id}),
                                status=200, content_type="application/json")
        else:
            return resp


class AjaxUserRoomSummaryView(BaseLoginRequired, TemplateView):

    def dispatch(self, *args, **kwargs):
        resp = super(AjaxUserRoomSummaryView,
                     self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            super(AjaxUserRoomSummaryView, self).get_context_data(**kwargs)
            summary_json = json.loads(self.request.body.decode("utf-8"))
            solved_time = summary_json.get('solved_time').replace(':','.')
            summary_json['play_user_id'] = self.request.user.id
            summary_json.pop('solved_time')
            #summary_json.pop('play_count')
            summary_json.update({'play_count':-1})
            summary_json.pop('is_delete')
            summary_json.pop('roomId')
            try:
                max_time = PuzzlesSummary.objects.filter(puzzle=summary_json['puzzle_id']).aggregate(Max('max_time'))
                min_time = PuzzlesSummary.objects.filter(puzzle=summary_json['puzzle_id']).aggregate(Min('min_time'))
            except:
                pass
            try:
                if float(solved_time) > max_time['max_time__max']:
                    _max = solved_time
                else:
                    _max = min_time['max_time__max']

            except:
                _max = solved_time

            try:
                if float(solved_time) < min_time['min_time__min']:
                    _min = solved_time
                else:
                    _min = min_time['min_time__min']
            except:
                _min = solved_time

            puzzle, status = PuzzlesSummary.objects.get_or_create(
                **summary_json)

            puzzle.solved_time = solved_time
            puzzle.mean_time = statistics.mean([float(_min),float(_max)])
            puzzle.median_time = statistics.median([float(_min),float(_max)])
            puzzle.max_time = _max
            puzzle.min_time = _min
            puzzle.save()
            return HttpResponse(json.dumps({'puzzle_id': puzzle.id}),
                                status=200, content_type="application/json")
        else:
            return resp
