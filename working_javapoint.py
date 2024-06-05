from bs4 import BeautifulSoup
import pandas as pd
import requests

def add_option(lst):    # Add Alphabet bullets(ABCD etc.) before each option in the list
    pointers = []
    num = len(lst)
    for i in range(num):
        ascii = 65 + i   # Start from A by default
        pointers.append(chr(ascii)) 

    result = []
    for j in range(num):
        result.append(pointers[j] + ". " + lst[j])
    return result
 
def url_to_df(url):
    
    print("Connecting...")
    response = requests.get(url)
    if response.status_code == 200:

        # Initialise
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Break down the html into groups, each group representing an entire question
        pq_tags = soup.find_all("p", class_="pq")
        groups = []
        i = 0
        while i < len(pq_tags):
            pq = pq_tags[i]
            group = {'pq' : pq, 'p_tags'  : [], 'ans-key': []}
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
            # Break down each group into question, answer key and explanation

            # Format the question
            para = ""
            for p in q["p_tags"]:
                if p.name != "ol" and p.name != "button": # Exclude list and button elements
                    para += f"\n{p.get_text()}"
    
                else:
                    # format the list of options
                    bullets = list(map(lambda x : x.get_text(), p.find_all("li")))
                    options = add_option(bullets)
                    opt_text = ""
                    for opt in options:
                        opt_text += f"\n{opt}"
                    para += f"\n{opt_text}"

            question_main = f"{q['pq'].get_text()}{para}"

            # Get Answer key
            answers = q['ans-key'][0].find_all('p')
            ans = answers[0]

            # Format Explanation
            solutions = answers[1:]
            solution = ""
            for sol_para in solutions:
                solution += f"{''.join(sol_para.find_all(string=True, recursive=False)).strip()}\n"

            # Form and add row to table
            row = {}
            row['Question'] = question_main
            row['Answer'] = ''.join(ans.find_all(string=True, recursive=False)).strip()
            row['Solution'] = solution.replace("\n",'', 1)
            row['url'] = url # add url for easier reference or categorisation
            table.append(row)
        
        
        # Export data as a Data Frame
        df = pd.DataFrame(table)
        return df
        
        
    else:
        print(f"Failed to connect to {url}.")





