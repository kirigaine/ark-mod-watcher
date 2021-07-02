import smtplib
from email.message import EmailMessage
from xml.etree import ElementTree

from bs4 import BeautifulSoup
import requests

# Parse XML for mods being used
dom = ElementTree.parse('lastupdate.xml')

# Move mods into list to iterate
mods = dom.findall('mod')

# Iterate 
made_changes = False
for mod in mods:
    html_text = requests.get(mod.find('mod_link').text).text
    last_update = mod.find('mod_last_updated').text
    soup = BeautifulSoup(html_text, 'lxml')

    mod_name = soup.find('div', class_="workshopItemTitle").text
    latest_mod_info = soup.find_all('div', class_="detailsStatRight")

    print(f"{mod_name}: Local update on {last_update}", end='')
    print(f", Last update on {latest_mod_info[-1].text}")
    if last_update != latest_mod_info[-1].text:
        mod.find('mod_last_updated').text = latest_mod_info[-1].text
        made_changes = True
        
if made_changes:
    dom.write('lastupdate.xml')