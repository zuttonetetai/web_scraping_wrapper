"""
requirements:selenium, chromedriver_binary(Win, MacOS)
"""
from bs4 import BeautifulSoup
import requests
import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ast import literal_eval
import time

def get_source_text_with_selenium(url, wait=0, os="windows", headless=True, proxy=None, proxy_id=None, proxy_pass=None):
    """
    scrape web page with selenium.
    """
    options = Options()
    if headless:options.add_argument('--headless') # Headless_mode
    
    if proxy != None:
        options.add_argument('--proxy-server=%s' % proxy)
        if proxy_id != None and proxy_pass != None:
            options.add_argument('--proxy-auth=%s' % proxy_id+':'+proxy_pass)
    
    if os == 'linux':
        CHROME_BIN = "/usr/bin/chromium-browser"
        CHROME_DRIVER = '/usr/lib/chromium-browser/chromedriver'
        options.binary_location = CHROME_BIN
        driver = webdriver.Chrome(CHROME_DRIVER, options=options)
    else:
        import chromedriver_binary
        driver = webdriver.Chrome(options=options)

    #get source and encode to utf-8
    driver.get(url)
    time.sleep(wait) #wait loading
    html = driver.page_source.encode('utf-8')
    decode_text = literal_eval(str(html)).decode()
    return decode_text

def get_source_text(url):
    """
    scrape web page. return str.
    """
    header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    txt = requests.get(url)
    return txt.text

def search_tag(txt, tag, type_='all', class_name=None, id_name=None, output_text_only=True):
    """
    text: str, source_code
    tag: str or list, html-tag (exp. 'a', 'div')
    class_name: str or list, html-class
    id_name: str or list, html-id

    Output: searched text list
    """
    searched = []
    if type_ == 'one':
        if class_name == None and id_name == None:
            t = BeautifulSoup(txt, 'lxml').find(tag)
            if output_text_only:t = t.text 
            searched.append(t)
        if class_name != None:
            t = BeautifulSoup(txt, 'lxml').find(tag, class_=class_name)
            if output_text_only:t = t.text 
            searched.append(t)
        if id_name != None:
            t = BeautifulSoup(txt, 'lxml').find(tag, id=id_name)
            if output_text_only:t = t.text 
            searched.append(t)
    elif type_ == 'all':
        tag_list = []
        if type(tag) is str:
            tag_list.append(tag)
        else:
            tag_list.extend(tag)
        for tg in tag_list:
            if class_name == None and id_name == None:
                t = BeautifulSoup(txt, 'lxml').find_all(tg)
                print(t, type(t))
                if output_text_only:t = [i.text for i in t] 
                searched.extend(t)
            if class_name != None:
                t = BeautifulSoup(txt, 'lxml').find_all(tg, class_=class_name)
                if output_text_only:t = [i.text for i in t]
                searched.extend(t)
            if id_name != None:
                t = BeautifulSoup(txt, 'lxml').find_all(tg, id=id_name)
                if output_text_only:t = [i.text for i in t]
                searched.extend(t)
    else:
        print('tag type error: only str, list or tuple')
    return searched
