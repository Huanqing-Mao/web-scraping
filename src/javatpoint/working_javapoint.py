"""
Scraping and organizing data from javatpoint.com URLs.
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.utils import add_option




def format_question_content(group):
    """
    Format question content from a question group.
    
    Args:
        group: Dictionary with question group data
        
    Returns:
        Formatted question text string
    """
    para = ""
    for p in group["p_tags"]:
        if p.name != "ol" and p.name != "button":  # Exclude list and button elements
            para += f"\n{p.get_text()}"
        else:
            # Format the list of options
            bullets = [li.get_text() for li in p.find_all("li")]
            options = add_option(bullets)
            opt_text = "\n".join([f"\n{opt}" for opt in options])
            para += f"\n{opt_text}"
    
    question_main = f"{group['pq'].get_text()}{para}"
    return question_main


def format_answer_and_solution(ans_key_div):
    """
    Extract and format answer and solution from answer key div.
    
    Args:
        ans_key_div: BeautifulSoup element containing answer key
        
    Returns:
        Tuple of (answer, solution) strings
    """
    answers = ans_key_div.find_all('p')
    ans = answers[0]
    
    # Format Explanation
    solutions = answers[1:]
    solution = ""
    for sol_para in solutions:
        solution += f"{''.join(sol_para.find_all(string=True, recursive=False)).strip()}\n"
    
    answer_text = ''.join(ans.find_all(string=True, recursive=False)).strip()
    solution_text = solution.replace("\n", '', 1) if solution else ""
    
    return answer_text, solution_text


def url_to_df(url):
    """
    Scrape questions from a javatpoint.com URL and return as DataFrame.
    
    Args:
        url: URL to scrape
        
    Returns:
        pandas DataFrame with scraped questions
    """
    print("Connecting...")
    response = requests.get(url)
    
    if response.status_code != 200:
        raise ConnectionError(f"Failed to connect to {url}. Status code: {response.status_code}")
    
    # Initialize
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Break down the html into groups, each group representing an entire question
    pq_tags = soup.find_all("p", class_="pq")
    groups = []
    i = 0
    
    while i < len(pq_tags):
        pq = pq_tags[i]
        group = {'pq': pq, 'p_tags': [], 'ans-key': []}
        next_sibling = pq.find_next_sibling()
        
        # Collect elements under the group until the answer section is found
        while next_sibling and (next_sibling.name != 'div' or 'testanswer' not in next_sibling.get('class', [])):
            group['p_tags'].append(next_sibling)
            
            if next_sibling.name == "p" and "pq" in next_sibling.get("class", []):
                i += 1
            
            next_sibling = next_sibling.find_next_sibling()
        
        # Collect all tags in the answer section
        while next_sibling and (next_sibling.name == 'div' and 'testanswer' in next_sibling.get('class', [])):
            group['ans-key'].append(next_sibling)
            next_sibling = next_sibling.find_next_sibling()
        
        i += 1
        groups.append(group)
    
    # Put each question into the table as a row
    table = []
    
    for q in groups:
        # Format the question
        question_main = format_question_content(q)
        
        # Get Answer key and solution
        if q['ans-key']:
            answer, solution = format_answer_and_solution(q['ans-key'][0])
        else:
            answer, solution = "", ""
        
        # Form and add row to table
        row = {
            'Question': question_main,
            'Answer': answer,
            'Solution': solution,
            'url': url  # Add url for easier reference or categorisation
        }
        table.append(row)
    
    # Export data as a DataFrame
    df = pd.DataFrame(table)
    return df
