"""
Format HTML list items with alphabet bullets.
"""

import re
from .utils import add_option


def clean_html_token(token):
    """
    Clean HTML token by removing tags and whitespace.
    
    Args:
        token: String token to clean
        
    Returns:
        Cleaned token string or None if empty
    """
    token = token.strip()
    if token:
        if token.find("</li>") >= 0:
            token = token[:-5]
        return token
    return None


def format_list_items(text):
    """
    Format HTML list items with alphabet bullets.
    
    Sample text:
    <li>Statement II is the cause and statement I is its effect</li>
    <li>Statement I is the cause and statement II is its effect</li>
    ...
    
    Args:
        text: HTML text containing list items
        
    Returns:
        List of formatted strings with alphabet bullets
    """
    token = '<li>'
    lst = re.split(token, text)
    result = [clean_html_token(item) for item in lst]
    result = [item for item in result if item]  # Filter out None/empty items
    output = add_option(result)
    return output


def main():
    """Main function to run the HTML formatter."""
    print("Input html source text: ")
    words = input()
    
    formatted_words = format_list_items(words)
    for word in formatted_words:
        print(f"{word}\n")


if __name__ == "__main__":
    main()
