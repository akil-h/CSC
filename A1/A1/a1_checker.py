"""A simple checker for types of functions in mm_functions.py."""

from typing import Any, Dict
import pytest
import checker_generic
import mm_functions as mm

FILENAME = 'mm_functions.py'
PYTA_CONFIG = 'a1_pythonta.json'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {'CONSONANT_POINTS': 1,
             'VOWEL_COST': 1,
             'CONSONANT_BONUS': 2,
             'PLAYER_ONE': 'Player One',
             'PLAYER_TWO': 'Player Two',
             'CONSONANT': 'C',
             'VOWEL': 'V',
             'SOLVE': 'S',
             'QUIT': 'Q',
             'HIDDEN': '^',
             'HUMAN': 'P1',
             'HUMAN_HUMAN': 'PVP',
             'HUMAN_COMPUTER': 'PVE',
             'EASY': 'E',
             'HARD': 'H',
             'ALL_CONSONANTS': 'bcdfghjklmnpqrstvwxyz',
             'ALL_VOWELS': 'aeiou',
             'PRIORITY_CONSONANTS': 'tnrslhdcmpfygbwvkqxjz'
             }


class TestChecker:
    """Sanity checker for assignment functions."""
    
    def test_is_win(self) -> None:
        """Function is_win."""
        
        self._check(mm.is_win, ['same','same'], bool)

    def test_is_one_player_game(self) -> None:
        """Function is_one_player_game."""

        self._check(mm.is_one_player_game, ['P1'], bool)

    def test_is_human(self) -> None:
        """Function is_human."""

        self._check(mm.is_human, ['Player One', 'P1'], bool)

    def test_current_player_score(self) -> None:
        """Function current_player_score."""

        self._check(mm.current_player_score, [1, 2, 'Player One'], int)

    def test_is_bonus_letter(self) -> None:
        """Function is_bonus_letter."""

        self._check(mm.is_bonus_letter, ['^^^le', 'a', 'apple'], bool)

    def test_get_updated_char_view(self) -> None:
        """"Function get_updated_char_view."""

        self._check(mm.get_updated_char_view, ['^^^le', 'apple', 0, 'a'], str)

    def test_calculate_score(self) -> None:
        """Function calculate_score."""

        self._check(mm.calculate_score, [4, 3, 'C'], int)

    def test_next_player(self) -> None:
        """Function next_player."""

        self._check(mm.next_player, ['Player One', 0, 'P1'], str)

    def test_is_fully_hidden(self) -> None:
        """Function is_fully_hidden."""

        self._check(mm.is_fully_hidden, ['^^^le', 1, 'apple'], bool)

    def test_computer_chooses_solve(self) -> None:
        """Function computer_chooses_solve."""

        self._check(mm.computer_chooses_solve, ['a^^le', 'H', 'pgh'], bool)

    def test_erase(self) -> None:
        """Function erase."""

        self._check(mm.erase, ['abc', 1], str)

    def test_check_constants(self) -> None:
        """Values of constants."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, mm)
        print('  check complete')

    def _check(self, func: callable, args: list, ret_type: type) -> None:
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
             'a1_checker.py'])
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style with Python TA')
print('  - checking type contract\n')
