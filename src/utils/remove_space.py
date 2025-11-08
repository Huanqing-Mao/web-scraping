"""
Remove leading spaces from each line in CSV cells.
"""

import pandas as pd


def remove_leading_space(content):
    """
    Remove leading spaces after newline characters.
    
    Args:
        content: String content to process
        
    Returns:
        String with leading spaces after newlines removed
    """
    if not isinstance(content, str):
        return content
    
    text = ""
    for i in range(1, len(content)):
        prev = content[i - 1]
        if prev == "\n":
            continue
        else:
            text += content[i]
    text = content[0] + text
    return text


def process_csv_file(input_filename, output_filename, column_name="Prompt"):
    """
    Process a CSV file to remove leading spaces from specified column.
    
    Args:
        input_filename: Path to input CSV file
        output_filename: Path to output CSV file
        column_name: Name of the column to process (default: "Prompt")
    """
    df = pd.read_csv(input_filename)
    
    if column_name in df.columns:
        col = df[column_name].dropna().apply(remove_leading_space)
        df[column_name] = col
    else:
        print(f"Warning: Column '{column_name}' not found in CSV.")
        print(f"Available columns: {list(df.columns)}")
    
    df.to_csv(output_filename, index=False)
    print(f"Processed file saved to {output_filename}")


def main():
    """Main function to run the space removal tool."""
    filename = input("File name: ")
    exportname = input("Output file name: ")
    
    process_csv_file(filename, exportname)


if __name__ == "__main__":
    main()
