# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from erm_auth.views import BaseLoginRequired
from helpers.decorators import administration_required
from leaderboard.forms import LeaderboardForm
from erm_room.models import LiveViewFont, Room, GameRecord
from django.shortcuts import render, redirect, reverse
from leaderboard.models import Leaderboard
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from api.room.serializers import TabletRoomSerializer, UserRoomCreateSerializer
import csv


class LeadershipView(BaseLoginRequired, View):
    template_name = "leaderboard/open_leadership.html"

    def get(self, request):

        leaderboard = Leaderboard.objects.first()
        rooms = Room.objects.filter(user=request.user)
        room_boards = []

        for room in rooms:
            entries = GameRecord.objects.filter(room=room)
            total = len(entries)
            escaped = 0
            for entry in entries:
                if entry.time_remaining > 0:
                    escaped = escaped + 1
      
            if total > 0:
                escape_rate = round(((escaped / total) * 100), 2)
            else:
                escape_rate = 'NA'
            room_info = {'room': room, 'escape_rate':  escape_rate}

            # weekly data
            wday = datetime.now().weekday()
            week_start = (datetime.now() - timedelta(days=wday)).replace(hour=0, minute=0, second=0, microsecond=0)
            week_winners = GameRecord.objects.filter(room=room, completed_on__gte=week_start, time_remaining__gt=0).order_by('-time_remaining')[:5]
            for e in week_winners:
                e.time_left = "{}m:{}s".format(e.time_remaining//60, e.time_remaining%60)
            # monthly stats
            month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            month_winners = GameRecord.objects.filter(room=room, completed_on__gte=month_start, time_remaining__gt=0).order_by('-time_remaining')[:5]
            for e in month_winners:
                e.time_left = "{}m:{}s".format(e.time_remaining//60, e.time_remaining%60)
            #yearly stats
            year_start = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            year_winners = GameRecord.objects.filter(room=room, completed_on__gte=year_start, time_remaining__gt=0).order_by('-time_remaining')[:5]
            for e in year_winners:
                e.time_left = "{}m:{}s".format(e.time_remaining//60, e.time_remaining%60)
            # all time
            alltime_winners = GameRecord.objects.filter(room=room, time_remaining__gt=0).order_by('-time_remaining')[:5]
            for e in alltime_winners:
                e.time_left = "{}m:{}s".format(e.time_remaining//60, e.time_remaining%60)

            board = {'room': room, 'escape_rate':escape_rate, 'week_winners': week_winners, 'month_winners':month_winners, 'year_winners': year_winners, 'alltime_winners':alltime_winners}
            room_boards.append(board)
        
        return render(request, self.template_name, context={'leaderboard':leaderboard, 'room_boards':room_boards} )


class UserLeadershipView(BaseLoginRequired, TemplateView):
    template_name = "leaderboard/user_open_leadership.html"

    def get_context_data(self, **kwargs):

        context = super(LeadershipView, self).\
            get_context_data(**kwargs)
        leaderboard = Leaderboard.objects.first()
        room = Room.objects.last()
        context['leaderboard'] = leaderboard
        context['room'] = room

        return context


@method_decorator(administration_required, name='dispatch')
class LeaderBoardSettingsView(BaseLoginRequired, View):
    template_name = "leaderboard/leaderboard_create.html"

    def get(self, request, *args, **kwargs):

        live_view_fonts = LiveViewFont.objects.all()
        try:
            leaderboard = Leaderboard.objects.first()
            form = LeaderboardForm(request.POST or None, instance=leaderboard)
        except (Leaderboard.ObjectDoesNotExist, AttributeError):
            form = LeaderboardForm(request.POST or None)
        return render(request, self.template_name, {
            'form': form, 'live_view_fonts': live_view_fonts})

    def post(self, request, *args, **kwargs):
        live_view_fonts = LiveViewFont.objects.all()
        try:
            leaderboard = Leaderboard.objects.first()
            form = LeaderboardForm(request.POST or None, instance=leaderboard)
        except (Leaderboard.ObjectDoesNotExist, AttributeError):
            form = LeaderboardForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Leaderboard settings was successfully updated!')
            return redirect('leaderboard_settings')

        return render(request, self.template_name, {
            'form': form, 'live_view_fonts': live_view_fonts})

# Leaderboard List views
class LeaderboardListView(BaseLoginRequired, View):
    template_name = "leaderboard/entries.html"

    def get(self, request, room_id):
        try:
            if int(room_id) == 0:
                room = Room.objects.filter(user=request.user).first()
            else:
                room = Room.objects.get(id=room_id, user=request.user) 

            rooms = Room.objects.filter(user=request.user)
            # get the default/first room from the list
            entries = GameRecord.objects.filter(room=room) 
            for e in entries:
                e.time_left = "{}m:{}s".format(e.time_remaining//60, e.time_remaining%60)
            return render(request, self.template_name, context={'entries':entries, 'rooms':rooms, 'active_room': room} )

        except Exception as err:
            #print("Error {}".format(str(err)))
            print(str(err))
            return render(request, "404.html", context={} )


class LeaderboardImportView(BaseLoginRequired, View):
    template_name = "leaderboard/import_entries.html"

    def get(self, request):
        try:
            rooms = Room.objects.filter(user=request.user)
            return render(request, self.template_name, context={'rooms':rooms} )

        except Exception as err:
            return HttpResponse(status=404, reason=str(err))

class LeaderboardEntriesView(viewsets.ViewSet): 
    serializer_class = GameRecordSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    # @csrf_protect
    def save(self, request):
        try:
            # room = request.POST.get('room', '')

            csv_file  = request.FILES.get('csvfile', '')

            print(request.FILES)

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                print(row)
                record = dict(row)
                entry = GameRecord()
                if record['Team Name'] != "":
                    entry.team_name = record['Team Name']
                else:
                    entry.team_name = 'Unnamed'
                if record['Time Remaining'] != "":
                    entry.time_remaining = int(float(record['Time Remaining']))
                else:
                    entry.time_remaining = 0
                if record['Num Players'] != "":
                    entry.num_players = record['Num Players']
                else:
                    entry.num_players = 0
                if  record['Clues Given'] != "":
                    entry.num_clues   = record['Clues Given']
                else:
                    entry.num_clues = 0

                dt_string = record['Entry Date']
                dt_format_string = '%Y-%m-%d %H:%M:%S'
                if dt_string.find('+00:00') > 0:
                    dt_string = dt_string.partition('+00:00')[0]
                    if dt_string.find('.') > 0:
                        dt_format_string = '%Y-%m-%d %H:%M:%S.%f'
                
                entry.completed_on = datetime.strptime(dt_string, dt_format_string)
                # entry.room = Room.objects.get(id=int(room))
                room_name = record['Room']

                if room_name == "":
                    continue
                
                if Room.objects.filter(room_name=room_name).count() > 0:
                    entry.room = Room.objects.get(room_name=room_name)
                else:
                    Room(
                        room_name=room_name,
                        user=request.user
                    ).save()
                    entry.room = Room.objects.get(room_name=room_name)
                entry.save()

            return Response({})

        except Exception as err:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LeaderboardEntryCreateView(BaseLoginRequired, View):
    template_name = "leaderboard/add_entry.html"

    def get(self, request):
        try:
            rooms = Room.objects.filter(user=request.user)
            return render(request, self.template_name, context={'rooms':rooms, 'edit':False} )

        except Exception as err:
          return HttpResponse(status=404, reason=str(err))

    def post(self, request):
        try:
            name = request.POST.get('name', '')
            time_left = request.POST.get('time_left', '')
            nplayers = request.POST.get('num_players', '')
            nclues = request.POST.get('num_clues', '')
            room_id = request.POST.get('room','')
            completed = request.POST.get('completed', '')
            completed_dt = datetime.strptime(completed, '%m/%d/%Y %H:%M')

            room = Room.objects.get(id=int(room_id))
            entry = GameRecord.objects.create(team_name=name, 
                                                    time_remaining=int(time_left), 
                                                    num_players=int(nplayers), 
                                                    num_clues=int(nclues), 
                                                    completed_on=completed_dt,
                                                    room=room)

            return JsonResponse({'success':True, 'redirect': '/leaderboard/room/0/entries'})

        except Exception as err:
            return JsonResponse({'success':False, 'redirect': '/leaderboard/room/0/entries'})

class LeaderboardEntryEditView(BaseLoginRequired, View):
    template_name = "leaderboard/add_entry.html"

    def get(self, request, pk):
        try:
            rooms = Room.objects.filter(user=request.user)
            entry = GameRecord.objects.get(id=pk)
            return render(request, self.template_name, context={'rooms':rooms, 'entry':entry, 'edit': True} )

        except Exception as err:
            return HttpResponse(status=404, reason=str(err))

    def post(self, request, pk):
        try:
            name = request.POST.get('name', '')
            time_left = request.POST.get('time_left', '')
            nplayers = request.POST.get('num_players', '')
            nclues = request.POST.get('num_clues', '')
            room_id = request.POST.get('room','')
            completed = request.POST.get('completed', '')
            completed_dt = datetime.strptime(completed, '%m/%d/%Y %H:%M')

            room = Room.objects.get(id=int(room_id))
            entry = GameRecord.objects.get(id=pk)
            entry.team_name = name
            entry.time_remaining = time_left
            entry.num_players = nplayers
            entry.num_clues = nclues
            entry.completed_on = completed_dt
            entry.save()
            
            return JsonResponse({'success':True})

        except Exception as err:
            return JsonResponse({'success':False})

class LeaderboardEntryDeleteView(BaseLoginRequired, View):

    def post(self, request):
        try:
            key = request.POST.get('key', '')
            GameRecord.objects.get(id=int(key)).delete()
            return JsonResponse({'success':True})

        except Exception as err:
            return JsonResponse({'success':False})

class LeaderboardEntriesExportView(BaseLoginRequired, View):

    def get(self, request):
        try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="leaderboard_entries.csv"'

            writer = csv.writer(response)
            entries = GameRecord.objects.filter(room__user=request.user).select_related('room')
            writer.writerow(['Team Name', 'Time Remaining', 'Num Players', 'Num Clues', 'Completed Date', 'Room'])
            for e in entries:
                writer.writerow([e.team_name, e.time_remaining, e.num_players, e.num_clues, e.completed_on.strftime("%m/%d/%y %H:%M"), e.room.room_name])

            return response

        except Exception as err:
            return HttpResponse(status=404, reason=str(err))



class LeaderboardsPublic(BaseLoginRequired, View):
    template_name = "leaderboard/leaderboard_public.html"

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {
            'live_view_fonts': []})
