"""
This code is provided solely for the personal and private use of students
taking the CSC108 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Michelle Craig, Tom Fairgrieve, Sadia Sharmin,
Jacqueline Smith, and Sophia Huynh.
"""

from typing import Tuple, Union
from copy import deepcopy

TYPE_ERROR_MSG = '{} should return a {}, but returned {}.'


def run_pyta(filename: str, config_file: str) -> None:
    """Run PythonTA with configuration config_file on the file named filename.
    """
    import json

    error_message = '\nCould not run PythonTA correctly.\n' \
                    'Please make sure you have run the setup.py provided on ' \
                    'Quercus: that should install PythonTA for you.\n' \
                    'Please attend office hours if you require assistance ' \
                    'in running PythonTA.'

    try:
        import python_ta
        with open(config_file) as cf:
            config_dict = json.loads(cf.read())
            config_dict['output-format'] = 'python_ta.reporters.PlainReporter'

        python_ta.check_all(filename, config=config_dict)
    except:
        print(error_message)


def type_check_simple(func: callable, args: list,
                      expected: Union[type, tuple]) -> Tuple[bool, object]:
    """Check if func(args) returns a result of type expected.

    Return (True, result-of-call) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.
    """

    try:
        args_copy = deepcopy(args)
        returned = func(*args_copy)
    except Exception as exn:
        return (False, error_message(func, args, exn))

    if isinstance(returned, expected):
        return (True, returned)

    return (False,
            type_error_message(func.__name__, expected.__name__, returned))


def type_check_full(func: callable, args: list,
                    checker_function: callable) -> Tuple[bool, object]:
    """Run checker_function on func(args).

    Pre: checker_function is also a type-checker (i.e. returns tuple
          in the same format).

    Return (True, result-of-call-func-args) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.
    """

    try:
        args_copy = deepcopy(args)
        returned = func(*args_copy)
    except Exception as exn:
        return (False, error_message(func, args, exn))

    return checker_function(returned)


def type_error_message(func: str, expected: str, got: object) -> str:
    """Return an error message for function func returning got, where the
    correct return type is expected.

    """

    return TYPE_ERROR_MSG.format(func, expected, got)


def error_message(func: callable, args: list,
                  error: Exception) -> str:
    """Return an error message: func(args) raised an error."""

    return 'The call {}({}) caused an error: {}'.format(
        func.__name__, ','.join(map(repr, args)), error)


def returns_list_of_Ts(func: callable, args: list, tp: type):
    """Check if func(args) returns a list of elements of type tp.

    Return (True, result-of-call) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.

    """

    result = type_check_simple(func, args, list)
    if not result[0]:
        return (False, result[1])

    msg = type_error_message(func.__name__, 'list of {}s'.format(tp.__name__),
                             result[1])
    for item in result[1]:
        if not isinstance(item, tp):
            return (False, msg)

    return (True, result[1])


def _mock_disallow(func_name: str):
    """Raise an Exception saying that use of function func_name is not
    allowed.

    """

    def mocker(*args):
        raise Exception(
            "The use of function {} is not allowed.".format(func_name))

    return mocker
