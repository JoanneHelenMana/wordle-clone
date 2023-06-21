#!/usr/bin/env python3
"""
Guess-My-Word is a word game in which the user is given 6 attempts to guess a 5-letter English word of the day.
The program randomly picks a valid target word and provides hints to the user based on the their guess.
The game is won when the user correctly guesses the target word, or is lost when there is no correct guess
within the 6 attempts.

Author: Joanne Helen Mana
Company: words-are-us
Copyright: November, 2022
"""
import random
import os

MISS = 0  # _-.: letter not found
MISPLACED = 1  # O, ?: letter in wrong place
EXACT = 2  # X, +: right letter, right place

MAX_ATTEMPTS = 6
WORD_LENGTH = 5

ALL_WORDS = 'word-bank/all_words.txt'
TARGET_WORDS = 'word-bank/target_words.txt'
MISS_LETTERS_FILE = 'miss_letters.txt'


def play():
    """Code that controls the interactive game play."""
    delete_miss_letters()
    attempt = 0
    word_of_the_day = get_target_word()
    valid_words = get_valid_words()

    print("Welcome to Guess My Word.\n")
    user_name = get_user_name()

    while attempt < MAX_ATTEMPTS:
        guess = ask_for_guess(valid_words, user_name)
        attempt += 1

        score = score_guess(guess, word_of_the_day)
        print(format_score(guess, score))
        print(track_miss_letters(guess, word_of_the_day))

        if is_correct(score) is True:
            print(f'\nWell done, {user_name}, you won!\nWord of the day: {word_of_the_day}\n')

        else:
            if attempt == MAX_ATTEMPTS:
                print(f'\nSorry, you lost, {user_name} :(\nThe word of the day was "{word_of_the_day}"\n')

            else:
                print(f'Not quite right, human. Give it another go.\n')


def is_correct(score):
    """
    Checks if the score is entirely correct and returns True if it is.

    Args:
        score: a 5-element tuple containing the score for user's guess against the target word.

    Tests:
    >>> is_correct((1,1,1,1,1))
    False
    >>> is_correct((2,2,2,2,1))
    False
    >>> is_correct((0,0,0,0,0))
    False
    >>> is_correct((2,2,2,2,2))
    True
    """
    if score == (2, 2, 2, 2, 2):
        return True
    else:
        return False


def get_valid_words(file_path=ALL_WORDS):
    """
    Returns a list containing all valid words.

    Args:
        file_path: a file containing all 5-letter English words valid accepted as guess by game.

    Tests:
    >>> get_valid_words()[0]
    'aahed'
    >>> get_valid_words()[-1]
    'zymic'
    >>> get_valid_words()[10:15]
    ['abamp', 'aband', 'abase', 'abash', 'abask']
    """
    with open(file_path) as file:
        valid_words = file.read().split()

    return valid_words


def get_target_word(file_path=TARGET_WORDS):
    """Picks a random word from a file of valid words.

    Args:
        file_path: the path to the file containing all posible target words.
    Returns:
        a random word from the file.

    To test randomness, I used the proposed expected words to run the test once. 'aback' would return 'newly' everytime,
    and 'zonal' would return 'first'. So to pass the tests, I used 'zonal' and 'aback' as seeds, accordingly.
    >>> random.seed('aback')
    >>> get_target_word()
    'newly'
    >>> random.seed('zonal')
    >>> get_target_word()
    'first'
    """
    with open(file_path) as file:
        words = file.read().split()
    target_word = random.choice(words)

    return target_word


def ask_for_guess(valid_words, user_name):
    """
    Requests a guess from the user directly from stdout/in.

    Returns:
        str: the guess entered by the user. Ensures guess is a valid word of correct length in lowercase.
    """
    while True:
        guess = input(f'Enter your guess, {user_name}:\n')
        guess = guess.lower().strip()
        if guess == 'h':
            game_help()
        elif guess not in valid_words:
            print(f'Error. Please enter a 5-letter valid English word, {user_name}.\n')
        elif len(guess) != WORD_LENGTH:
            print(f'Error. Please enter a 5-letter valid English word, {user_name}.\n')
        else:
            return guess


def score_guess(guess, target_word):
    """
    Given two strings of equal length, returns a tuple of ints representing the score of the guess
    against the target word.

    Args:
        guess: the word entered by user as guess.
        target_word: the word of the day chosen at random by the program from a list of valid words.

    Returns:
        a tuple of ints where the numbers represent a score: 0 = miss, 1 = misplaced, 2 = exact.

    Examples:
    >>> score_guess('hello', 'hello')
    (2, 2, 2, 2, 2)
    >>> score_guess('drain', 'float')
    (0, 0, 1, 0, 0)
    >>> score_guess('hello', 'spams')
    (0, 0, 0, 0, 0)
    >>> score_guess('gauge', 'range')
    (0, 2, 0, 2, 2)
    >>> score_guess('melee', 'erect')
    (0, 1, 0, 1, 0)
    >>> score_guess('array', 'spray')
    (0, 0, 2, 2, 2)
    >>> score_guess('train', 'tenor')
    (2, 1, 0, 0, 1)
    """
    # initialisers
    temporary_score = [' '] * 5
    score_list = []

    # key for letter checked in guess
    checked = '-'

    guess_letters = list(guess)
    target_word_letters = list(target_word)

    # identifies exact scores
    for position, letter in enumerate(guess):
        if letter == target_word[position]:
            temporary_score[position] = 'X'  # 'X': exact
            guess_letters[position] = checked
            target_word_letters.remove(letter)

    for position, letter in enumerate(guess_letters):
        # rules out repeated and/or already checked letters
        if letter != checked:
            # identifies misplaced scores
            if letter in target_word_letters:
                temporary_score[position] = '0'  # '0': misplaced
                guess_letters[position] = checked
                target_word_letters.remove(letter)
            # identifies miss scores
            else:
                temporary_score[position] = '_'  # '_': miss

    # formats score into required convention
    for character in temporary_score:
        if character == 'X':
            score_list.append(2)  # 2: exact
        elif character == '0':
            score_list.append(1)  # 1: misplaced
        elif character == '_':
            score_list.append(0)  # 0: miss
    score = tuple(score_list)

    return score


def game_help():
    """Provides help for the game"""
    print('Guess-My-Word HELP:\nThe goal in Guess-My-Word is to guess a 5-letter English word of the day in 6 '
          'attempts or less.\nFor each attempt, you must enter a valid word. The attempt is not lost if the '
          'guess is invalid - the game continues to ask for a guess until a valid guess is provided.\n'
          'Both the target word and the guess can contain repeated letters. You must enter your guess and press '
          'ENTER.\nThe system returns a score on your guess, which displays if the letters in the guess are '
          'present in the word of the day.\n\nX = exact \n0 = misplaced \n_ = miss\n\nIf the guess is not '
          'correct, the game continues to ask for a guess until the attempts are exhausted (game is lost)\nor '
          'until you correctly guess the word of the day (game is won) within the provided attempts.\n')


def format_score(guess, score):
    """
    Formats a guess with a given score as output to the terminal.

    '_' = miss
    '0' = misplaced
    'X' = exact

    Args:
        guess: the word entered by user as guess.
        score: a 5-element tuple containing the score for user's guess against the target word.

    Returns:
        an easily readable version of the user's guess and its score.

    Examples:
    >>> print(format_score('hello', (0,0,0,0,0)))
    H E L L O
    _ _ _ _ _
    >>> print(format_score('hello', (0,0,0,1,1)))
    H E L L O
    _ _ _ 0 0
    >>> print(format_score('hello', (1,0,0,2,1)))
    H E L L O
    0 _ _ X 0
    >>> print(format_score('hello', (2,2,2,2,2)))
    H E L L O
    X X X X X
    """
    score_format = ()
    miss = ('_',)
    misplaced = ('0',)
    exact = ('X',)

    # formats guess
    upper_guess = guess.upper()
    output_guess = ' '.join(upper_guess)

    # formats score
    score_string = ' '.join(str(value) for value in score)
    for value in score_string:
        if value == '0':
            score_format += miss
        elif value == '1':
            score_format += misplaced
        elif value == '2':
            score_format += exact

    output_score = ' '.join(str(value) for value in score_format)
    output = output_guess + '\n' + output_score

    return output


def track_miss_letters(guess, target_word, file_path=MISS_LETTERS_FILE):
    """
    Tracks and displays to user individual input letters not in target word.

    Args:
        guess: the word entered by user as guess.
        target_word: the word of the day chosen at random by the program from a list of valid words.
        file_path: file created by track_miss_letters() where input letters not in target word are stored.

    Returns:
        a message to user with all letters from their guess that are not in the target word.

    Examples:
    >>> print(track_miss_letters('hello', 'weird'))
    Letters entered not in word of the day: ['H', 'L', 'O']
    >>> delete_miss_letters()
    >>> print(track_miss_letters('avail', 'trace'))
    Letters entered not in word of the day: ['I', 'L', 'V']
    >>> delete_miss_letters()
    """
    tracked_miss_letters = []

    file = open(file_path, 'a')
    for letter in guess:
        if letter not in target_word:
            file.write(f'{letter}')

    file = open(file_path, 'r')
    miss_letters = file.read().upper()

    for letter in miss_letters:
        if letter not in tracked_miss_letters:
            tracked_miss_letters.append(letter)

    tracked_miss_letters.sort()
    miss_letters_tracker = f'Letters entered not in word of the day: {tracked_miss_letters}'

    return miss_letters_tracker


def delete_miss_letters(file_path=MISS_LETTERS_FILE):
    """
    Deletes the text file created by track_miss_letters().

    Args:
        file_path: file created by track_miss_letters() where input letters not in target word are stored.
    """

    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        pass


def get_user_name():
    """Obtains the name of the player, which is used to introduce the game to them.

    Returns:
        str: the name the user inputs.
    """
    user_name = input(f'What is your name, human?\n')
    print(
        f"\nHi, {user_name}. Let's begin, shall we?\nYou have 6 attempts to guess the word of the day."
        f"\nGood luck!\n\nFor help, enter H.\n")

    return user_name


def main(test=False):
    if test:
        import doctest
        return doctest.testmod(verbose=True)
    play()


if __name__ == '__main__':
    main(test=False)
    play()
