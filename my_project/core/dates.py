# coding: utf-8
import calendar
from datetime import datetime, timedelta, date, time
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from django.utils.timezone import get_current_timezone, make_aware, is_naive, now
from pytz import NonExistentTimeError


TIMEZONE_CHOICES = (
    ('America/Asuncion', 'America/Asuncion'),
    ('America/Bahia', 'America/Bahia'),
    ('America/Cuiaba', 'America/Cuiaba'),
    ('America/Campo_Grande', 'America/Campo_Grande'),
    ('America/Sao_Paulo', 'America/Sao_Paulo'),
    ('Asia/Dubai', 'Asia/Dubai'),
    ('Europe/London', 'Europe/London'),
)


def datetime_to_default():
    return now() + timedelta(days=36500)


def parse_date(dt, input_format='%d/%m/%Y'):
    if not dt:
        return None

    timezone = get_current_timezone()

    if '-' in dt and '-' not in input_format:
        input_format = '%Y-%m-%d'

    try:
        dt = datetime.strptime(dt, input_format)
        return normalized(timezone.localize(dt))
    except NonExistentTimeError:
        return normalized(timezone.localize(dt + timedelta(hours=1)))
    except Exception:
        pass

    return None


def parse_aware_date(dt_str):
    if not dt_str:
        return None

    try:
        dt = parse(dt_str)
        if is_naive(dt):
            dt = make_aware(dt)
        return dt
    except ValueError:
        return None


def normalized(dt, tz=None):
    if type(dt) == date or is_naive(dt):
        dt = localized(dt, tz=tz)
    if not tz:
        tz = get_current_timezone()
    return tz.normalize(dt)


def localized(dt, tz=None):
    if type(dt) == date:
        dt = datetime.combine(dt, time())
    if not tz:
        tz = get_current_timezone()
    return tz.localize(dt)


def iso_strf(value):
    value = value.isoformat()
    if value.endswith('+00:00'):
        value = value[:-6] + 'Z'
    return value


def add_months(sourcedate, months):
    return sourcedate + relativedelta(months=months)


def replace_day(dt, day):
    try:
        return dt.replace(day=day)
    except ValueError:
        last_day_of_month = calendar.monthrange(dt.year, dt.month)[1]
        return dt.replace(day=last_day_of_month)

def week_of_month(date):
    """Retorna o numero da semana"""

    #Calendar object. 6 = Start on Sunday, 0 = Start on Monday
    cal_object = calendar.Calendar(0)
    month_calendar_dates = cal_object.itermonthdates(date.year,date.month)

    day_of_week = 1
    week_number = 1

    for day in month_calendar_dates:
        #add a week and reset day of week
        if day_of_week > 7:
            week_number += 1
            day_of_week = 1

        if date == day:
            break
        else:
            day_of_week += 1

    return week_number