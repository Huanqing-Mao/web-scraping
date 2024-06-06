import requests


url = input("CHECK URL: ")
response = requests.get(url)
print(response)