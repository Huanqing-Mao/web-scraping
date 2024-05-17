from bs4 import BeautifulSoup
import pandas as pd

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

# store each question into the list
table = []
for question in questions:
    
    # question main
    content = question.find("div", class_="d-flex flex-row align-items-top justify-content-start")
    q_no = content.find("div", class_="bix-td-qno").get_text()
    q_main = content.find("div", class_="bix-td-qtxt table-responsive w-100")
    q_texts = q_main.find_all("p")
    q_text = ""
    for text in q_texts:
        q_text += f"{text.get_text()}\n"
    options = q_main.find("ol", class_="lr-ol-upper-roman")
    bullets = add_pointer(list(map(lambda x : x.get_text(), options.find_all("li"))))
    bullet_s = ""
    for bullet in bullets:
        bullet_s += f"{bullet}\n"
    entire = f"{q_no} {q_text}{bullet_s}"


    # question multiple choices
    choices = question.find("div", class_="bix-tbl-options")
    idv_c = choices.find_all("div", class_="d-flex flex-row align-items-top bix-opt-row")
    idv_c = list(map(lambda x : x.find("div", class_="bix-td-option-val d-flex flex-row align-items-center").find("div", class_="flex-wrap").get_text(), idv_c))
    formatted_choices = add_option(idv_c)
    entire_c = ""
    for c in formatted_choices:
        entire_c += f"{c}\n"
    


    # add solutions and explanation
    answer = question.find("div", class_="bix-td-miscell").find("input", class_="jq-hdnakq").get('value')
    explanation = question.find("div", class_="bix-td-miscell").find("div", class_="bix-ans-description table-responsive").get_text().strip()
    table.append({'Question' : entire + f"\n" + entire_c, "Answer" : answer, "Solution" : explanation})

df.to_csv("Logical Deduction.csv")

######## TESTS #######
print(f"\n=====================  RESULTS =========================")
df = pd.DataFrame(table)
print(df)
