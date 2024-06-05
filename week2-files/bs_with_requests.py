import requests 
from bs4 import BeautifulSoup
import pandas as pd

## API ###
def add_pointer(lst, length):
    pointers = []
    num = len(lst)
    for i in range(num):
        ascii = 65 + i % length
        pointers.append(chr(ascii)) 
    result = []
    for j in range(num):
        result.append(pointers[j] + ". " + lst[j])
    return result


# fetch html from url
url = "https://www.javatpoint.com/course-of-action-1"
data = requests.get(url)
soup = BeautifulSoup(data.text, "html.parser")

# get the questions
lst_of_pq = soup.find_all("p", class_="pq")
PQs = list(map(lambda x : x.get_text(), lst_of_pq))


# get the options for each question
options = soup.find("ol").find_all("li")
options = list(map(lambda x : x.get_text(), options))

# format the list items
formatted_options = add_pointer(options, 5)
option_string = ""
for s in formatted_options:
    option_string += f"\n{s}"

table = []
for pq in PQs:
    table.append({"Question" : pq + option_string})

df = pd.DataFrame(table)
df.to_csv("Question Set.csv")