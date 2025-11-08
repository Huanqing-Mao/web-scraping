"""
Utility functions for web scraping and data formatting.
"""


def add_pointer(lst):
    """
    Add roman numeral bullets (I, II, III, etc.) before each item in the list.
    
    Args:
        lst: List of strings to format
        
    Returns:
        List of formatted strings with roman numeral bullets
    """
    pointers = []
    num = len(lst)
    for i in range(num):
        bullet = "I" * (i + 1)
        pointers.append(bullet)
    result = []
    for j in range(num):
        result.append(pointers[j] + ". " + lst[j])
    return result


def add_option(lst):
    """
    Add alphabet bullets (A, B, C, etc.) before each item in the list.
    
    Args:
        lst: List of strings to format
        
    Returns:
        List of formatted strings with alphabet bullets
    """
    pointers = []
    num = len(lst)
    for i in range(num):
        ascii_val = 65 + i  # Start from 'A'
        pointers.append(chr(ascii_val))
    result = []
    for j in range(num):
        result.append(pointers[j] + ". " + lst[j])
    return result


def add_pointer_cyclic(lst, length=5):
    """
    Add alphabet bullets with cycling (A, B, C, D, E, A, B, ...).
    
    Args:
        lst: List of strings to format
        length: Number of options before cycling (default: 5)
        
    Returns:
        List of formatted strings with cyclic alphabet bullets
    """
    pointers = []
    num = len(lst)
    for i in range(num):
        ascii_val = 65 + (i % length)
        pointers.append(chr(ascii_val))
    result = []
    for j in range(num):
        result.append(pointers[j] + ". " + lst[j])
    return result

