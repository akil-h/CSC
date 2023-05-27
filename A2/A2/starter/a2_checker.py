"""A simple checker for types of functions in mm_functions.py."""

from typing import Any, Dict, Union
import pytest
import checker_generic
import carbon_emissions as ce

FILENAME = 'carbon_emissions.py'
PYTA_CONFIG = 'a2_pythonta.json'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'START_YEAR': 1799,
    'END_YEAR': 2017,
    'EMISSION_FILENAME': 'co2_emissions_per_person.csv',
    'POP_FILENAME': 'populations.csv',
    'G7_COUNTRIES': ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom',
                     'United States']
}

NUMBER_TYPE = (float, int)


class TestChecker:
    """Sanity checker for assignment functions."""

    def test_convert_population(self) -> None:
        """Function convert_population."""

        self._check(ce.convert_population, ['4320'], NUMBER_TYPE)

    def test_get_year_index(self) -> None:
        """Function get_year_index"""

        self._check(ce.get_year_index, [1799], int)

    def test_get_country_row(self) -> None:
        """Function get_country_row"""

        self._check(ce.get_country_row,
                    [ce.SAMPLE_POPULATION_DATA, 'Canada'], list)

    def test_country_with_largest_emissions_by_year(self) -> None:
        """Function country_with_largest_emissions_by_year"""

        self._check(ce.country_with_largest_emissions_by_year,
                    [ce.SAMPLE_EMISSIONS_DATA, 1800], str)

    def test_emissions_by_country_by_year(self) -> None:
        """Function emissions_by_country_by_year"""

        self._check(ce.emissions_by_country_by_year,
                    [ce.SAMPLE_EMISSIONS_DATA,
                     ce.SAMPLE_POPULATION_DATA,
                     'Canada', 1799],
                    NUMBER_TYPE)

    def test_total_emissions_by_countries(self) -> None:
        """Function total_emissions_by_countries"""

        self._check(ce.total_emissions_by_countries,
                    [['Canada', 'Finland'],
                     ce.SAMPLE_POPULATION_DATA,
                     ce.SAMPLE_EMISSIONS_DATA, 1799
                     ], NUMBER_TYPE)

    def test_country_average_over_range(self) -> None:
        """Function country_average_over_range"""

        self._check(ce.country_average_over_range,
                    [ce.SAMPLE_EMISSIONS_DATA, 1799, 1800, 'Canada'], NUMBER_TYPE)

    def test_peak_year_by_country(self) -> None:
        """Function peak_year_by_country"""

        self._check(ce.peak_year_by_country,
                    [ce.SAMPLE_EMISSIONS_DATA, 'Canada'], int)

    def test_create_total_emissions_table(self) -> None:
        """Function create_total_emissions_table"""

        checker_generic.returns_list_of_Ts(
            ce.create_total_emissions_table,
            [ce.SAMPLE_EMISSIONS_DATA, ce.SAMPLE_POPULATION_DATA],
            list)

    def test_update_country_year_data(self) -> None:
        """Function update_country_year_data"""

        self._check(ce.update_country_year_data,
                    [[['France', -1.0, -1.0, -1.0, -1.0] + [-1.0] * 215],
                     'France', 1799, 0.05], NUMBER_TYPE)

    def test_read_data(self) -> None:
        """Function read_data"""

        checker_generic.returns_list_of_Ts(ce.read_data,
                                           ['co2_emissions_per_person.csv'],
                                           list)

    def test_prepare_data(self) -> None:
        """Function prepare_data"""

        checker_generic.returns_list_of_Ts(ce.read_data,
                                           ['co2_emissions_per_person.csv',
                                            True],
                                           list)

    def test_clean_population_data(self) -> None:
        """Function clean_population_data"""

        self._check(ce.clean_population_data,
                    [[['France', '29M', '29.1M', '29.2M', '29.3m'],
                      ['Mauritius', '59k', '60.7k', '62.4k', '64.2k']]],
                    type(None))

    def test_clean_emission_data(self) -> None:
        """Function clean_emission_data"""

        self._check(ce.clean_emission_data, [
            [['Canada', '0.00733', '0.00716', '0.00698', '0.00681'] + [''] * 215,
             ['Finland'] + [''] * 3 + ['0.00341'] + [''] * 215,
             ['Poland', '0.0452', ' 0.0489', '0.0494', '0.0502'] + [''] * 215]],
                    type(None))

    def test_check_constants(self) -> None:
        """Values of constants."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, ce)
        print('  check complete')

    def _check(self, func: callable, args: list, ret_type: Union[type, tuple]) -> None:
        """Check that func called with arguments args returns a value of type
        ret_type. Display the progress and the result of the check.

        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker_generic.type_check_simple(func, args, ret_type)
        assert result[0] is True, result[1]
        print('  check complete')

    def _check_constants(self, name2value: Dict[str, object], mod: Any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.
        """

        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = 'The value of constant {} should be {} but is {}.'.format(
                name, expected, actual)
            assert expected == actual, msg


print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style with PythonTA '.center(TARGET_LEN, SEP))
checker_generic.run_pyta(FILENAME, PYTA_CONFIG)
print(' End checking coding style with PythonTA '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
pytest.main(['--show-capture', 'no', '--disable-warnings', '--tb=short',
             'a2_checker.py'])
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style with Python TA')
print('  - checking type contract\n')
