from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from erm_room.models import (Room, Clue, RoomImages, Sounds, Videos, Puzzles,
                             MicBiquadFilter, LiveViewFont, Scoring,
                             PuzzleClue)

# Image upload limit
# set to 100 MB
MAX_SIZE = 150 * 1024 * 1024
# Audio upload limit
# set to 120 MB
MAX_AUDIO_UPLOAD_LIMIT = 150 * 1024 * 1024
# Video upload limit
# set to 100 MB
MAX_VIDEO_UPLOAD_LIMIT = 150 * 1024 * 1024


ROLE_TYPE_CHOICES = (
    ('0', 'admin'),
    ('1', 'user'),
)
ENDING_GAME_CHIOCE = (
    ('video ending', 'video ending'),
    ('text ending', 'text ending')
)


class RoomCreateForm(ModelForm):

    class Meta:
        model = Room
        exclude = ('user', 'admin_pin', 'success_ending_type',
                   'fail_ending_type')

    def __init__(self, *args, **kwargs):

        super(RoomCreateForm, self).__init__(*args, **kwargs)

        mic_biquad_filter = MicBiquadFilter.objects.filter(name="On")
        live_view_fonts = LiveViewFont.objects.all()
        live_view_font_list = [(lvf.id, lvf.font_name.split(",")[0])
                               for lvf in live_view_fonts]
        self.fields['clue_label'].required = False
        self.fields['time_remaining_label'].required = False
        self.fields['communication_box_label'].required = False
        self.fields['initial_data_feed_text'].required = False
        self.fields['success_screen_header'].required = False
        self.fields['success_screen_footer'].required = False
        self.fields['failure_screen_header'].required = False
        self.fields['failure_screen_footer'].required = False
        self.fields['theme'].required = False
        self.fields['background_video'].required = False
        self.fields['soundtrack'].required = False
        self.fields['success_audio'].required = False
        self.fields['failed_audio'].required = False
        self.fields['audio_alert'].required = False
        self.fields['video_brief'].required = False
        self.fields['success_video'].required = False
        self.fields['fail_video'].required = False
        self.fields['header_font_size'].required = True
        self.fields['timer_font_size'].required = True
        self.fields['clue_label_font_size'].required = True
        self.fields['text_clue_font_size'].required = True
        self.fields['room_end_header_font_size'].required = True
        self.fields['room_end_footer_font_size'].required = True
        self.fields['room_end_time_font_size'].required = True
        self.fields['data_feed_distance_from_top'].required = True
        self.fields['data_feed_distance_from_left'].required = True
        self.fields['timer_distance_from_top'].required = True
        self.fields['timer_distance_from_left'].required = True
        self.fields['clue_count_img_width'].required = True
        self.fields['num_clues'].required = True
        self.fields['live_view_font'].choices = sorted(live_view_font_list)
        if mic_biquad_filter.exists():
            self.fields['mic_biquad_filter'].initial = mic_biquad_filter.first()

    def clean_soundtrack(self):
        content_types = ['audio/mp3', 'audio/ogg', 'audio/mpeg', 'audio/wav']
        file = self.cleaned_data['soundtrack']
        try:
            c_type = file.content_type
            if c_type not in content_types:
                raise ValidationError(
                    "File type not supported! File must be .mp3 or .ogg")
            elif file.size > MAX_AUDIO_UPLOAD_LIMIT:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 120MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_success_audio(self):
        content_types = ['audio/mp3', 'audio/ogg', 'audio/mpeg']
        file = self.cleaned_data['success_audio']
        try:
            c_type = file.content_type
            if c_type not in content_types:
                raise ValidationError(
                    "File type not supported! File must be .mp3 or .ogg")
            elif file.size > MAX_AUDIO_UPLOAD_LIMIT:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 120MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_failed_audio(self):
        content_types = ['audio/mp3', 'audio/ogg', 'audio/mpeg']
        file = self.cleaned_data['failed_audio']
        try:
            c_type = file.content_type
            if c_type not in content_types:
                raise ValidationError(
                    "File type not supported! File must be .mp3 or .ogg")
            elif file.size > MAX_AUDIO_UPLOAD_LIMIT:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 120MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_audio_alert(self):
        content_types = ['audio/mp3', 'audio/ogg', 'audio/mpeg']
        file = self.cleaned_data['audio_alert']
        try:
            c_type = file.content_type
            if c_type not in content_types:
                raise ValidationError(
                    "File type not supported! File must be .mp3 or .ogg")
            elif file.size > MAX_AUDIO_UPLOAD_LIMIT:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 120MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_video_brief(self):
        content_types = ['video/mp4', 'video/quicktime']
        file = self.cleaned_data['video_brief']
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "File type not supported! File must be .mp4")
            elif file.size > MAX_VIDEO_UPLOAD_LIMIT:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_success_video(self):

        content_types = ['video/mp4', 'video/quicktime']
        file = self.cleaned_data['success_video']
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "File type not supported! File must be .mp4")
            elif file.size > MAX_VIDEO_UPLOAD_LIMIT:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_fail_video(self):

        content_types = ['video/mp4', 'video/quicktime']
        file = self.cleaned_data['fail_video']
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "File type not supported! File must be .mp4")
            elif file.size > MAX_VIDEO_UPLOAD_LIMIT:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_background_video(self):
        content_types = ['video/mp4', 'video/quicktime']
        file = self.cleaned_data['background_video']
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "File type not supported! File must be .mp4")
            elif file.size > MAX_VIDEO_UPLOAD_LIMIT:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_logo(self):
        content_types = ['image/jpg', 'image/png',
                         'image/gif', 'image/bmp', 'image/jpeg']
        file = self.cleaned_data.get("logo")
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
            elif file.size > MAX_SIZE:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_overlay_image(self):
        content_types = ['image/jpg', 'image/png',
                         'image/gif', 'image/bmp', 'image/jpeg']
        file = self.cleaned_data.get("overlay_image")
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
            elif file.size > MAX_SIZE:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_clue_count_off_img(self):
        content_types = ['image/jpg', 'image/png',
                         'image/gif', 'image/bmp', 'image/jpeg']
        file = self.cleaned_data.get("clue_count_off_img")
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
            elif file.size > MAX_SIZE:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_clue_count_available_img(self):
        content_types = ['image/jpg', 'image/png',
                         'image/gif', 'image/bmp', 'image/jpeg']
        file = self.cleaned_data.get("clue_count_available_img")
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
            elif file.size > MAX_SIZE:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_clue_count_used_img(self):
        content_types = ['image/jpg', 'image/png',
                         'image/gif', 'image/bmp', 'image/jpeg']
        file = self.cleaned_data.get("clue_count_used_img")
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
            elif file.size > MAX_SIZE:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_background_image(self):
        content_types = ['image/jpg', 'image/png',
                         'image/gif', 'image/bmp', 'image/jpeg']
        file = self.cleaned_data.get("background_image")
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
            elif file.size > MAX_SIZE:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_end_game_success_background(self):
        content_types = ['image/jpg', 'image/png',
                         'image/gif', 'image/bmp', 'image/jpeg']
        file = self.cleaned_data.get("end_game_success_background")
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
            elif file.size > MAX_SIZE:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_end_game_failure_background(self):
        content_types = ['image/jpg', 'image/png',
                         'image/gif', 'image/bmp', 'image/jpeg']
        file = self.cleaned_data.get("end_game_failure_background")
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
            elif file.size > MAX_SIZE:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file

    def clean_leaderboard_image(self):
        content_types = ['image/jpg', 'image/png',
                         'image/gif', 'image/bmp', 'image/jpeg']
        file = self.cleaned_data.get("leaderboard_image")
        try:
            content_type = file.content_type
            if content_type not in content_types:
                raise ValidationError(
                    "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
            elif file.size > MAX_SIZE:
                raise ValidationError(
                    "The file you are trying to upload is too large (max 100MB)")
            return file
        except AttributeError:
            pass
        return file


class UserRoomCreateForm(ModelForm):

    class Meta:
        model = Room
        fields = ['room_name']


class RoomClueForm(ModelForm):

    name = forms.CharField(
        label='Clue Text', widget=forms.Textarea({'cols': '90', 'rows': '5'}),
        required=True,)

    class Meta:
        model = Clue
        fields = ['name', 'room']


class RoomImagesForm(ModelForm):

    img_name = forms.FileField(label='Room Image', required=True)

    class Meta:
        model = RoomImages
        fields = ['img_name', 'room']

    def clean_img_name(self):
        content_types = ['image/jpg', 'image/png',
                         'image/gif', 'image/bmp', 'image/jpeg']
        file = self.cleaned_data.get("img_name", False)
        content_type = file.content_type
        if content_type not in content_types:
            raise ValidationError(
                "Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
        elif file.size > MAX_SIZE:
            raise ValidationError(
                "The file you are trying to upload is too large (max 100MB)")
        return file


class SoundsForm(ModelForm):

    sound_img = forms.FileField(label='Sound Image', required=True)
    name = forms.CharField(required=True)

    class Meta:
        model = Sounds
        fields = ['sound_img', 'name']

    def clean_sound_img(self):
        content_types = ['audio/mp3', 'audio/ogg', 'audio/mpeg']
        file = self.cleaned_data['sound_img']
        content_type = file.content_type
        if content_type not in content_types:
            raise ValidationError(
                "File type not supported! File must be .mp3 or .ogg")
        elif file.size > MAX_AUDIO_UPLOAD_LIMIT:
            raise ValidationError(
                "The file you are trying to upload is too large (max 120MB)")
        return file


class VideosForm(ModelForm):

    video_img = forms.FileField(label='Video Image', required=True)
    name = forms.CharField(required=True)

    class Meta:
        model = Videos
        fields = ['video_img', 'name']

    def clean_video_img(self):
        content_types = ['video/mp4', 'video/quicktime']
        file = self.cleaned_data['video_img']
        content_type = file.content_type
        if content_type not in content_types:
            raise ValidationError("File type not supported! File must be .mp4")
        elif file.size > MAX_VIDEO_UPLOAD_LIMIT:
            raise ValidationError(
                "The file you are trying to upload is too large (max 100MB)")
        return file


class PuzzlesForm(ModelForm):

    class Meta:
        model = Puzzles
        fields = ['puzzle_name', 'reset_instructions', 'damage_or_notes']
        exclude = ('enabled_puzzle_clue', 'dashboard_icon')

    def __init__(self, *args, **kwargs):
        super(PuzzlesForm, self).__init__(*args, **kwargs)

        self.fields['puzzle_name'].required = True
        self.fields['reset_instructions'].required = False


class TabletRoomCreateForm(ModelForm):

    class Meta:
        model = Room
        exclude = ('user', 'theme', 'custom_js', 'custom_header_includes',
                   'hide_data_feed', 'hide_timer', 'soundtrack',
                   'data_feed_distance_from_top', 'loop_soundtrack',
                   'data_feed_distance_from_left', 'success_audio',
                   'timer_distance_from_top', 'timer_distance_from_left',
                   'overlay_image', 'clue_count_off_img', 'failed_audio',
                   'clue_count_available_img', 'clue_count_used_img',
                   'clue_count_img_width', 'background_video',
                   'loop_background_video', 'audio_alert_on_clue_send',
                   'start_background_video_on_timer_start',
                   'override_default_timer', 'audio_alert_on_image_clue_send',
                   'end_game_success_background', 'mic_biquad_filter',
                   'audio_alert_on_clue_count_change', 'success_video',
                   'play_soundtrack_on_timer_start', 'fail_video',
                   'end_game_failure_background', 'video_brief',
                   'start_timer_after_video_brief', 'lap_timer',
                   'fail_screen_after_fail_video', 'display_polling_output',
                   'success_screen_after_success_video',
                   'hide_time_remaining_on_failure', 'enable_time_warp',
                   'fail_ending_type', 'success_ending_type',
                   'admin_pin')

    def __init__(self, *args, **kwargs):
        super(TabletRoomCreateForm, self).__init__(*args, **kwargs)
        live_view_fonts = LiveViewFont.objects.all()
        live_view_font_list = [(lvf.id, lvf.font_name.split(",")[0])
                               for lvf in live_view_fonts]
        self.fields['clue_label'].required = False
        self.fields['time_remaining_label'].required = False
        self.fields['communication_box_label'].required = False
        self.fields['initial_data_feed_text'].required = False
        self.fields['success_screen_header'].required = False
        self.fields['success_screen_footer'].required = False
        self.fields['failure_screen_header'].required = False
        self.fields['failure_screen_footer'].required = False
        self.fields['audio_alert'].required = False
        self.fields['header_font_size'].required = True
        self.fields['timer_font_size'].required = True
        self.fields['clue_label_font_size'].required = True
        self.fields['text_clue_font_size'].required = True
        self.fields['room_end_header_font_size'].required = True
        self.fields['room_end_footer_font_size'].required = True
        self.fields['room_end_time_font_size'].required = True
        self.fields['num_clues'].required = True
        self.fields['live_view_font'].choices = sorted(live_view_font_list)


class GuideRoomCreateForm(ModelForm):

    class Meta:
        model = Room
        fields = ('room_name', 'default_time_limit', 'admin_pin')

    def __init__(self, *args, **kwargs):
        super(GuideRoomCreateForm, self).__init__(*args, **kwargs)

    def clean_admin_pin(self):
        admin_pin = self.cleaned_data['admin_pin']
        if not any(i.isdigit() for i in admin_pin):
            if not admin_pin.isnumeric():
                raise ValidationError('Invalid Admin Pin')
        elif len(admin_pin) < 4:
            raise ValidationError(
                'Ensure this value has at least 4 characters.(it has ({}))'.format(len(admin_pin)))
        return admin_pin


class GuideRoomEditForm(ModelForm):

    class Meta:
        model = Room
        fields = ('room_name', 'logo', 'default_time_limit',
                  'display_timer_milliseconds', 'video_brief',
                  'start_timer_after_video_brief', 'background_image',
                  'background_color', 'font_color', 'widget_header_color',
                  'admin_pin', 'default_time_limit', 'hint', 'final_code', 'hide_timer',
                  'hint_tap_exit', 'hints_full_screen')

    def __init__(self, *args, **kwargs):
        super(GuideRoomEditForm, self).__init__(*args, **kwargs)

    def clean_admin_pin(self):
        admin_pin = self.cleaned_data['admin_pin']
        if not any(i.isdigit() for i in admin_pin):
            if not admin_pin.isnumeric():
                raise ValidationError('Invalid Admin Pin')
        elif len(admin_pin) < 4:
            raise ValidationError(
                'Ensure this value has at least 4 characters.(it has ({}))'.format(len(admin_pin)))
        return admin_pin


class ScoringForm(ModelForm):

    class Meta:
        model = Scoring
        exclude = ('room',)

    def __init__(self, *args, **kwargs):
        super(ScoringForm, self).__init__(*args, **kwargs)
        self.fields['score_title'].required = True


class EndingGameForm(ModelForm):
    success_ending_type = forms.ChoiceField(
        choices=ENDING_GAME_CHIOCE, widget=forms.RadioSelect())
    fail_ending_type = forms.ChoiceField(
        choices=ENDING_GAME_CHIOCE, widget=forms.RadioSelect())

    class Meta:
        model = Room
        fields = ('success_video', 'success_screen_after_success_video',
                  'success_screen_header', 'success_screen_footer',
                  'end_game_success_background',
                  'game_end_screen_background_color', 'success_ending_type',
                  'game_end_screen_font_color', 'timer_font_size',
                  'success_timer_size', 'success_hide_timer',
                  'fail_video', 'fail_screen_after_fail_video',
                  'failure_screen_header', 'failure_screen_footer',
                  'end_game_failure_background', 'fail_font_size',
                  'fail_timer_size', 'hide_time_remaining_on_failure',
                  'fail_ending_type')

    def __init__(self, *args, **kwargs):
        super(EndingGameForm, self).__init__(*args, **kwargs)
