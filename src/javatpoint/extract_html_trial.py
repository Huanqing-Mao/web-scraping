"""
Extract questions from javatpoint.com HTML page.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.utils import add_pointer_cyclic


def fetch_html_from_url(url):
    """
    Fetch HTML content from a URL.
    
    Args:
        url: URL to fetch
        
    Returns:
        BeautifulSoup object of the HTML content
    """
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_questions_from_javatpoint(url):
    """
    Extract questions from a javatpoint.com URL.
    
    Args:
        url: URL of the javatpoint page
        
    Returns:
        pandas DataFrame with extracted questions
    """
    soup = fetch_html_from_url(url)
    
    # Get the questions
    lst_of_pq = soup.find_all("p", class_="pq")
    PQs = [pq.get_text() for pq in lst_of_pq]
    
    # Get the options for each question
    options_list = soup.find("ol").find_all("li")
    options = [opt.get_text() for opt in options_list]
    
    # Format the list items
    formatted_options = add_pointer_cyclic(options, 5)
    option_string = "\n".join([f"\n{opt}" for opt in formatted_options])
    
    # Create table
    table = []
    for pq in PQs:
        table.append({"Question": pq + option_string})
    
    return pd.DataFrame(table)


def main():
    """Main function to run the extractor."""
    url = "https://www.javatpoint.com/course-of-action-1"
    
    df = extract_questions_from_javatpoint(url)
    df.to_csv("../../output/Question Set.csv")
    print(f"Extracted {len(df)} questions and saved to ../../output/Question Set.csv")


if __name__ == "__main__":
    main()
