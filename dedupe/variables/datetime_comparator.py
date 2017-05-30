from __future__ import print_function

from dedupe.variables.base import FieldType, DerivedType
from dedupe import predicates
from datetime_distance import DateTimeComparator
import numpy as np


class DateTimeType(FieldType):

    type = "DateTime"
    _predicate_functions = [predicates.wholeFieldPredicate]

    def __len__(self):

        return self.expanded_size

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

        self.variables = ('seconds', 'days', 'months', 'years')
        fields = self._get_fields(definition['field'])

        # not missing + indicators + fields
        self.expanded_size = (1 + (len(self.variables) - 1) +
                              len(self.variables))

        self.higher_vars = [DerivedType({'name': variable,
                                         'type': field_type})
                            for variable, field_type in fields]

    def _get_fields(self, field):

        fields = [('{}: Not Missing'.format(field), 'Dummy')]

        fields += [(var, 'Dummy') for var in self.variables[:-1]]

        fields += [(var, 'Derived') for var in self.variables]

        return fields

    def comparator(self, field_1, field_2):

        c = DateTimeComparator(fuzzy=self.fuzzy,
                               dayfirst=self.dayfirst,
                               yearfirst=self.yearfirst)

        distances = np.empty(self.expanded_size)

        if not (field_1 and field_2):
            return distances

        distances[0] = 1

        comparisons = c(field_1, field_2)

        if not np.any(comparisons):
            # Exact match
            return distances
        else:
            # Switch on the right dummy variable
            for i, val in enumerate(comparisons):
                if val and i < (len(comparisons) - 1):
                    distances[i+1] = 1
                    break

            distances[len(comparisons):] = comparisons

        return distances
