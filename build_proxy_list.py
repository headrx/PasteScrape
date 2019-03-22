import requests
from bs4 import BeautifulSoup

def retrieve_latest_link():
        #Build session with headers
        s = requests.Session()
        headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        response = s.get('https://pastebin.com/u/DavidStorm', headers=headers)
        #Get the source and open in soup
        page_source = response.content
        soup = BeautifulSoup(page_source, 'lxml')
        #Find our table and grab the link for latest post
        latest_pastes = soup.find('table', class_="maintable")
        link = latest_pastes.find('a')
        return "https://pastebin.com/raw"+link['href']

def get_list(url):
    proxies = []
    #Build session with headers
    s = requests.Session()
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    response = s.get(url, headers=headers)
    page_source = response.text
    #Create file / empty file if already present
    with open('proxies.txt', 'w') as proxy_file:
        proxy_file.writelines(page_source)
    #Open file, read in contents, grab ip address's, append to list, write to file
    with open('proxies.txt', 'r+') as proxy_file:
        data = proxy_file.readlines()
        for line in data:
            try:
                current_line = line.split()
                ip = current_line[2]
                proxies.append(ip)
                print('[+] Proxy Added : ', ip)
            except:
                pass
    with open('proxies.txt', 'w') as proxy_file:
        for ip in proxies:
            proxy_file.write(ip+"\n")

#Get link for daily post
url = retrieve_latest_link()
#Get contents of pastebin page, clean, and output to proxies.txt
get_list(url)


