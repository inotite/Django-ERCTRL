import json


class UserManager():

    @classmethod
    def get_message_recipients_source(cls, user):
        source_recipients = []
        if user.is_superuser or user.profile.is_administrator():
            users = user.profile.get_administrator_users()
        else:
            users = user.profile.get_user_administrators()

        for usr in users:
            source_recipients_dict = {}
            source_recipients_dict['id'] = usr.id
            source_recipients_dict['text'] = usr.username
            source_recipients.append(source_recipients_dict)
        return json.dumps(source_recipients)
