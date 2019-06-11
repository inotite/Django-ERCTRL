"""escaperoom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from erm_auth.views import (UserListView, UserDeleteView,
                            create_user, LoginView, change_password,
                            activate, UserSignupWithSubscription,
                            charges_succeeded, subscription_created)
from django.conf import settings
from erm_room import views
from erm_automation import views as automation_views
from erm_business import views as business_views

from erm_billing.views import BillingUpdate
from leaderboard.views import (LeadershipView, UserLeadershipView, LeaderboardListView, 
                               LeaderboardEntryCreateView, LeaderboardEntryDeleteView, LeaderboardEntryEditView, 
                               LeaderboardImportView, LeaderboardEntriesView, LeaderboardEntriesExportView,
                               LeaderBoardSettingsView, LeaderboardsPublic)
from django.conf.urls.static import static
from erm_room.ajax import (VideosDelete, VideosCreate,
                           SoundsDelete, SoundsCreate, PuzzlesCreate,
                           PuzzlesDelete, puzzles_update, ClearCacheView,
                           RoomDelete, SaveGameResult, GuideRoomDelete,
                           ScoringCreateAndUpdateView,
                           EndingGameCreateAndUpdateView,
                           PuzzleClueCreateAndUpdateView,
                           PuzzleClueOptionsView)

from portals.views import (
    landpage, landpage_administration, landpage_user, landpage_guest, ContactView)
from django.views.generic import TemplateView
from erm_automation.ajax import (RoomByAutomationDetailView, AutomationDelete)
from django.contrib.auth import views as auth_views
from users.views import (TrackerDetailView, TrackerView, PricingView,
                         PlanCreateView, PlanListView)
from users.ajax import AjaxTrackerView, UserStatusView, AjaxUserRoomSummaryView


urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^administration/$', landpage_administration,
        name='landpage_administration'),
    url(r'^signup/pricing/plan/(?P<plan_id>\d+)/$',
        UserSignupWithSubscription.as_view(),
        name='user-pricing-signup'),
    url(r'^recive/webhooks/$',charges_succeeded,
        name='recive-webhooks'),
    url(r'^subscription/created/$',subscription_created,
        name='subscription-created'),
    url(r'^user/$', landpage_user, name='landpage_user'),
    url(r'^guest/$', landpage_guest, name='landpage_guest'),

    url(r'^login/$', LoginView.as_view(), name='user_login'),
    url(r'^users/create/$', create_user, name='create-user'),
    url(r'^logout/$', logout,
        {'next_page': settings.LOGOUT_REDIRECT_URL}, name="user_logout"),
    url(r'^users/settings/management/$', UserListView.as_view(),
        name='users-settings-management'),
    url(r'^user/delete/(?P<pk>\d+)$', UserDeleteView.as_view(), name='user_delete'),
    url(r'^user/edit/(?P<user_id>\d+)$', create_user, name='user_edit'),
    url(r'^password_change/$', change_password, name='change_password'),
    url(r'^users/(?P<pk>\d+)/tracker/$',
        TrackerDetailView.as_view(), name='user_tracker_details'),
    url(r'^users/tracker/$',
        TrackerView.as_view(), name='user_tracker'),
    url(r'^ajax/users/tracker/$',
        AjaxTrackerView.as_view(), name='ajax_user_tracker'),
    url(r'^ajax/users/status/$',
        UserStatusView.as_view(), name='ajax_user_status'),

    #Room Urls#
    url(r'^leaderboards/room/create$',
        views.RoomCreate.as_view(), name='leaderboards_rooms_create'),
    url(r'^leaderboards/rooms/update/(?P<pk>\d+)$',
        views.RoomUpdate.as_view(), name='leaderboards_rooms_update'),
    url(r'^leaderboards/rooms/delete/(?P<pk>\d+)$',
        RoomDelete.as_view(), name='room-delete'),
    url(r'^leaderboards/public/$',
        LeaderboardsPublic.as_view(), name='leaderboards_public'),

    url(r'^leaderboards/room/saveresult/$',
        SaveGameResult.as_view(), name='save_game_result'),

    url(r'^dashboard/rooms/$', views.RoomList.as_view(), name='dashboard_rooms'),
    url(r'^dashboard/rooms/create$', views.RoomCreateView.as_view(),
        name='dashboard_rooms_create'),
    url(r'^dashboard/rooms/update/(?P<room_id>\d+)/$',
        views.edit_room, name='dashboard_rooms_update'),
    url(r'^dashboard/gm/(?P<pk>\d+)$',
        views.RoomDetailView.as_view(), name='dashboard_gm_details'),
    url(r'^dashboard/live_view/(?P<pk>\d+)/$',
        views.RoomLiveViewmDetail.as_view(), name='dashboard_live_view_details'),

    # url(r'^dashboard/live_view/(?P<pk>\d+)/(?P<second>\d+)/$',
    #     views.NewRoomLiveViewmDetail.as_view(),
    #     name='dashboard_new_live_view_details'),

    url(r'^dashboard/rooms/clue/create/$',
        views.create_clue, name='room_clue_create'),
    url(r'^dashboard/rooms/clue/delete/$',
        views.delete_clue, name='clue_delete'),
    url(r'^dashboard/rooms/clue/edit/$', views.edit_clue, name='clue_edit'),

    url(r'^dashboard/rooms/image/create/$',
        views.create_image, name='room_create_image'),
    url(r'^dashboard/rooms/image/delete/$',
        views.delete_image, name='image_delete'),

    #Automation Urls#
    url(r'^dashboard/rooms/automation/$',
        automation_views.AutomationList.as_view(),
        name='dashboard_rooms_automation'),
    url(r'^automation/edit/(?P<pk>\d+)$',
        automation_views.AutomationUpdate.as_view(), name='automation_edit'),
    url(r'^automation/delete/(?P<pk>\d+)$',
        AutomationDelete.as_view(), name='automation_delete'),

    url(r'^dashboard/rooms/(?P<pk>\d+)/automation/$',
        RoomByAutomationDetailView.as_view(),
        name='dashboard_room_automations'),

    url(r'^dashboard/rooms/automation/create/(?P<pk>\d+)$',
        automation_views.AutomationCreateOrUpdate.as_view(),
        name='automation_new'),
    url(r'^dashboard/rooms/(?P<room_id>\d+)/automation/(?P<automation_id>\d+)$',
        automation_views.AutomationCreateOrUpdate.as_view(),
        name='edit_automations'),
    # Ajax Sound Urls
    url(r'^dashboard/rooms/(?P<room_id>\d+)/sound/create/$',
        SoundsCreate.as_view(), name='dashboard_rooms_sound_create'),
    url(r'^dashboard/rooms/sounds/(?P<pk>\d+)/delete/$',
        SoundsDelete.as_view(), name='dashboard_rooms_sound_delete'),

    # Ajax video Urls
    url(r'^dashboard/rooms/(?P<room_id>\d+)/video/create/$',
        VideosCreate.as_view(), name='dashboard_rooms_video_create'),
    url(r'^dashboard/rooms/videos/(?P<pk>\d+)/deletes/$',
        VideosDelete.as_view(), name='dashboard_rooms_video_delete'),

    # Ajax video Urls
    url(r'^dashboard/rooms/(?P<room_id>\d+)/puzzle/create/$',
        PuzzlesCreate.as_view(), name='dashboard_rooms_puzzle_create'),
    url(r'^dashboard/rooms/puzzles/(?P<pk>\d+)/deletes/$',
        PuzzlesDelete.as_view(), name='dashboard_rooms_puzzle_delete'),
    # url(r'^dashboard/rooms/puzzles/(?P<pk>\d+)/edit/$',
    #     PuzzlesUpdate.as_view(), name='dashboard_rooms_puzzle_edit'),
    url(r'^dashboard/rooms/(?P<room_id>\w+)/puzzles/(?P<puzzle_id>\w+)/edit/$',
        puzzles_update, name='dashboard_rooms_puzzle_edit'),
    #Business Urls#
    url(r'^settings/account-settings$',
        business_views.BusinessCreate.as_view(), name='account_settings'),

    #Billing Urls#
    url(r'^settings/update-billing/$',
        BillingUpdate.as_view(), name='update_billing'),

    # Leaderboard
    url(r'^leaderboards/top/$', LeadershipView.as_view(), name='leadership_top'),
    #url(r'^leaderboard/entries/$', LeaderboardListView.as_view(), name='leaderboard_entries'),
    url(r'^leaderboard/room/(?P<room_id>\d+)/entries/$', LeaderboardListView.as_view(), name='leaderboard_entries'),
    url(r'^leaderboard/entries/import/$', LeaderboardImportView.as_view(), name='leaderboard_import_entries'),
    url(r'^leaderboard/entries/export/$', LeaderboardEntriesExportView.as_view(), name='leaderboard_export_entries'),
    url(r'^leaderboard/entries/save/$', LeaderboardEntriesView.as_view({'post': 'save',}), name='leaderboard_save_entries'),
    url(r'^leaderboard/entry/create/$', LeaderboardEntryCreateView.as_view(), name='leaderboard_create_entry'),
    url(r'^leaderboard/entry/edit/(?P<pk>\d+)/$', LeaderboardEntryEditView.as_view(), name='leaderboard_edit_entry'),
    url(r'^leaderboard/entry/delete/$', LeaderboardEntryDeleteView.as_view(), name='leaderboard_delete_entry'),

    # Events
    url(r'^automation/events/create/$',
        automation_views.EventCreate.as_view(), name='waivers-events-create'),

    # Cache url
    url(r'^clear/cache/$', ClearCacheView.as_view(), name='clear-cache'),

    url(r'^dashboard/rooms/puzzle-print/(?P<pk>\d+)$',
        views.RoomPuzzleViewPrintView.as_view(), name='puzzle-print'),
    url(r'^dashboard/rooms/gm-stat/(?P<pk>\d+)$',
        views.RoomPuzzleGmStatView.as_view(), name='puzzle-gm-stat'),
    url(r'^dashboard/rooms/gm-players-status/(?P<pk>\d+)/$',
        views.RoomPuzzleGmPlayerStatusViewPrintView.as_view(),
        name='puzzle-gm-player-status'),

    # Normal user urls

    url(r'^landpage/$', landpage, name='main_dashboard'),

    url(r'^user/dashboard/rooms/$', views.UserRoomList.as_view(),
        name='dashboard_user_rooms'),

    # User Leadership
    url(r'^user/leaderboards/top/$',
        UserLeadershipView.as_view(), name='leadership_user_top'),
    url(r'^leaderboards/settings/$', LeaderBoardSettingsView.as_view(),
        name='leaderboard_settings'),

    url(r'^user/password_change/$', change_password, name='user_change_password'),

    url(r'^_403/$', TemplateView.as_view(template_name='403.html')),
    url(r'^_404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^_500/$', TemplateView.as_view(template_name='500.html')),

    url(r'^message/', include('messages_system.urls')),

    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name': 'users/password_reset_form.html'},
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'users/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'users/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'users/password_reset_complete.html'},
        name='password_reset_complete'),

    url(r'^api/', include('api.urls')),

    url(r'^user/pricing/plan/$',
        PricingView.as_view(), name='pricing_plan'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

    url(r'^users/plan/create$', PlanCreateView.as_view(),
        name='users_plan_create'),
    url(r'^users/plan/list$', PlanListView.as_view(),
        name='users_plan_list'),
    url(r'^users/room/summary$', AjaxUserRoomSummaryView.as_view(),
        name='users_room_summary'),
    # Django rest authentication Apis
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^tablet/dashboard/rooms/create$', views.TabletRoomCreateView.as_view(),
        name='tablet_dashboard_rooms_create'),
    url(r'^tablet/rooms/live-views/$',
        views.TabletRoomLiveListView.as_view(), name='tablet_live_rooms'),
    url(r'^tablet/rooms/lv/(?P<pk>\d+)/$',
        views.TabletRoomLiveView.as_view(), name='tablet_room_live_details'),
    url(r'^tablet/rooms/$',
        views.TabletRoomListView.as_view(), name='tablet_rooms'),
    url(r'^tablet/rooms/gm/(?P<pk>\d+)/$',
        views.TabletRoomDetailsView.as_view(), name='tablet_room_details'),

    url(r'^dashboard/tablet/rooms/update/(?P<room_id>\d+)/$',
        views.edit_tablet_room, name='dashboard_tablet_rooms_update'),

    url(r'^dashboard/guide/room$',
        views.GuideRoomListView.as_view(), name='dashboard_guide_rooms'),
    url(r'^guide/dashboard/rooms/create$', views.GuideRoomCreateView.as_view(),
        name='guide_dashboard_rooms_create'),
    url(r'^guide/rooms/(?P<pk>\d+)/update$', views.GuideRoomUpdate.as_view(),
        name='guide_dashboard_rooms_update'),
    url(r'^guide/rooms/(?P<pk>\d+)/delete$', GuideRoomDelete.as_view(),
        name='guide_dashboard_rooms_delete'),
    # url(r'^guide/rooms/(?P<room_id>\d+)/puzzle/add$',
    #     views.ScoringCreateAndUpdateView.as_view(),
    #     name='room_scoring_create'),
    url(r'^guide/rooms/(?P<room_id>\d+)/scrolling/add$',
        ScoringCreateAndUpdateView.as_view(), name='room_scoring_create'),
    url(r'^guide/rooms/(?P<room_id>\d+)/endinggame/add$',
        EndingGameCreateAndUpdateView.as_view(),
        name='room_ending_game_create'),
    url(r'^guide/rooms/(?P<puzzle_id>\d+)/puzzleclue/add$',
        PuzzleClueCreateAndUpdateView.as_view(),
        name='room_puzzle_clue_create'),
    url(r'^guide/rooms/(?P<puzzle_id>\d+)/puzzleclue/option$',
        PuzzleClueOptionsView.as_view(),
        name='room_puzzle_clue_options'),
    url(r'^$', TemplateView.as_view(template_name="landing/home.html"), name='erctrl_home'),
    url(r'^faq/$', TemplateView.as_view(template_name="landing/faq.html"), name='erctrl_faq'),
    url(r'^contact/$', ContactView.as_view(), name='erctrl_contact'),
    url(r'^thanks/$', TemplateView.as_view(template_name="emails/thanks.html"), name='erctrl_thanks'),
    # url(r'^contact/$', ContactView.as_view(template_name="landing/contact.html"), name='erctrl_contact'),

    url(r'^dashboard/rooms/ph-hue/$',
        views.TestPhilipsHueSetting.as_view(),
        name='dashboard_rooms_ph_hue'),
    url(r'^dashboard/rooms/(?P<room_id>\d+)/ph-settings/$',
        views.PhilipsHueRoomSetting.as_view(),
        name='dashboard_rooms_ph_settings'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
