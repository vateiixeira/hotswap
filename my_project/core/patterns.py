import re

_time = '(2[0-3]|[0-1]?[0-9]):[0-5]?[0-9](:[0-5]?[0-9])?'
_time_range = '{time}-{time}'.format(time=_time)


PATTERN_DATE = re.compile(r'^\d{4}-((0?[1-9])|(1[0-2]))-((0?[1-9])|[1-2][0-9]|3[0-1])$')
PATTERN_TIME = re.compile(r'^{}$'.format(_time))
PATTERN_TIME_RANGES = re.compile(r'^{time_range}(,{time_range})*$'.format(time_range=_time_range))
PATTERN_ID_LIST = re.compile(r'^[0-9]+(,[0-9]+)*$')
PATTERN_SLUG_LIST = re.compile(r'^[-\w]+(,[-\w]+)*$')

PATTERN_EVENT_MONTH = re.compile(r'^\d{4}-((0?[1-9])|(1[0-2]))$')