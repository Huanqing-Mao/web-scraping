import working_javapoint as wj
import pandas as pd

df = pd.DataFrame()
inputfile = input("Batch file:")
with open(inputfile, 'r') as file:
    # Read all lines into a list
    lines = file.readlines()

# Remove any trailing newline characters from each line
list = [line.strip() for line in lines]

#list = ["https://www.javatpoint.com/verification-of-the-truth-of-the-statement-1", "https://www.javatpoint.com/logical-problems-1"]
for url in list:
    df1 = wj.url_to_df(url)
    df = df._append(df1)


print("======= FINAL DATAFRAME =======")
print(df)
filename = input("Output file:")
df.to_csv(filename)