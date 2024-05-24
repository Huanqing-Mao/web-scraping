from bs4 import BeautifulSoup
import pandas as pd

# API functions
def add_pointer(lst):
    pointers = []
    num = len(lst)
    for i in range(num):
        bullet = "I" * (i + 1)
        pointers.append(bullet) 
    #print(pointers) 
    result = []
    for j in range(num):
        result.append(pointers[j] + ". " + lst[j])
    return result

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

# read file and initialise the soup
filename = input("Input filename: ")
with open(filename) as f:
    data = f.read()

soup = BeautifulSoup(data, 'html.parser')

questions = soup.find_all("div", class_="bix-div-container")

instr = input("Input instructions: ")


# store each question into the list
table = []
for question in questions:
    
    # add question main
    content = question.find("div", class_="d-flex flex-row align-items-top justify-content-start")
    q_no = content.find("div", class_="bix-td-qno").get_text() # can just don't show this
    q_main = content.find("div", class_="bix-td-qtxt table-responsive w-100")
    q_texts = q_main.find_all("p") 

    q_text = ""

    # deal with <p> embedded in the question div
    if not q_texts:
        q_text = q_main.get_text()

    else:
        for text in q_texts:
            q_text += f"{text.get_text()}\n"
    
    options = q_main.find("ol", class_="lr-ol-upper-roman")
    bullet_s = ""

    # deal with bullets in the question itself
    if options:
        bullets = add_pointer(list(map(lambda x : x.get_text(), options.find_all("li"))))
        for bullet in bullets:
            bullet_s += f"{bullet}\n"
    entire = f"{instr}\n\n{q_text.strip()}\n{bullet_s}"


    # add multiple choices/options
    choices = question.find("div", class_="bix-tbl-options")
    idv_c = choices.find_all("div", class_="d-flex flex-row align-items-top bix-opt-row")
    idv_c = list(map(lambda x : x.find("div", class_="bix-td-option-val d-flex flex-row align-items-center").find("div", class_="flex-wrap").get_text(), idv_c))
    
    # format options
    formatted_choices = add_option(idv_c)
    entire_c = ""
    for c in formatted_choices:
        entire_c += f"{c}\n"


    # add solutions
    answer = question.find("div", class_="bix-td-miscell").find("input", class_="jq-hdnakq").get('value')

    # add explanation: Explanation may involve <p> or <sup>
    explanation = ""
    explanation_ele = question.find("div", class_="bix-td-miscell").find("div", class_="bix-ans-description table-responsive")
    exp_para = explanation_ele.find_all("p")

    # deal with special characters
    sup_tags = explanation_ele.find_all("sup")
    if sup_tags:
        for sup in sup_tags:
            sup_text = f"^{sup.get_text()}"
            sup.insert_before(sup_text)
            sup.decompose()

    # deal with <p> embedded
    if exp_para:
        for p in exp_para:
            explanation += f"{p.get_text()}\n"
    else:
        explanation = explanation_ele.get_text().strip()
    print(explanation)
    
    
    # final input row
    table.append({'Question' : entire + f"\n" + entire_c, "Answer" : answer, "Solution" : explanation})



######## TESTS #######
print(f"\n=====================  RESULTS =========================")
df = pd.DataFrame(table)
print(df)
output_filename = input("Output file name: ")
df.to_csv(output_filename)
