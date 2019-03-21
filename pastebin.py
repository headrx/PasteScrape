from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import webbrowser

#WIll store all pastes from the /archive(recent)
all_pastes = {}

#Selenium driver setup
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

#Request the page
driver.get('https://pastebin.com/archive')
#Get the source and open in soup
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
#Find our table and grab all links
latest_pastes = soup.find('table', class_="maintable")
pastes = latest_pastes.findAll('a')
#add each link to all_pastes as post_title:url
for paste in pastes:
    all_pastes[paste.text] = "https://pastebin.com/raw"+paste['href']
print('[+] Complete')

#Open each link in browser in new tab
for paste in all_pastes:
    browser = webbrowser.open(all_pastes[paste])
    




