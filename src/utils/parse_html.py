"""
Parse HTML chunks to extract questions and options.
"""

from bs4 import BeautifulSoup
from .utils import add_option


def extract_questions_from_html(html_string):
    """
    Extract questions and options from HTML string.
    
    Args:
        html_string: HTML string to parse
        
    Returns:
        Tuple of (questions list, formatted options list)
    """
    soup = BeautifulSoup(html_string, "html.parser")
    
    # Extract questions
    para = soup.find_all("p", class_="pq")
    questions = [p.get_text() for p in para]
    
    # Format the list items
    options_list = soup.find_all("li")
    options = [opt.get_text() for opt in options_list]
    formatted_options = add_option(options)
    
    return questions, formatted_options


def main():
    """Main function to run the HTML parser."""
    html_string = input("Input your html chunk: ")
    
    questions, formatted_options = extract_questions_from_html(html_string)
    
    print("\n")
    print("##### TEST ######")
    print("\n")
    for p in questions:
        print(f"{p}")
    print("\n")
    for opt in formatted_options:
        print(opt)


if __name__ == "__main__":
    main()
