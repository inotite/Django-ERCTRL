from django.forms import ModelForm
from erm_room.models import LiveViewFont, GameRecord
from leaderboard.models import Leaderboard

ROLE_TYPE_CHOICES = (
    ('0', 'admin'),
    ('1', 'user'),
)


class LeaderboardForm(ModelForm):

    class Meta:
        model = Leaderboard
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(LeaderboardForm, self).__init__(*args, **kwargs)
        live_view_fonts = LiveViewFont.objects.all()
        live_view_font_list = [(lvf.id, lvf.font_name.split(",")[0]) for lvf in live_view_fonts]
        self.fields['live_view_font'].choices = sorted(live_view_font_list)


class LeaderboardEntryForm(ModelForm):
     
    class Meta:
        model = GameRecord
        fields = ['team_name', 'time_remaining', 'num_players', 'num_clues', 'completed_on', 'room']
        labels = {
                   'team_name': 'Team Name',
                   'time_remaining': 'Time Left',
                   'num_payers': 'Number of players',
                   'num_clues': 'Number of clues',
                   'completed_on': 'Completed Date',
                   'room': 'Room',
                 }

