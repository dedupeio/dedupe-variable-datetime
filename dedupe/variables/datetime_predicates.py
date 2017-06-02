from datetime_distance import DateTimeComparator


def parse_field(field):
    """
    Standardized helper function to parse a datetime field.
    """
    comp = DateTimeComparator()
    dt = comp.parse_resolution(field)[0]
    return dt


def yearPredicate(field):
    """
    Hash a field based on year.
    """
    dt = parse_field(field)
    return (dt.year,)


def monthPredicate(field):
    """
    Hash a field based on year + month.
    """
    dt = parse_field(field)
    return (dt.year, dt.month)


def exclusiveMonthPredicate(field):
    """
    Hash a field based on calendar month (e.x. 'June').
    """
    dt = parse_field(field)
    return (dt.month,)


def dayPredicate(field):
    """
    Hash a field based on year + month + day.
    """
    dt = parse_field(field)
    return (dt.year, dt.month, dt.day)


def exclusiveDayPredicate(field):
    """
    Hash a field based on calendar day (e.x. '23rd').
    """
    dt = parse_field(field)
    return (dt.day,)


def hourPredicate(field):
    """
    Hash a field based on year + month + day + nearest hour.
    """
    dt = parse_field(field)
    return (dt.year, dt.month, dt.day, dt.hour)


def exclusiveHourPredicate(field):
    """
    Hash a field based on nearest hour (e.x. '5:00')
    """
    dt = parse_field(field)
    return (dt.hour,)
