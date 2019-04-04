from bs4 import BeautifulSoup
import webbrowser
import requests
import sys
import subprocess

def retrieve_pastes():
        """Scrape the newest public pastes """
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
                if 'archive' not in paste['href']:
                        if check_log("https://pastebin.com"+paste['href'])== True:
                                all_pastes[paste.text] = "https://pastebin.com"+paste['href']

        print('[+] Complete')
        print('[+] Opening...')
        return all_pastes

def write_paste_log(url):
        """ Write urls to txt file to keep from viewing duplicates"""
        with open('checked_pastes.txt', 'a') as paste_file:
                paste_file.writelines(url+"\n")

def check_log(paste_url):
        """Check the log of viewed urls"""
        with open('checked_pastes.txt', 'r') as paste_file:
                paste_file = paste_file.readlines()
        if paste_url+'\n' not in paste_file:
                return True
        else:
                return False

def open_pastes(all_pastes):
        """Open all the pastes in browser tabs """
        #Open all links in browser
        for paste in all_pastes:
                #print("[+] URL Opened >> ", all_pastes[paste])
                write_paste_log(all_pastes[paste])
                webbrowser.open(all_pastes[paste])

def submit_pastes(pastes):
        """This will ask user to submit specific pastes they find worth submission"""
        x = 0
        urls = list()
        titles = list()
        for paste in pastes:
                print("[{}] {} : {}".format(x,paste,pastes[paste]))
                urls.append(pastes[paste])
                titles.append(paste)
                x +=1
        print('Enter numbers to submit seperated by commas, no spaces. For ex: 3,4,5,6')
        print("q for exit")
        selections = input('>> ')
        if selections.lower() == "q":
                sys.exit()        
        selections = selections.split(',')
        try:    
                for num in selections:
                        url_split = urls[int(num)].split('/')
                        url_num = url_split.pop()
                        title = titles[int(num)]
                        print("[+]",url_num, title, " -- saved to database")
                        requests.get('http://hotrack.pythonanywhere.com/submit/pastebin/{}/{}'.format(url_num,title))
        except:
                if IndexError:
                        subprocess.call('clear')
                        print('[!] Invalid entry, try again')
                        submit_pastes(pastes)
                
pastes = retrieve_pastes()
open_pastes(pastes)
submit_pastes(pastes)