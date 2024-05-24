import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.forloop.ai/blog'
response = requests.get(url)

# Parthe the HTML content of the website
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the arciles elemtns on the page
articles = soup.find_all("div", class_="article-item")

data = []
for article in articles:
    title = article.find("h5").text
    date = article.find(class_="blog-post-date-v2").text
    link = article.find("a")['href']
    data.append({'title':title, 'date':date, 'link':link})

df = pd.DataFrame(data)
print(df)