""" Tests to test function get_bigger_neighbourhood in a3.py """
from a3 import get_bigger_neighbourhood as gbn
from a3 import SAMPLE_DATA


def test_first_bigger() -> None:
    """Test that test_first_bigger correctly returns the first neighbourhood
    when its population is strictly greater than the population of the second
    neighbourhood.
    """
    result = gbn(SAMPLE_DATA, "Rexdale-Kipling", "Elms-Old Rexdale")
    assert result == "Rexdale-Kipling"
    
def test_second_bigger() -> None:
    """Test that test__ correctly returns the second neighbourhood when its 
    population is strictly greater than the population of the first 
    neighbourhood.
    """
    result = gbn(SAMPLE_DATA, "Elms-Old Rexdale", "Rexdale-Kipling")
    assert result == "Rexdale-Kipling"

def test_imaginary_neighbourhood() -> None:
    """Test that test_imaginary_neighbourhood returns the neighbourhood that
    exists in the data when a neighbourhood that is not in the data is passed.
    """
    result = gbn(SAMPLE_DATA, 'Imaginary neighbourhood', 'Rexdale-Kipling')
    assert result == 'Rexdale-Kipling'
    
def test_empty_string() -> None:
    """Test that test_empty_string returns the neighbourhood that exists when 
    an empty string is passed.
    """
    result = gbn(SAMPLE_DATA, '', 'Rexdale-Kipling')
    assert result == 'Rexdale-Kipling'    
    
def test_empty_strings() -> None:
    """Test that test_empty_strings returns an empty string when two empty 
    strings are passsed.
    """
    result = gbn(SAMPLE_DATA, '', '')
    assert result == ''

def test_duplicate() -> None:
    """Test that test_duplicate returns either neighbourhood when the same
    neighbourhood is passed.
    """
    result = gbn(SAMPLE_DATA, 'Rexdale-Kipling', 'Rexdale-Kipling')
    assert result == 'Rexdale-Kipling'

if __name__ == '__main__':
    import pytest
    pytest.main(['test_a3.py'])
