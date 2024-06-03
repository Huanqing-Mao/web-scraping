from bs4 import BeautifulSoup
import pandas as pd
import requests


# API functions
def add_option(lst):
    pointers = []
    num = len(lst)
    for i in range(num):
        ascii = 65 + i
        pointers.append(chr(ascii)) 
    #print(pointers) 
    result = []
    for j in range(num):
        result.append(pointers[j] + ". " + lst[j])
    return result

''' 
Format the pointsu class as ABCD

The Roman characters are in the text of the pq class
'''


def url_to_df(url):
    # initialisation
    print("Connecting...")
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        #filename = "jpt_test.txt"
        #with open(filename, encoding="utf8") as f:
            #html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        # get each pq element and the ol following it, and the testanswer following it
        pq_tags = soup.find_all("p", class_="pq")
        #print(pq_tags)
        groups = []


        # find the ol following it
        i = 0
        #print("length = ", len(pq_tags))
        while i < len(pq_tags):
            #print()
            #print("i = ", i)
            pq = pq_tags[i]
            #print("pq = ", pq)
            group = {'pq' : pq, 'p_tags'  : [], 'ans-key': []}
            next_sibling = pq.find_next_sibling()

            
            # Collect <p> tags until the answer section is found
            while next_sibling and (next_sibling.name != 'div' or 'testanswer' not in next_sibling.get('class', [])):
                group['p_tags'].append(next_sibling)
                
                if next_sibling.name == "p" and "pq" in next_sibling.get("class", []):
                    i += 1
                    #print("inner, curr = ", next_sibling)
                next_sibling = next_sibling.find_next_sibling()
                #print("come next = ", next_sibling)
            
            while next_sibling and (next_sibling.name == 'div' and 'testanswer' in next_sibling.get('class', [])):
                group['ans-key'].append(next_sibling)
                next_sibling = next_sibling.find_next_sibling()
            
            i += 1


            groups.append(group) 
        #print(groups)
        table = [] # {qn: , ans: , solution:}
        # formatting questions

        
        for q in groups:
            para = ""
            #print()
            #print("q = ", q)
            for p in q["p_tags"]:
                if p.name != "ol" and p.name != "button":
                    para += f"\n{p.get_text()}"
    
                else:
                    bullets = list(map(lambda x : x.get_text(), p.find_all("li")))
                    options = add_option(bullets)
                    opt_text = ""
                    for opt in options:
                        opt_text += f"\n{opt}"
                    para += f"\n{opt_text}"

            question_main = f"{q['pq'].get_text()}{para}"
            #print("qn main = ", question_main)
            
            #print(q['ans-key'])
            answers = q['ans-key'][0].find_all('p')
            ans = answers[0]
            solutions = answers[1:]
            solution = ""
            for sol_para in solutions:
                solution += f"{''.join(sol_para.find_all(string=True, recursive=False)).strip()}\n"
            #print(''.join(ans.find_all(text=True, recursive=False)).strip())
            #print(solution)
            row = {}
            row['Question'] = question_main
            row['Answer'] = ''.join(ans.find_all(string=True, recursive=False)).strip()
            row['Solution'] = solution.replace("\n",'', 1)
            table.append(row)
        
        
        df = pd.DataFrame(table)
        print("Done organising data.")
        #print(" ===== RESULT =====")
        #print(df)
        return df
        
        
    else:
        print(f"Failed to connect to {url}.")





