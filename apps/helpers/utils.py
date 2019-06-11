import datetime
import calendar
import pytz
from django.utils import timezone


class CustomFormatter(object):

    def get_current_week_days(is_string_format=False):
        today = datetime.datetime.now().date()
        for i in range(0 - today.isoweekday(), 7 - today.isoweekday()):
            if is_string_format:
                new_date_format = today + datetime.timedelta(days=i)
                yield new_date_format.strftime("%Y-%m-%d")
            else:
                yield today + datetime.timedelta(days=i)

    def get_current_month_of_weeks(is_string_format=False):
        today = datetime.datetime.now().date()
        first_day = today.replace(day=1)
        last_day = today.replace(
            day=calendar.monthrange(today.year, today.month)[1])
        number_of_week = (last_day.day - 1) // 7 + 1

        for i in range(number_of_week):
            w_start_date = first_day + datetime.timedelta(days=i * 7)
            w_end_date = w_start_date + datetime.timedelta(days=6)
            if w_end_date > last_day:
                w_end_date = last_day
            if is_string_format:
                yield w_start_date.strftime("%Y-%m-%d") + " - " + w_end_date.strftime("%Y-%m-%d")
            else:
                yield (w_start_date, w_end_date)

    def get_months_range_of_year(n=12, ending=None, is_string_format=False):
        """Return a list of tuples of the first/last day of the month
           for the last N months
        """
        current_year = datetime.datetime.now().year
        number_of_days_in_months = [calendar.monthrange(year, month)[1] for year in [current_year] for month in range(1,13)]
        for index, nodim in enumerate(number_of_days_in_months):
            start_date = datetime.date(current_year, index + 1, 1)
            end_date = datetime.date(current_year, index + 1, nodim)
            if is_string_format:
                yield start_date.strftime("%Y-%m-%d") + " - " + end_date.strftime("%Y-%m-%d")
            else:
                yield (start_date, end_date)

    def get_date_between_two_dates(start=12, end=None, is_string_format=False):
        """Return a list of dates between two given dates
        """
        delta = end - start

        for i in range(delta.days + 1):
            new_date = start + datetime.timedelta(days=i)
            if is_string_format:
                yield new_date.strftime("%Y-%m-%d")
            else:
                yield new_date


def make_naive(value):
    return timezone.make_naive(
        value,
        timezone.pytz.timezone(timezone.get_current_timezone_name()))


def make_aware(value):
    try:
        return timezone.make_aware(
            value,
            timezone.pytz.timezone(timezone.get_current_timezone_name()))

    except (pytz.NonExistentTimeError, pytz.AmbiguousTimeError):
        tz = timezone.pytz.timezone(timezone.get_current_timezone_name())
        return tz.localize(value, is_dst=False)
