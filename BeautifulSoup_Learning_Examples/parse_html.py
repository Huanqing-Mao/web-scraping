from bs4 import BeautifulSoup

## API ###
def add_pointer(lst):
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


### Main ###
html_string = input("input your html chunk: ")
soup = BeautifulSoup(html_string, "html.parser")
clean_text = ' '.join(soup.stripped_strings)

# extract questions
para = soup.find_all("p", class_="pq")
para = list(map(lambda x : x.get_text(), para))


# format the list items
options = soup.find_all("li")
options = list(map(lambda x : x.get_text(), options))
formatted_options = add_pointer(options)


print(f"\n")
print("##### TEST ######")
print(f"\n")
for p in para:
    print(f"{p}")
print(f"\n")
for opt in formatted_options:
    print(opt)