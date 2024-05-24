import re

print("Input html source text: ")
words = input()


def format(text):
    ''' sample text: 

    <li>Statement II is the cause and statement I is its effect</li>
    <li>Statement I is the cause and statement II is its effect</li>
    <li>Both the statements are effects of independent causes</li>
    <li>Both the statements are independent causes</li>
    <li>Both the statements are effects of some common cause</li>

    
    '''

    token = '<li>'
    lst = re.split(token, text)
    result = list(map(lambda x: clean(x), lst))
    result = list(filter(lambda x: True if x else False, result))
    output = add_pointer(result)
    return output

def clean(token):
    token = token.strip()
    if token:
        if token.find("</li>") >= 0:
            token = token[:-5]
        return token
    

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

#print(format(words))
formatted_words = format(words)
for word in formatted_words:
    print(f"{word}\n")