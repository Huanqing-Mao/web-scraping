import working_javapoint as wj
import pandas as pd

'''
Note that the Question column may contain leading spaces, select
"wrap text" to view the questions in Excel
'''

df = pd.DataFrame()
inputfile = input("Batch file: ")

with open(inputfile, 'r') as file:
    # Read all lines into a list
    lines = file.readlines()

# Remove any trailing newline characters from each line
list = [line.strip() for line in lines]

for i in range(len(list)):
    url = list[i]
    try:
        df1 = wj.url_to_df(url)
        print(f"Progress {i + 1} / {len(list)} ")
        df = df._append(df1)
    except:
        print("Connection failed. Please check format of the source html.")
        quit()


print("======= FINAL DATAFRAME =======")
print(df)
filename = input("Output file: ")
df.to_csv(filename)
print("Success.")
print("Note that the Question column may contain leading spaces, select 'wrap text' to view the questions in Excel")