"""
Wordle Game Functions

This module contains functions for implementing and testing a Wordle game.
"""


def validate_guess(guess, word_length=5):
    """
    Validate a Wordle guess.

    A valid guess is a lowercase alphabetic string of exactly 5 characters.

    Parameters
    ----------
    guess : str
        The candidate guess.

    Returns
    -------
    bool
        True if the guess is valid, otherwise False.

    Examples
    --------
    >>> validate_guess("crane")
    True
    >>> validate_guess("CRANE")
    False
    >>> validate_guess("cat")
    False
    """
    if not isinstance(guess, str):
        return False
    if len(guess) != word_length:
        return False
    if not guess.isalpha():
        return False
    return guess.islower()


def check_guess(secret_word, guess):
    """
    Compare a guess to the secret and return Wordle-style feedback.

    Parameters
    ----------
    secret : str
        The secret 5-letter word.
    guess : str
        The guessed 5-letter word.

    Returns
    -------
    list[tuple[str, str]]
        Each element is (letter, color), where color is 'green', 'yellow', or 'gray'.

    Examples
    --------
    >>> check_guess("crane", "react")
    [('r', 'yellow'), ('e', 'yellow'), ('a', 'green'), ('c', 'yellow'), ('t', 'gray')]
    >>> check_guess("crane", "crane")
    [('c', 'green'), ('r', 'green'), ('a', 'green'), ('n', 'green'), ('e', 'green')]
    """
    if len(secret_word) != len(guess):
        return []
    
    result = []
    secret_list = list(secret_word)
    guess_list = list(guess)
    
    # First pass: mark exact matches (green)
    for i in range(len(guess_list)):
        if guess_list[i] == secret_list[i]:
            result.append((guess_list[i], 'green'))
            secret_list[i] = None  # Mark as used
            guess_list[i] = None   # Mark as used
        else:
            result.append((guess_list[i], None))  # Placeholder
    
    # Second pass: mark partial matches (yellow)
    for i in range(len(guess_list)):
        if guess_list[i] is not None:  # Not already marked green
            if guess_list[i] in secret_list:
                result[i] = (guess_list[i], 'yellow')
                # Remove first occurrence from secret_list
                secret_list[secret_list.index(guess_list[i])] = None
            else:
                result[i] = (guess_list[i], 'gray')
    
    return result


def is_valid_word(word, word_list):
    """
    Checks if a word exists in the valid word list.
    
    Args:
        word (str): The word to check.
        word_list (list): List of valid words.
    
    Returns:
        bool: True if word is in the list, False otherwise.
    """
    return word.lower() in [w.lower() for w in word_list]


def calculate_game_score(guesses_used, max_guesses=6):
    """
    Calculates the score for a completed Wordle game.
    
    Args:
        guesses_used (int): Number of guesses used to solve the puzzle.
        max_guesses (int): Maximum allowed guesses (default 6).
    
    Returns:
        int: Score from 0 to max_guesses (higher is better).
    """
    if guesses_used <= 0 or guesses_used > max_guesses:
        return 0
    return max_guesses - guesses_used + 1


def analyze_guess_pattern(guess_history):
    """
    Analyzes the pattern of guesses to provide insights.
    
    Args:
        guess_history (list): List of guess results from previous guesses.
    
    Returns:
        dict: Analysis results including total guesses, unique letters, etc.
    """
    if not guess_history:
        return {'total_guesses': 0, 'unique_letters': 0, 'green_count': 0, 'yellow_count': 0}
    
    total_guesses = len(guess_history)
    all_letters = set()
    green_count = 0
    yellow_count = 0
    
    for guess_result in guess_history:
        for letter, color in guess_result:
            all_letters.add(letter)
            if color == 'green':
                green_count += 1
            elif color == 'yellow':
                yellow_count += 1
    
    return {
        'total_guesses': total_guesses,
        'unique_letters': len(all_letters),
        'green_count': green_count,
        'yellow_count': yellow_count
    }


def filter_word_list(word_list, constraints):
    """
    Filters a word list based on revealed constraints.
    
    Args:
        word_list (list): List of possible words.
        constraints (dict): Dictionary with 'green', 'yellow', 'gray' constraints.
    
    Returns:
        list: Filtered list of words that match the constraints.
    """
    if not constraints:
        return word_list
    
    filtered_words = []
    
    for word in word_list:
        word_lower = word.lower()
        valid = True
        
        # Check green constraints (exact position)
        if 'green' in constraints:
            for pos, letter in constraints['green'].items():
                if word_lower[int(pos)] != letter.lower():
                    valid = False
                    break
        
        # Check yellow constraints (letter exists but not in this position)
        if valid and 'yellow' in constraints:
            for pos, letter in constraints['yellow'].items():
                if word_lower[int(pos)] == letter.lower() or letter.lower() not in word_lower:
                    valid = False
                    break
        
        # Check gray constraints (letter not in word)
        if valid and 'gray' in constraints:
            for letter in constraints['gray']:
                if letter.lower() in word_lower:
                    valid = False
                    break
        
        if valid:
            filtered_words.append(word)
    
    return filtered_words
