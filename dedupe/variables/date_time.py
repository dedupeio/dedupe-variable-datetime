from __future__ import print_function

from dedupe.variables.string import affineGap
from dedupe.variables.base import FieldType, DerivedType
from dedupe import predicates
from datetime_distance import DateTimeComparator
import dedupe.variables.datetime_predicates as dtp
import numpy as np


class DateTimeType(FieldType):

    type = "DateTime"
    _predicate_functions = [predicates.wholeFieldPredicate,
                            dtp.yearPredicate,
                            dtp.monthPredicate,
                            dtp.dayPredicate,
                            dtp.hourPredicate,
                            dtp.exclusiveMonthPredicate,
                            dtp.exclusiveDayPredicate,
                            dtp.threeDayPredicate,
                            dtp.exclusiveHourPredicate]

    def __len__(self):

        return self.expanded_size

    def __init__(self, definition):
        """
        Initialize a field for comparing datetime types, including timestamps,
        dates, months, and years.

        Custom field definitions for this class include:
            * `fuzzy` (bool): Use fuzzy parsing for datetime fields (default True)
            * `dayfirst` (bool): Ambiguous dates should be parsed as dd/mm/yy (default False)
            * `yearfirst` (bool): Ambiguous dates should be parsed as yy/mm/dd (default False)

        If both `dayfirst` and `yearfirst` are set to True, `dayfirst` will take precedence.
        See https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse
        for more information about python-dateutil's parser settings.
        """

        super(DateTimeType, self).__init__(definition)

        # Parser settings
        self.fuzzy = definition.get('fuzzy', True)
        self.dayfirst = definition.get('dayfirst', False)
        self.yearfirst = definition.get('yearfirst', False)

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
        String comparison function (backup in case of bad parses).
        """
        return affineGap(field_1, field_2)

    def comparator(self, field_1, field_2):
        """
        The comparator function for this class.

        Compares two strings and returns a distance vector.
        """
        c = DateTimeComparator(fuzzy=self.fuzzy,
                               dayfirst=self.dayfirst,
                               yearfirst=self.yearfirst)

        # Initialize the output vector with zeros
        distances = np.zeros(self.expanded_size)

        # In case of missing fields, return Is Missing bool + all zeros
        if not (field_1 and field_2):
            return distances

        distances[0] = 1

        # Cast inputs to strings, in case they're DateTime objects
        field_1, field_2 = str(field_1), str(field_2)

        try:
            comparisons = c(field_1, field_2)
        except ValueError:
            # Bad parse - use string comparison instead
            distances[-1] = self._compare_as_strings(field_1, field_2)
            # We don't have to update any dummy vars, because string is last
            return distances

        # Copy over all comparisons, skipping the last index (string var)
        distances[1:len(comparisons)+1] = comparisons

        return distances
