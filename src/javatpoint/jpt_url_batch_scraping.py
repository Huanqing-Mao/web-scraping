"""
Batch scraping from javatpoint.com using a list of URLs.
Note that the Question column may contain leading spaces, select
"wrap text" to view the questions in Excel.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from javatpoint.working_javapoint import url_to_df
import pandas as pd


def read_urls_from_file(filename):
    """
    Read URLs from a text file, one URL per line.
    
    Args:
        filename: Path to text file containing URLs
        
    Returns:
        List of URL strings
    """
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Remove any trailing newline characters from each line
    urls = [line.strip() for line in lines if line.strip()]
    return urls


def scrape_batch_urls(urls):
    """
    Scrape questions from a list of URLs.
    
    Args:
        urls: List of URLs to scrape
        
    Returns:
        pandas DataFrame with all scraped questions
    """
    df = pd.DataFrame()
    
    for i, url in enumerate(urls, 1):
        try:
            df1 = url_to_df(url)
            print(f"Progress {i} / {len(urls)}")
            df = pd.concat([df, df1], ignore_index=True)
        except Exception as e:
            print(f"Connection failed for {url}. Error: {e}")
            print("Please check format of the source html.")
            raise
    
    return df


def main():
    """Main function to run batch scraping."""
    inputfile = input("Batch file: ")
    
    urls = read_urls_from_file(inputfile)
    print(f"Found {len(urls)} URLs to process")
    
    df = scrape_batch_urls(urls)
    
    print("======= FINAL DATAFRAME =======")
    print(df)
    
    filename = input("Output file: ")
    df.to_csv(filename)
    print("Success.")
    print("Note that the Question column may contain leading spaces, "
          "select 'wrap text' to view the questions in Excel")


if __name__ == "__main__":
    main()
