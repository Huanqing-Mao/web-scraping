"""
Scraping and organizing data from indiabix.com HTML files.
Note that the Question column may contain leading spaces, select
"wrap text" to view the questions in Excel.
"""

from bs4 import BeautifulSoup
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.utils import add_pointer, add_option


def parse_question_text(q_main, instr=""):
    """
    Extract and format question text from HTML element.
    
    Args:
        q_main: BeautifulSoup element containing question text
        instr: General instructions to prepend to question
        
    Returns:
        Formatted question text string
    """
    q_text = ""
    
    # Deal with <p> embedded in the question div
    q_texts = q_main.find_all("p")
    if not q_texts:
        q_text = q_main.get_text()
    else:
        for text in q_texts:
            q_text += f"{text.get_text()}\n"
    
    # Deal with bullets in the question itself
    options = q_main.find("ol")
    bullet_s = ""
    if options:
        bullets = add_pointer([li.get_text() for li in options.find_all("li")])
        for bullet in bullets:
            bullet_s += f"{bullet}\n"
    
    # Deal with tables in the question itself
    tables = q_main.find("table")
    table_text = ""
    if tables:
        cells = [cell.get_text() for cell in tables.find_all("td")]
        for cell in cells:
            table_text += f"{cell}\n"
    
    # Combine all parts
    entire = f"{instr}\n\n{q_text.strip()}\n{bullet_s}\n{table_text}"
    return entire


def parse_question_options(question):
    """
    Extract and format multiple choice options from question element.
    
    Args:
        question: BeautifulSoup element containing the question
        
    Returns:
        Formatted options string
    """
    choices = question.find("div", class_="bix-tbl-options")
    idv_c = choices.find_all("div", class_="d-flex flex-row align-items-top bix-opt-row")
    idv_c = [
        opt.find("div", class_="bix-td-option-val d-flex flex-row align-items-center")
           .find("div", class_="flex-wrap").get_text()
        for opt in idv_c
    ]
    
    # Format options
    formatted_choices = add_option(idv_c)
    entire_c = ""
    for c in formatted_choices:
        entire_c += f"{c}\n"
    
    return entire_c


def parse_question_explanation(question):
    """
    Extract and format answer and explanation from question element.
    
    Args:
        question: BeautifulSoup element containing the question
        
    Returns:
        Tuple of (answer, explanation) strings
    """
    miscell = question.find("div", class_="bix-td-miscell")
    answer = miscell.find("input", class_="jq-hdnakq").get('value')
    
    # Extract explanation
    explanation_ele = miscell.find("div", class_="bix-ans-description table-responsive")
    explanation = ""
    exp_para = explanation_ele.find_all("p")
    
    # Deal with special characters (superscript)
    sup_tags = explanation_ele.find_all("sup")
    if sup_tags:
        for sup in sup_tags:
            sup_text = f"^{sup.get_text()}"
            sup.insert_before(sup_text)
            sup.decompose()
    
    # Deal with <p> embedded
    if exp_para:
        for p in exp_para:
            text = p.get_text()
            # Handle arrows
            if "→" in text:
                text = text.replace("→", "->")
            explanation += f"{text}\n"
    else:
        explanation = explanation_ele.get_text().strip().replace("→", "->")
    
    return answer, explanation


def parse_indiabix_question(question, instr=""):
    """
    Parse a single question from indiabix.com HTML.
    
    Args:
        question: BeautifulSoup element containing the question
        instr: General instructions to prepend to question
        
    Returns:
        Dictionary with 'Question', 'Answer', and 'Solution' keys
    """
    content = question.find("div", class_="d-flex flex-row align-items-top justify-content-start")
    q_main = content.find("div", class_="bix-td-qtxt table-responsive w-100")
    
    # Parse question text
    question_text = parse_question_text(q_main, instr)
    
    # Parse options
    options_text = parse_question_options(question)
    
    # Parse answer and explanation
    answer, explanation = parse_question_explanation(question)
    
    return {
        'Question': question_text + f"\n" + options_text,
        'Answer': answer,
        'Solution': explanation
    }


def scrape_indiabix_from_file(filename, instr=""):
    """
    Scrape questions from an indiabix.com HTML file.
    
    Args:
        filename: Path to HTML file
        instr: General instructions for the page
        
    Returns:
        pandas DataFrame with scraped questions
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
    
    soup = BeautifulSoup(data, 'html.parser')
    questions = soup.find_all("div", class_="bix-div-container")
    
    table = []
    for question in questions:
        parsed_question = parse_indiabix_question(question, instr)
        table.append(parsed_question)
    
    return pd.DataFrame(table)


def main():
    """Main function to run the indiabix scraper."""
    try:
        # Read file and initialize the soup
        filename = input("Input filename: ")
        instr = input("General instructions for this page(if any): ")
        
        df = scrape_indiabix_from_file(filename, instr)
        
        if len(df) > 0:
            print(f"\n=====================  RESULTS =========================")
            print("Preview of table:")
            print(df)
            
            output_filename = input("Output file name: ")
            df.to_csv(output_filename)
            print("Success.")
            print("Note that the Question column may contain leading spaces, "
                  "select 'wrap text' to view the questions in Excel")
        else:
            print("Please check the format of the file. Expected a Question Page "
                  "source in txt format from www.indiabix.com")
    
    except Exception as e:
        print(f"Error: {e}")
        print("Invalid file.")


if __name__ == "__main__":
    main()
