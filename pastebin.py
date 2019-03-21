from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import webbrowser


def retrieve_pastes():
        #WIll store all pastes from the /archive(recent)
        all_pastes = {}

        #Selenium driver setup
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)

        #Request the page
        driver.get('https://pastebin.com/archive')
        #Get the source and open in soup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        driver.quit()
        #Find our table and grab all links
        latest_pastes = soup.find('table', class_="maintable")
        pastes = latest_pastes.findAll('a')
        #add each link to all_pastes as post_title:url
        for paste in pastes:
                all_pastes[paste.text] = "https://pastebin.com/raw"+paste['href']

        print('[+] Complete')
        print('[+] Opening...')
        return all_pastes


def open_pastes(all_pastes):
        #Open all links in browser
        for paste in all_pastes:
                if not all_pastes[paste].startswith('https://pastebin.com/raw/archive'):
                        print("[+] URL Opened >> ", all_pastes[paste])
                        webbrowser.open(all_pastes[paste])

pastes = retrieve_pastes()
open_pastes(pastes)