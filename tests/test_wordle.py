"""
Test file for Wordle functions - Completed Version
Modeled after the provided template.
"""

import pytest
from wordle_jz4007.wordle import (
    validate_guess,
    check_guess,
    is_valid_word,
    filter_word_list,
)

# Word list for testing
WORD_LIST = [
    "crane", "apple", "hello", "world", "python",
    "house", "water", "light", "music", "dream",
    "happy", "smile", "peace", "heart", "brain",
    "table", "chair", "phone", "paper", "green"
]


# =============================================================================
# PART 1: BASIC TESTING
# =============================================================================

def test_validate_guess():
    """
    Test the validate_guess function with various inputs.

    Behavior based on the provided wordle.py:
    - Returns True only for 5-letter, all-lowercase, alphabetic strings.
    - Returns False for uppercase, wrong length, non-alphabetic, non-string, empty.
    """
    assert validate_guess("crane") is True
    assert validate_guess("apple") is True


    assert validate_guess("CRANE") is False
    assert validate_guess("Apple") is False

    assert validate_guess("cra") is False
    assert validate_guess("craness") is False
    assert validate_guess("") is False

    assert validate_guess("cr4ne") is False
    assert validate_guess("cra_e") is False
    assert validate_guess("12345") is False
    assert validate_guess("!!abc") is False

    assert validate_guess(None) is False
    assert validate_guess(12345) is False


def test_check_guess_basic():
    """
    Test basic check_guess functionality.

    Based on the provided implementation:
    - Returns list of (letter, color) with color in {'green','yellow','gray'}.
    - If secret and guess lengths differ, returns [] (empty list).
    """

    assert check_guess("crane", "crane") == [('c', 'green'), ('r', 'green'), ('a', 'green'), ('n', 'green'), ('e', 'green') ]

    assert check_guess("crane", "blimp") == [('b', 'gray'), ('l', 'gray'), ('i', 'gray'), ('m', 'gray'), ('p', 'gray')]

    assert check_guess("crane", "react") == [('r', 'yellow'), ('e', 'yellow'), ('a', 'green'), ('c', 'yellow'), ('t', 'gray')]

    assert check_guess("short", "longer") == []


def test_is_valid_word():
    """
    Test the is_valid_word function.

    Behavior based on the provided implementation:
    - Case-insensitive membership.
    """
    assert is_valid_word("crane", WORD_LIST) is True
    assert is_valid_word("CrAnE", WORD_LIST) is True

    assert is_valid_word("xxxxx", WORD_LIST) is False
    assert is_valid_word("cranes", WORD_LIST) is False


# =============================================================================
# PART 2: ADVANCED TESTING
# =============================================================================

@pytest.mark.parametrize("secret_word,guess,expected", [
    ("crane", "crane",
     [('c', 'green'), ('r', 'green'), ('a', 'green'), ('n', 'green'), ('e', 'green')]),

    ("crane", "blimp",
     [('b', 'gray'), ('l', 'gray'), ('i', 'gray'), ('m', 'gray'), ('p', 'gray')]),

    ("crane", "react",
     [('r', 'yellow'), ('e', 'yellow'), ('a', 'green'), ('c', 'yellow'), ('t', 'gray')]),

    ("apple", "paper",
     [('p', 'yellow'), ('a', 'yellow'), ('p', 'green'), ('e', 'yellow'), ('r', 'gray')]),

    ("eerie", "keeps",
     [('k', 'gray'), ('e', 'green'), ('e', 'yellow'), ('p', 'gray'), ('s', 'gray')]),

    ("hello", "lemon",
     [('l', 'yellow'), ('e', 'green'), ('m', 'gray'), ('o', 'yellow'), ('n', 'gray')]),])

def test_check_guess_comprehensive(secret_word, guess, expected):
    """
    Test check_guess with multiple scenarios using parametrize.
    """
    result = check_guess(secret_word, guess)
    assert result == expected, f"Failed for {secret_word} vs {guess}. Expected {expected}, got {result}"


@pytest.fixture
def common_word_list():
    """
    Fixture providing a list of common 5-letter words.
    Uses the WORD_LIST defined above.
    """
    return list(WORD_LIST)  

def test_word_list_fixture(common_word_list):
    """
    Demonstrate fixture usage with is_valid_word and filter_word_list.
    """
    assert is_valid_word("apple", common_word_list) is True
    assert is_valid_word("APPLE", common_word_list) is True
    assert is_valid_word("applz", common_word_list) is False

    # Use filter_word_list with constraints supported by implementation:
    # - green: {position: letter} exact match
    # - yellow: {position: letter} letter must be in word but not at this position
    # - gray: [letters] letters that must not appear
    constraints_green_gray = {"green": {"0": "c"},"gray": ["x", "z"]  }
    filtered = filter_word_list(common_word_list, constraints_green_gray)
    assert "crane" in filtered
    assert "chair" in filtered
    assert "apple" not in filtered 

    # A yellow constraint example:
    constraints_yellow = {
        "yellow": {"0": "a"}
    }
    filtered_yellow = filter_word_list(common_word_list, constraints_yellow)
    assert "crane" in filtered_yellow
    assert "apple" not in filtered_yellow

def test_fixture_contains_common_words(common_word_list):
    """
    Simple test using the common_word_list fixture.

    Purpose:
    - Ensure the fixture-provided list includes some expected common words.
    - Demonstrates that pytest correctly injects the fixture.
    """
    expected_words = {"apple", "crane", "hello"}
    for word in expected_words:
        assert word in common_word_list, f"{word} should be in the fixture word list"

    assert len(common_word_list) > 0, "The fixture word list should not be empty"

