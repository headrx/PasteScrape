from bs4 import BeautifulSoup
import webbrowser, requests


def retrieve_pastes():
        #WIll store all pastes from the /archive(recent)
        all_pastes = {}
        #Request the page
        s = requests.Session()
        headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        response = s.get('https://pastebin.com/archive', headers=headers)
        #Get the source and open in soup
        page_source = response.content
        soup = BeautifulSoup(page_source, 'lxml')
        #Find our table and grab all links
        latest_pastes = soup.find('table', class_="maintable")
        pastes = latest_pastes.findAll('a')
        #add each link to all_pastes as post_title:url
        for paste in pastes:
                all_pastes[paste.text] = "https://pastebin.com/raw"+paste['href']

        print('[+] Complete')
        print('[+] Opening...')
        return all_pastes

def write_paste_log(url):
        with open('checked_pastes.txt', 'a') as paste_file:
                paste_file.writelines(url+"\n")

def check_log(paste_url):
        with open('checked_pastes.txt', 'r') as paste_file:
                paste_file = paste_file.readlines()
        if paste_url not in paste_file:
                return True
        else:
                return False

def open_pastes(all_pastes):
        #Open all links in browser
        for paste in all_pastes:
                if not all_pastes[paste].startswith('https://pastebin.com/raw/archive') and check_log(all_pastes[paste]):
                        print("[+] URL Opened >> ", all_pastes[paste])
                        write_paste_log(all_pastes[paste])
                        webbrowser.open(all_pastes[paste])

pastes = retrieve_pastes()
open_pastes(pastes)