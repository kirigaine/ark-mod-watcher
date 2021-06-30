from bs4 import BeautifulSoup
import requests

last_update = ""

with open("lastupdate.txt", "r", encoding="utf-16") as file:
    last_update = file.read()

html_text = requests.get("https://steamcommunity.com/sharedfiles/filedetails/?id=731604991").text
soup = BeautifulSoup(html_text, 'lxml')

mod_info = soup.find_all('div', class_="detailsStatRight")
print(f"{last_update}")
print(mod_info[-1].text)
if last_update == mod_info[-1].text:
    print("true")