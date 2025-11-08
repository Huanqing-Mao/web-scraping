### Web Scraping exercises ##

#### Directory Structure ####
- `src/` - All source code files organized by category
  - `indiabix/` - Scripts for scraping indiabix.com
    - `working_indiabix.py` - Main scraper for indiabix HTML files
    - `logical_ded.py` - Scraper for logical deduction questions
  - `javatpoint/` - Scripts for scraping javatpoint.com
    - `working_javapoint.py` - Core scraper module for javatpoint URLs
    - `jpt_url_batch_scraping.py` - Batch processing for multiple URLs
    - `extract_html_trial.py` - HTML extraction trial script
  - `utils/` - Utility functions and helper scripts
    - `utils.py` - Shared formatting functions (add_pointer, add_option, etc.)
    - `remove_space.py` - Remove leading spaces from CSV cells
    - `parse_html.py` - Parse HTML chunks
    - `format_html.py` - Format HTML list items
    - `test_connection.py` - Test URL connection
  - `notebooks/` - Jupyter notebooks
    - `combine_csv.ipynb` - Combine multiple CSV files
    - `remove_space.ipynb` - Remove spaces notebook
    - `trial_test.ipynb` - Trial test notebook
  - `examples/` - Example and learning scripts
    - `forloop_eg.py` - For loop example
- `input/` - Input files (batch URL lists, HTML text files)
- `output/` - Output files (generated CSV files)

#### Program files ####
1. Scraping and Organising data from indiabix.com -> `src/indiabix/working_indiabix.py`
   - The url is not reachable using requests library
   - Manually paste Page Source html into txt files for each Question Page
   - Place input txt files in `input/` directory
   - Use this txt file as the input for the program and the program will organise the data and export a csv to `output/`
   
2. Scraping and Organising data from javatpoint.com -> `src/javatpoint/working_javapoint.py`
   - Paste a list of urls of questions e.g. https://www.javatpoint.com/coding-decoding-2 into a txt file, each line representing a url
   - Place the batch txt file in `input/` directory
   - Use `src/javatpoint/jpt_url_batch_scraping.py` to process batch files - it will read from `input/` and export csv to `output/`
   
3. Combine all csvs in the output directory into one csv file -> `src/notebooks/combine_csv.ipynb`
   - Reads all CSV files from `output/` directory and combines them into `output/combined.csv`
   
4. Remove leading space in each line of each cell -> `src/utils/remove_space.py`
   - Use a csv file from `output/` as input for the program and the program will remove the leading space of each line in the cell and export a cleaned csv to `output/`
