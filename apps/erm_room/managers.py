from erm_room.models import MicBiquadFilter
from erm_automation.models import Automation, EVENT_DICT


class RoomManager():

    @classmethod
    def get_room_initial_dict(cls):
        """Return initial dict value of room."""
        room_initial = {'num_clues': 3, 'clue_label': 'Clues',
                        'time_remaining_label': 'Time Remaining',
                        'communication_box_label': 'Data Feed',
                        'initial_data_feed_text': 'Awaiting Transmission...',
                        'success_screen_header': 'Company Name',
                        'failure_screen_header': 'Company Name',
                        'logo_max_height': 150, 'data_feed_distance_from_top': 0,
                        'data_feed_distance_from_left': 0,
                        'timer_distance_from_top': 0,
                        'timer_distance_from_left': 0, 'clue_count_img_width': 72,
                        'header_font_size': 24, 'timer_font_size': 160,
                        'clue_label_font_size': 72, 'text_clue_font_size': 48,
                        'room_end_header_font_size': 140,
                        'room_end_footer_font_size': 140,
                        'room_end_time_font_size': 250}
        return room_initial

    @classmethod
    def get_room_edit_initial_dict(cls, room=None):
        """Return initial dict value of room for edit."""
        initial_dict = {}
        mic_biquad_filters = MicBiquadFilter.objects.filter(name="On")
        for kr, vr in cls.get_room_initial_dict().items():
            value = getattr(room, kr)
            initial_dict[kr] = vr if value is None else value
        if mic_biquad_filters.exists() and not room.mic_biquad_filter:
            initial_dict['mic_biquad_filter'] = mic_biquad_filters.first()
        return initial_dict

    @classmethod
    def get_room_event_and_actions(cls, room=None, event_name=None):
        """Return actions list according to event selection."""
        event = EVENT_DICT.get(event_name)

        automations = Automation.objects.filter(
            room_id=room, event_reference__event__event_name=event)

        for automation in automations:
            for action_ref in automation.action_reference.all():
                action_references = {}
                action_references['action_name'] = action_ref.action.action_name
                if action_references['action_name'] == 'Send Clue Text':
                    action_references['clue'] = action_ref.clue_text
                if action_references['action_name'] == 'Play Alert Tone':
                    action_references['alert_tone'] = ''
                if action_references['action_name'] == 'Play Sound':
                    action_references['sound_name'] = action_ref.sound.name
                    action_references['sound_url'] = action_ref.sound.get_sound_filetype
                if action_references['action_name'] == 'Play Video':
                    action_references['video_name'] = action_ref.video.name
                    action_references['video_url'] = action_ref.video.get_video_filetype
                if action_references['action_name'] == 'Display Image':
                    action_references['image_name'] = action_ref.room_images.img_name.url
                if action_references['action_name'] == 'Send Network Request':
                    action_references['url'] = action_ref.url
                if action_references['action_name'] == 'Complete Puzzle':
                    action_references['puzzle_name'] = action_ref.puzzle.puzzle_name
                    action_references['reset_instructions'] = action_ref.puzzle.reset_instructions
                    action_references['damage_or_notes'] = action_ref.puzzle.damage_or_notes
                if action_references['action_name'] == 'Start Timer':
                    action_references['start_timer'] = ''
                if action_references['action_name'] == 'Stop Timer':
                    action_references['stop_timer'] = ''
                if action_references['action_name'] == 'Adjust Time':
                    action_references['time_to_adjust'] = action_ref.time_to_adjust
                if action_references['action_name'] == 'Complete Room':
                    action_references['complete_room'] = ''
                if action_references['action_name'] == 'Fail Room':
                    action_references['fail_room'] = ''
                if action_references['action_name'] == 'Reset Room':
                    action_references['reset_room'] = ''
                if action_references['action_name'] == 'Start VideoBrief':
                    action_references['start_video_brief'] = ''
                if action_references['action_name'] == 'Start Soundtrack':
                    action_references['start_soundtrack'] = ''
                if action_references['action_name'] == 'Stop Soundtrack':
                    action_references['stop_soundtrack'] = ''
                if action_references['action_name'] == 'Request Clue from GM':
                    action_references['request_clue_from_gm'] = ''
                if action_references['action_name'] == 'Run Script':
                    action_references['script_name'] = action_ref.script_name
                    action_references['script_text'] = action_ref.script_text
                yield action_references
