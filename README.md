### Web Scraping exercises ##

#### Program files ####
1. Scraping and Organising data from indiabix.com -> working_indiabix.py
   - The url is not reachable using requests library
   - Manually paste Page Source html into txt files for each Question Page
   - Use this txt file as the input for the program and the program will organise the data and export a csv 
2. Scraping and Organising data from javatpoint.com -> working_javapoint.py
   - Paste a list of urls of questions e.g. https://www.javatpoint.com/coding-decoding-2 into a txt file, each line representing a url
   - Use this txt file as the input for the program and the program will organise and combine the data from all urls and export a csv
3. Combine all csvs in the directory into one csv file -> combine_csv.ipynb
4. Remove leading space in each line of each cell -> remove_space.py
   - Use the csv file as input for the program and the program will remove the leading space of each line in the cell and export a cleaned csv
