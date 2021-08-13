import smtplib
import datetime
from email.message import EmailMessage
from xml.etree import ElementTree

from bs4 import BeautifulSoup
import requests

# Setup possible email
current_date = datetime.datetime.now()
msg = EmailMessage()
msg['Subject'] = f"!SERVER NEEDS ATTENTION! - {current_date.strftime('%x')} {current_date.strftime('%I')}:{current_date.strftime('%M')} {current_date.strftime('%p')}"
msg['From'] = "youremail"
msg['To'] = "destinationemail"
msg.set_content("Hi,")

# Parse XML for mods being used
dom = ElementTree.parse('lastupdate.xml')

# Move mods into list to iterate
mods = dom.findall('mod')

# Iterate and compare mod update dates
made_changes = False
for mod in mods:
    # Request mod steampage html
    html_text = requests.get(mod.find('mod_link').text).text
    # Get local update date
    last_update = mod.find('mod_last_updated').text
    soup = BeautifulSoup(html_text, 'lxml')

    # Get info from scraped
    mod_name = soup.find('div', class_="workshopItemTitle").text
    latest_mod_info = soup.find_all('div', class_="detailsStatRight")
    mod_status = "--- [ UP TO DATE ]"
    
    # Compare to local data and overwrite accordingly
    if last_update != latest_mod_info[-1].text:
        mod_status = "--- [ NOT UP TO DATE ]"
        mod.find('mod_last_updated').text = latest_mod_info[-1].text

        msg.set_content(msg.get_content + mod_name + mod_status)
        made_changes = True

    print(f"{mod_name} {mod_status}")
    print(f"\tLocal update on: {last_update}\n\tLast update on: {latest_mod_info[-1].text}\n")
        
# If we made changes, notify admin
if made_changes:
    dom.write('lastupdate.xml')
    with smtplib.SMTP('smptserver') as s:
        s.connect('smtpserver')
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("youremail","yourpassword")
        s.send_message(msg)
        s.quit()