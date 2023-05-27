"""CSC108/CSCA08: Fall 2022 -- Assignment 1: Mystery Message Game

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Mario Badr, Jennifer Campbell, Tom Fairgrieve, Diane
Horton, Michael Liut, Jacqueline Smith, Anya Tafliovich and Michelle Craig.
"""

from constants import (CONSONANT_POINTS, VOWEL_COST, CONSONANT_BONUS,
                       PLAYER_ONE, PLAYER_TWO, CONSONANT, VOWEL,
                       SOLVE, QUIT, HUMAN, HUMAN_HUMAN,
                       HUMAN_COMPUTER, EASY, HARD, ALL_CONSONANTS,
                       ALL_VOWELS, PRIORITY_CONSONANTS, HIDDEN)


# We provide this function as an example.
def is_win(view: str, message: str) -> bool:
    """Return True if and only if message and view are a winning
    combination. That is, if and only if message and view are the same.

    >>> is_win('banana', 'banana')
    True
    >>> is_win('a^^le', 'apple')
    False
    >>> is_win('app', 'apple')
    False
    """

    return message == view


# We provide this function as an example of using a function as a helper.
def is_game_over(view: str, message: str, move: str) -> bool:
    """Return True if and only if message and view are a winning
    combination or move is QUIT.

    >>> is_game_over('a^^le', 'apple', 'V')
    False
    >>> is_game_over('a^^le', 'apple', 'Q')
    True
    >>> is_game_over('apple', 'apple', 'S')
    True
    """

    return move == QUIT or is_win(view, message)


def is_one_player_game(game_type: str) -> bool:
    """Return True if an only if the game type is a one-player game.

    >>> is_one_player_game("P1")
    True
    >>> is_one_player_game("PVP")
    False
    """

    return game_type == HUMAN


# We provide the header and docstring of this function as an example
# of where and how to use constants in the docstring.
def is_human(current_player: str, game_type: str) -> bool:
    """Return True if and only if current_player represents a human in a game.

    current_player is PLAYER_ONE or PLAYER_TWO.
    game_type is HUMAN, HUMAN_HUMAN, or HUMAN_COMPUTER.

    In a HUMAN game or a HUMAN_HUMAN game, a player is always
    human. In a HUMAN_COMPUTER game, PLAYER_ONE is human and
    PLAYER_TWO is computer.

    >>> is_human('Player One', 'P1')
    True
    >>> is_human('Player One', 'PVP')
    True
    >>> is_human('Player Two', 'PVP')
    True
    >>> is_human('Player One', 'PVE')
    True
    >>> is_human('Player Two', 'PVE')
    False
    """
    if game_type == HUMAN_COMPUTER:
        return current_player == PLAYER_ONE
    else:
        return True


def current_player_score(player_one_score: str, player_two_score: str,
                         current_player: str) -> int:
    """Return the score of current_player.

    >>> current_player_score("3","4",PLAYER_TWO)
    "4"
    >>> current_player_score("3","1",PLAYER_ONE)
    "3"
    """
    if current_player == PLAYER_ONE:
        return player_one_score
    return player_two_score


def is_bonus_letter(view: str, letter: str, message: str) -> bool:
    """Return True if and only if letter is a bonus letter.

    >>> is_bonus_letter("y^^", "s", "yes")
    True
    >>> is_bonus_letter("f^^^shed", "s", "finished")
    False
    """

    return letter in message and letter not in view


def get_updated_char_view(view: str, message: str, index: int,
                          guess: str) -> str:
    """Return a single character string that is the updated view of
    that one character. If the guess is correct, the updated view should be
    the revealed character. Otherwise, it should be the unchanged.

    >>> get_updated_char_view("y^^", "yes", 1 ,"e")
    "e"
    >>> get_updated_char_view("f^^^shed", "finished", 2 ,"n")
    "n"
    """
    if guess == message[index]:
        return guess
    else:
        return view[index]


def calculate_score(score: int, num_occurrences: int, move: str) -> int:
    """Return the player's score after their latest move.

    >>> calculate_score(5, 2, 'C')
    7
    >>> calculate_score(3, 2, 'V')
    2
    """
    if move == VOWEL:
        return score - VOWEL_COST
    else:
        return score + num_occurrences * CONSONANT_POINTS


def next_player(current_player: str, num_occurrences: int,
                game_type: str) -> str:
    """Return the next player to play the next turn (player one or player two)
    for any given game type.

    >>> next_player("Player One", 2,'P1')
    "Player One"
    >>> next_player("Player Two", 0,'PVP')
    "Player One"
    """
    if game_type == HUMAN or num_occurrences > 0:
        return current_player
    elif current_player == PLAYER_ONE:
        return PLAYER_TWO
    else:
        return PLAYER_ONE


def is_fully_hidden(view: str, index: int, message: str) -> bool:
    """Return True if and only if a character at the given index of the message
    is hidden in the view.

    >>> is_fully_hidden("s^^^^^ious", 3,"suspicious")
    True
    >>> is_fully_hidden("s^^^^^ious", 2,"suspicious")
    False
    """
    return message[index] not in view and view[index] == HIDDEN


# Helper function for computer_chooses_solve
# This function is already complete. You must not modify it.
def half_revealed(view: str) -> bool:
    """Return True if and only if at least half of the alphabetic
    characters in view are revealed.

    >>> half_revealed('')
    True
    >>> half_revealed('x')
    True
    >>> half_revealed('^')
    False
    >>> half_revealed('a^,^c!')
    True
    >>> half_revealed('a^b^^e ^c^d^^d')
    False
    """

    num_hidden = view.count(HIDDEN)
    num_alphabetic = 0
    for char in view:
        if char.isalpha():
            num_alphabetic += 1
    return num_alphabetic >= num_hidden


def computer_chooses_solve(view: str, difficulty: str, consonants: str) -> bool:
    """Return True if and only if the computer decides to solve the mystery in
    a PVE game. If on hard difficulty, return True if half of the letters have
    been revealed or if there are no more consonants to guess. If difficulty is
    easy, return True if and only if there are no more consonants to choose
    from.

    >>> computer_chooses_solve("su^^ly", "H", "pfgtk")
    True
    >>> computer_chooses_solve("su^^ly", "E", "p")
    False
    """
    if difficulty == EASY:
        return consonants == ''
    else:
        return consonants == '' or half_revealed(view)


def erase(s: str, index: int) -> str:
    """Return a new string where the character at the index is removed as long
    as the index is between 0 and the index of the last character in the string

    >>> erase("This is a message", 4)
    "Thisis a message"
    >>> erase("CSC108 is fun!", -1)
    "CSC108 is fun"
    """
    if 0 <= index <= len(s):
        return s[:index] + s[index + 1:]
    else:
        return s
