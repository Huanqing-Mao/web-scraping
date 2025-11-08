"""
Scraping logical deduction questions from indiabix.com HTML files.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.utils import add_pointer, add_option


def parse_question_content(question):
    """
    Parse question content from HTML element.
    
    Args:
        question: BeautifulSoup element containing the question
        
    Returns:
        Formatted question content string
    """
    content = question.find("div", class_="d-flex flex-row align-items-top justify-content-start")
    q_no = content.find("div", class_="bix-td-qno").get_text()
    q_main = content.find("div", class_="bix-td-qtxt table-responsive w-100")
    
    q_texts = q_main.find_all("p")
    q_text = ""
    for text in q_texts:
        q_text += f"{text.get_text()}\n"
    
    options = q_main.find("ol", class_="lr-ol-upper-roman")
    bullets = add_pointer([li.get_text() for li in options.find_all("li")])
    
    bullet_s = ""
    for bullet in bullets:
        bullet_s += f"{bullet}\n"
    
    entire = f"{q_no} {q_text}{bullet_s}"
    return entire


def parse_question_choices(question):
    """
    Parse multiple choice options from question element.
    
    Args:
        question: BeautifulSoup element containing the question
        
    Returns:
        Formatted choices string
    """
    choices = question.find("div", class_="bix-tbl-options")
    idv_c = choices.find_all("div", class_="d-flex flex-row align-items-top bix-opt-row")
    idv_c = [
        opt.find("div", class_="bix-td-option-val d-flex flex-row align-items-center")
           .find("div", class_="flex-wrap").get_text()
        for opt in idv_c
    ]
    
    formatted_choices = add_option(idv_c)
    entire_c = ""
    for c in formatted_choices:
        entire_c += f"{c}\n"
    
    return entire_c


def parse_question_solution(question):
    """
    Parse answer and explanation from question element.
    
    Args:
        question: BeautifulSoup element containing the question
        
    Returns:
        Tuple of (answer, explanation) strings
    """
    miscell = question.find("div", class_="bix-td-miscell")
    answer = miscell.find("input", class_="jq-hdnakq").get('value')
    explanation = miscell.find("div", class_="bix-ans-description table-responsive").get_text().strip()
    
    return answer, explanation


def scrape_logical_deduction_from_file(filename):
    """
    Scrape logical deduction questions from HTML file.
    
    Args:
        filename: Path to HTML file
        
    Returns:
        pandas DataFrame with scraped questions
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
    
    soup = BeautifulSoup(data, 'html.parser')
    questions = soup.find_all("div", class_="bix-div-container")
    
    table = []
    for question in questions:
        question_content = parse_question_content(question)
        choices = parse_question_choices(question)
        answer, explanation = parse_question_solution(question)
        
        table.append({
            'Question': question_content + f"\n" + choices,
            'Answer': answer,
            'Solution': explanation
        })
    
    return pd.DataFrame(table)


def main():
    """Main function to run the logical deduction scraper."""
    filename = input("Input filename: ")
    
    df = scrape_logical_deduction_from_file(filename)
    
    print(f"\n=====================  RESULTS =========================")
    print(df)
    
    df.to_csv("../../output/Logical Deduction.csv")
    print("Saved to ../../output/Logical Deduction.csv")


if __name__ == "__main__":
    main()
