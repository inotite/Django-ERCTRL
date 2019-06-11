from django.conf.urls import url
from messages_system.views import ComposeMessage, InboxList
from messages_system.ajax import InboxMessageDelete, OutboxMessageDelete


urlpatterns = [
    url(r'^compose/$', ComposeMessage.as_view(), name='messages_compose'),
    url(r'^outbox/$', InboxList.as_view(), name='user_messages'),
    url(r'^users/inbox/message/(?P<pk>\d+)/delete$',
        InboxMessageDelete.as_view(), name='user_inbox_delete_message'),
    url(r'^users/outbox/message/(?P<pk>\d+)/delete$',
        OutboxMessageDelete.as_view(), name='user_outbox_delete_message'),
]
