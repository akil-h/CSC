"""A simple checker for types of functions in mm_functions.py."""

from typing import Any, Dict, Union
import pytest
import checker_generic
import a3

FILENAME = 'a3.py'
PYTA_CONFIG = 'a3_pythonta.json'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'ID': 'id',
    'HT_KEY': 'hypertension',
    'TOTAL': 'total',
    'LOW_INCOME': 'low_income',
    'HT_20_44': 0,
    'NBH_20_44': 1,
    'HT_45_64': 2,
    'NBH_45_64': 3,
    'HT_65_UP': 4,
    'NBH_65_UP': 5,
    'ID_COL': 0,
    'NBH_NAME_COL': 1,
    'POP_COL': 2,
    'LI_POP_COL': 3
}

SAMPLE_DATA = {
    "West Humber-Clairville": {
        "id": 1,
        "hypertension": [703, 13291, 3741, 9663, 3959, 5176],
        "total": 33230,
        "low_income": 5950,
    },
    "Mount Olive-Silverstone-Jamestown": {
        "id": 2,
        "hypertension": [789, 12906, 3578, 8815, 2927, 3902],
        "total": 32940,
        "low_income": 9690,
    },
    "Thistletown-Beaumond Heights": {
        "id": 3,
        "hypertension": [220, 3631, 1047, 2829, 1349, 1767],
        "total": 10365,
        "low_income": 2005,
    },
    "Rexdale-Kipling": {
        "id": 4,
        "hypertension": [201, 3669, 1134, 3229, 1393, 1854],
        "total": 10540,
        "low_income": 2140,
    },
    "Elms-Old Rexdale": {
        "id": 5,
        "hypertension": [176, 3353, 1040, 2842, 948, 1322],
        "total": 9460,
        "low_income": 2315,
    },
}



class TestChecker:
    """Sanity checker for assignment functions."""

    def test_get_hypertension_data(self) -> None:
        """Function get_hypertension_data"""
        with open('hypertension_data_small.csv') as f:
            d = {}
            assert a3.get_hypertension_data(d, f) is None, \
                "get_hypertension_data should return None"
            assert d != {}, \
                "The dictionary provided to get_hypertension_data " \
                "should have new elements."

    def test_get_low_income_data(self) -> None:
        """Function get_low_income_data"""
        with open('low_income_small.csv') as f:
            d = {}
            assert a3.get_low_income_data(d, f) is None, \
                "get_low_income_data should return None"
            assert d != {}, \
                "The dictionary provided to get_low_income_data " \
                "should have new elements."

    def test_get_bigger_neighbourhood(self) -> None:
        """Function get_bigger_neighbourhood"""
        self._check(a3.get_bigger_neighbourhood,
                    [SAMPLE_DATA,
                     'Mount Olive-Silverstone-Jamestown',
                     'Rexdale-Kipling'],
                    str)

    def test_get_high_hypertension_rate(self) -> None:
        """Function get_high_hypertension_rate"""
        results = checker_generic.returns_list_of_Ts(
            a3.get_high_hypertension_rate, [SAMPLE_DATA, 0.24], tuple)
        assert results[0], results[1]

    def test_get_ht_to_low_income_ratios(self) -> None:
        """Function get_ht_to_low_income_ratios"""
        self._check(a3.get_ht_to_low_income_ratios,
                    [SAMPLE_DATA], dict)

    def test_calculate_ht_rates_by_age_group(self) -> None:
        """Function calculate_ht_rates_by_age_group"""
        results = checker_generic.returns_tuple_of \
            (a3.calculate_ht_rates_by_age_group,
                                                   [SAMPLE_DATA,
                                                    'Elms-Old Rexdale'],
                                                   (float, float, float))
        assert results[0], results[1]

    def test_get_stats_summary(self) -> None:
        """Function get_stats_summary"""
        self._check(a3.get_stats_summary, [SAMPLE_DATA], float)

    def test_order_by_ht_rate(self) -> None:
        """Function order_by_ht_rate"""
        results = checker_generic.returns_list_of_Ts(a3.order_by_ht_rate,
                                                     [SAMPLE_DATA], str)
        assert results[0], results[1]

    def test_check_constants(self) -> None:
        """Values of constants."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, a3)
        print('  check complete')

    def test_test_a3_has_test_cases(self) -> None:
        """test_a3.py has test cases beyond the provided 'test_first_bigger'
        """
        import test_a3
        test_cases = [item for item in dir(test_a3)
                      if item.startswith('test_')
                      and item != 'test_first_bigger']
        assert test_cases, \
            "No new test cases were found in test_a3.py: " \
            "make sure all of your test case names start with " \
            "'test_')"

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
             'a3_checker.py'])
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style with Python TA')
print('  - checking type contract\n')
