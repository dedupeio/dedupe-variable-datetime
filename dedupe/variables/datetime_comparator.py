from __future__ import print_function

from dedupe.variables.base import FieldType
from dedupe import predicates
from datetime_distance import DateTimeComparator


class DateTimeType(FieldType):

    type = "DateTime"
    _predicate_functions = [predicates.wholeFieldPredicate]

    def __init__(self):

        self.comparator = DateTimeComparator()
