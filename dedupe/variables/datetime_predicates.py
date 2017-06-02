from datetime_distance import DateTimeComparator


def parse_field(field):
    """
    Standardized helper function to parse a datetime field.
    """
    comp = DateTimeComparator()
    dt = comp.parse_resolution(field)[0]
    return dt


def make_predicate(attrs):
    """
    Standardized helper function to handle missing resolutions and
    return predicates.
    """
    output = tuple(attrs)
    # Check that all resolutions are present in the string
    if all(output):
        return output
    else:
        return ()


def yearPredicate(field):
    """
    Hash a field based on year.
    """
    dt = parse_field(field)
    # Parser will return a NoneType in case of a bad parse
    if dt:
        return make_predicate([dt.year])
    else:
        return ()


def monthPredicate(field):
    """
    Hash a field based on year + month.
    """
    dt = parse_field(field)
    if dt:
        return make_predicate([dt.year, dt.month])
    else:
        return ()


def exclusiveMonthPredicate(field):
    """
    Hash a field based on calendar month (e.x. 'June').
    """
    dt = parse_field(field)
    if dt:
        return make_predicate([dt.month])
    else:
        return ()


def dayPredicate(field):
    """
    Hash a field based on year + month + day.
    """
    dt = parse_field(field)
    if dt:
        return make_predicate([dt.year, dt.month, dt.day])
    else:
        return ()


def exclusiveDayPredicate(field):
    """
    Hash a field based on calendar day (e.x. '23rd').
    """
    dt = parse_field(field)
    if dt:
        return make_predicate([dt.day])
    else:
        return ()


def hourPredicate(field):
    """
    Hash a field based on year + month + day + nearest hour.
    """
    dt = parse_field(field)
    if dt:
        return make_predicate([dt.year, dt.month, dt.day, dt.hour])
    else:
        return ()


def exclusiveHourPredicate(field):
    """
    Hash a field based on nearest hour (e.x. '5:00')
    """
    dt = parse_field(field)
    if dt:
        return make_predicate([dt.hour])
    else:
        return ()
