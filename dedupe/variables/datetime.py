from __future__ import print_function

from dedupe.variables.string import affineGap
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

        # Parser settings
        # (c.f. https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse)
        try:
            # Use fuzzy parsing
            self.fuzzy = definition['fuzzy']
        except KeyError:
            self.fuzzy = True

        try:
             # Ambiguous dates should be parsed as dd/mm/yy (default: mm/dd/yy)
            self.dayfirst = definition['dayfirst']
        except KeyError:
            self.dayfirst = False

        try:
            # Ambiguous dates should be parsed as yy/mm/dd
            self.yearfirst = definition['yearfirst']
        except KeyError:
            self.yearfirst = False

        # Define the expected fields in the output vector
        self.variables = ('seconds', 'days', 'months', 'years', 'full string')
        fields = self._get_fields(definition['field'])

        # Format for output vector: Not Missing + Dummies + Fields
        self.expanded_size = (1 + (len(self.variables) - 1) +
                              len(self.variables))

        self.higher_vars = [DerivedType({'name': variable,
                                         'type': field_type})
                            for variable, field_type in fields]

    def _get_fields(self, field):
        """
        Returns the format for the output vector.
        """
        fields = [('{}: Not Missing'.format(field), 'Dummy')]

        fields += [(var, 'Dummy') for var in self.variables[:-1]]

        fields += [(var, 'Derived') for var in self.variables]

        return fields

    def _compare_as_strings(self, field_1, field_2):
        """
        String comparison function (backup in case of bad parse).
        """
        if (field_1 and field_1 != '') and (field_2 and field_2 != ''):
            return affineGap(field_1, field_2)
        else:
            return 0

    def comparator(self, field_1, field_2):

        c = DateTimeComparator(fuzzy=self.fuzzy,
                               dayfirst=self.dayfirst,
                               yearfirst=self.yearfirst)

        # Initialize the output vector with zeros
        distances = np.zeros(self.expanded_size)

        # In case of missing fields, return Is Missing bool + all zeros
        if not (field_1 and field_2):
            return distances

        distances[0] = 1

        try:
            comparisons = c(field_1, field_2)
        except ValueError:
            # Bad parse - use string comparison instead
            distances[-1] = self._compare_as_strings(field_1, field_2)
            # We don't have to update any dummy vars, because string is last
            return distances

        if not np.any(comparisons):  # If all distances are 0
            # Exact match
            return distances
        else:
            # Switch on the right dummy variable
            for i, val in enumerate(comparisons):
                if val:
                    distances[i+1] = 1
                    break

            # Insert the comparison vector after the dummy variables
            i = len(comparisons) + 1

            # Copy over all comparisons, skipping the last index (string var)
            distances[i:i+i-1] = comparisons

            return distances
