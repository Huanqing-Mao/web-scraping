import pandas as pd


# Function to cast
def remove_leading_space(content):
    text = ""
    for i in range(1, len(content)):
        
        prev = content[i - 1]
        if prev == f"\n":
            continue
        else:
            text += content[i]
    text = content[0] + text
    return text


# Main
filename = input("File name:")
df = pd.read_csv(filename)
col = df["Prompt"].dropna().apply(remove_leading_space)
df["Prompt"] = col

exportname = input("Output file name:")
df.to_csv(exportname)
