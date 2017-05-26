from __future__ import print_function

from dedupe.variables.base import FieldType
from dedupe import predicates
from datetime_distance import DateTimeComparator


class DateTimeType(FieldType):

    type = "DateTime"
    _predicate_functions = [predicates.wholeFieldPredicate]

    def __init__(self, definition):

        super(DateTimeType, self).__init__(definition)

        try:
            self.fuzzy = definition['fuzzy']
        except KeyError:
            self.fuzzy = True

        try:
            self.dayfirst = definition['dayfirst']
        except KeyError:
            self.dayfirst = False

        try:
            self.yearfirst = definition['yearfirst']
        except KeyError:
            self.yearfirst = False

        self.comparator = DateTimeComparator(fuzzy=self.fuzzy,
                                             dayfirst=self.dayfirst,
                                             yearfirst=self.yearfirst)
