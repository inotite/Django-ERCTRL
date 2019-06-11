# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from djstripe.utils import subscriber_has_active_subscription
from djstripe.models import Customer, Invoice
from helpers.utils import CustomFormatter

ROLE_TYPE_CHOICES = (
    ('0', 'admin'),
    ('1', 'user'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_4_digits = models.CharField(null=True, max_length=4, blank=True)
    stripe_id = models.CharField(null=True, max_length=255, blank=True)
    subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = (user,)

    @property
    def get_role(self):
        try:
            return self.roles.first().role
        except (AttributeError, IndexError):
            return None

    def is_administrator(self):
        if self.get_role == 'admin':
            return True
        return False

    def is_normal_user(self):
        if self.get_role == 'user':
            return True
        return False

    def get_base_portal(self):
        if self.user.is_superuser or self.user.profile.is_administrator():
            base_portal = "portals/base_administration_portal.html"
        else:
            base_portal = "portals/base_user_portal.html"
        return base_portal

    def get_user_administrators(self):
        """Rerutn admin of user."""
        for emp in self.user_employees.all():
            yield emp.parent.user

    def get_administrator_users(self):
        """Rerutn admin of users."""
        for emp in self.user_parent_employee.all():
            yield emp.employee.user

    def get_user_child_administrators(self, start_date=None, end_date=None):
        """Rerutn child administrators of current login user."""
        administrators = self.user_parent_employee.filter(
            employee__roles__role='admin')
        if start_date:
            administrators = administrators.filter(
                employee__user__date_joined__gte=start_date)
        if end_date:
            administrators = administrators.filter(
                employee__user__date_joined__lt=end_date)
        return administrators

    def get_user_child_users(self, start_date=None, end_date=None):
        """Rerutn child users of current login user."""
        users = self.user_parent_employee.filter(
            employee__roles__role='user')
        if start_date:
            users = users.filter(
                employee__user__date_joined__gte=start_date)
        if end_date:
            users = users.filter(
                employee__user__date_joined__lt=end_date)
        return users

    def get_administrators_count_list(self):
        """Rerutn child administrators count according to selected user object."""
        week_days = CustomFormatter.get_current_week_days()
        for week_day in week_days:
            next_date = week_day + datetime.timedelta(1)
            administrators = self.get_user_child_administrators(
                start_date=week_day, end_date=next_date)
            yield administrators.count()

    def get_users_count_list(self):
        """Rerutn child users count according to selected user object."""
        week_days = CustomFormatter.get_current_week_days()
        for week_day in week_days:
            next_date = week_day + datetime.timedelta(1)
            users = self.get_user_child_users(
                start_date=week_day, end_date=next_date)
            yield users.count()

    def get_administrators_count_by_month_list(self):
        """Rerutn child administrators count according to selected user object."""
        month_weeks = CustomFormatter.get_current_month_of_weeks()
        for month_week in month_weeks:
            next_date = month_week[1] + datetime.timedelta(1)
            administrators = self.get_user_child_administrators(
                start_date=month_week[0], end_date=next_date)
            yield administrators.count()

    def get_users_count_by_month_list(self):
        """Rerutn child users count according to selected user object."""
        month_weeks = CustomFormatter.get_current_month_of_weeks()
        for month_week in month_weeks:
            next_date = month_week[1] + datetime.timedelta(1)
            users = self.get_user_child_users(
                start_date=month_week[0], end_date=next_date)
            yield users.count()

    def get_administrators_count_by_year_list(self):
        """Rerutn child administrators count according to selected user object."""
        year_months = CustomFormatter.get_months_range_of_year()
        for year_month in year_months:
            next_date = year_month[1] + datetime.timedelta(1)
            administrators = self.get_user_child_administrators(
                start_date=year_month[0], end_date=next_date)
            yield administrators.count()

    def get_users_count_by_year_list(self):
        """Rerutn child users count according to selected user object."""
        year_months = CustomFormatter.get_months_range_of_year()
        for year_month in year_months:
            next_date = year_month[1] + datetime.timedelta(1)
            users = self.get_user_child_users(
                start_date=year_month[0], end_date=next_date)
            yield users.count()

    def get_graph_source_data(self):
        """Return week source data of graph for user."""
        week_days = CustomFormatter.get_current_week_days(
            is_string_format=True)
        tracker_list = [['timestamps'], ['admin'], ['user']]
        tracker_list[0].extend(list(week_days))
        tracker_list[1].extend(list(self.get_administrators_count_list()))
        tracker_list[2].extend(list(self.get_users_count_list()))
        return tracker_list

    def get_month_graph_source_data(self):
        """Return month source data of graph for user."""
        month_weeks = CustomFormatter.get_current_month_of_weeks(
            is_string_format=True)
        tracker_list = [['timestamps'], ['admin'], ['user']]
        tracker_list[0].extend(list(month_weeks))
        tracker_list[1].extend(list(self.get_administrators_count_by_month_list()))
        tracker_list[2].extend(list(self.get_users_count_by_month_list()))
        return tracker_list

    def get_year_graph_source_data(self):
        """Return month source data of graph for user."""
        year_months = CustomFormatter.get_months_range_of_year(
            is_string_format=True)
        tracker_list = [['timestamps'], ['admin'], ['user']]
        tracker_list[0].extend(list(year_months))
        tracker_list[1].extend(list(self.get_administrators_count_by_year_list()))
        tracker_list[2].extend(list(self.get_users_count_by_year_list()))
        return tracker_list

    def get_administrators_count_by_range_list(self, start_date=None, end_date=None):
        """Rerutn child administrators count according to selected user object."""
        date_range = CustomFormatter.get_date_between_two_dates(
            start=start_date, end=end_date)
        for dr in date_range:
            next_date = dr + datetime.timedelta(1)
            administrators = self.get_user_child_administrators(
                start_date=dr, end_date=next_date)
            yield administrators.count()

    def get_users_count_by_range_list(self, start_date=None, end_date=None):
        """Rerutn child users count according to selected user object."""
        date_range = CustomFormatter.get_date_between_two_dates(
            start=start_date, end=end_date)
        for dr in date_range:
            next_date = dr + datetime.timedelta(1)
            users = self.get_user_child_users(
                start_date=dr, end_date=next_date)
            yield users.count()

    def get_range_graph_source_data(self, start_date=None, end_date=None):
        """Return range source data of graph for user."""
        if start_date:
            start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y')
        if end_date:
            end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y')
        date_range = CustomFormatter.get_date_between_two_dates(
            start=start_date, end=end_date, is_string_format=True)
        tracker_list = [['timestamps'], ['admin'], ['user']]
        tracker_list[0].extend(list(date_range))
        tracker_list[1].extend(list(
            self.get_administrators_count_by_range_list(start_date, end_date)))
        tracker_list[2].extend(
            list(self.get_users_count_by_range_list(start_date, end_date)))
        return tracker_list

    @cached_property
    def has_active_subscription(self):
        """Checks if a user has an active subscription."""
        return subscriber_has_active_subscription(self.user)

    def get_total_pay(self):

        try:
            cust_id = Customer.objects.get(stripe_id=self.stripe_id).id
            paid_invoices = float(sum(Invoice.objects.filter(
                customer_id=cust_id, paid=True).values_list('total', flat=True)))
            return paid_invoices
        except AttributeError:
            return 0.0
