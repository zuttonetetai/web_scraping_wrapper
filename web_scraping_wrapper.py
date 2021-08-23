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
from tqdm import tqdm
import os
from playwright.sync_api import sync_playwright
import fitz


def get_source_text_with_playright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            java_script_enabled=True,
            user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
            accept_downloads=True
        )
        page = context.new_page()
        page.goto(url, wait_until='domcontentloaded')
        _content = page.content()
        browser.close()
    return _content

def get_source_text_with_selenium(url, timeout=None, wait=0, os="windows", headless=True, proxy=None, proxy_id=None, proxy_pass=None):
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
    if timeout != None:driver.set_page_load_timeout(timeout)
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


def search_tag(txt, tag, search_type='all', class_name=None, id_name=None, output_type='all'):
    """
    text: str, str(source_code), not bs4 tag type
    tag: str or list, html-tag (exp. 'a', 'div')
    search_type: str, 'all' or 'one'
    class_name: str or list, html-class
    id_name: str or list, html-id
    output_type: str, 'all' or 'text' or 'href'

    Output: searched text list
    """
    def decision_output_type(t):
        if search_type == 'all':
            if output_type == 'all':
                t = [str(i) for i in t]
            elif output_type == 'text':
                t = [str(i.text) for i in t]
            else:
                t = [str(i.get(output_type)) for i in t]
        elif search_type == 'one':
            if output_type == 'all':
                t = str(t)
            elif output_type == 'text':
                t = str(t.text)
            else:
                t = str(t.get(output_type))
        return t

    searched = []
    tag_list = []
    if type(tag) is str:tag_list.append(tag)
    else:tag_list.extend(tag)
    
    if search_type == 'one':
        for tg in tag_list:
            if class_name == None and id_name == None:
                t = BeautifulSoup(txt, 'lxml').find(tg)
                t = decision_output_type(t)
                searched.append(t)
            if class_name != None:
                t = BeautifulSoup(txt, 'lxml').find(tg, class_=class_name)
                t = decision_output_type(t) 
                searched.append(t)
            if id_name != None:
                t = BeautifulSoup(txt, 'lxml').find(tg, id=id_name)
                t = decision_output_type(t) 
                searched.append(t)
    elif search_type == 'all':
        tag_list = []
        if type(tag) is str:
            tag_list.append(tag)
        else:
            tag_list.extend(tag)
        for tg in tag_list:
            if class_name == None and id_name == None:
                t = BeautifulSoup(txt, 'lxml').find_all(tg)
                t = decision_output_type(t)
                searched.extend(t)
            if class_name != None:
                t = BeautifulSoup(txt, 'lxml').find_all(tg, class_=class_name)
                t = decision_output_type(t)
                searched.extend(t)
            if id_name != None:
                t = BeautifulSoup(txt, 'lxml').find_all(tg, id=id_name)
                t = decision_output_type(t)
                searched.extend(t)
    else:
        print('tag type error: only str, list or tuple')
    return searched


def download_img(img_url, path, process_name=None, log=True, file_extension='jpg', dl_on_exist_dir=True, use_playwright=False):
    """
    img_url: str or list, image urls
    path: str, download directly path
    process_name: str, show process_name on process bar when log=True
    log: bool, show process bar on terminal
    file_extension: str, 'jpg', 'png' and so on.
    dl_on_exist_dir: bool, True is dl on a already exist directly
    """
    def to_img_from_pdf(pdf_data, path_name_no_ext):
        with fitz.open(stream=pdf_data, filetype="pdf") as doc:
            for i, pg in enumerate(doc):
                for j, img in enumerate(pg.getImageList()):
                    x = doc.extractImage(img[0])
                    name = path_name_no_ext + str(x['ext'])
                    with open(name, "wb") as ofh:
                        ofh.write(x['image'])
    
    def dl_img():    
        i = 0
        if type(img_url) is str:
            try:
                urllib.request.urlretrieve(img_url, os.path.join(path, str(i).rjust(4, '0')+'.'+file_extension))
            except:
                print('DOWNLOAD-ERROR:', path, img_url)
            if log:
                bar = tqdm(total=1)
                if process_name != None:bar.set_description(process_name)
                bar.update(1)
        
        elif type(img_url) is list:
            if log:
                bar = tqdm(total=len(img_url))
                if process_name != None:bar.set_description(process_name)
            for im in img_url:
                try:
                    if use_playwright:
                        with sync_playwright() as p:
                            browser = p.chromium.launch(headless=True)
                            context = browser.new_context(
                                java_script_enabled=True,
                                user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
                                accept_downloads=True
                            )
                            page = context.new_page()
                            page.goto(im, wait_until='load')
                            img_pdf = page.pdf()
                            to_img_from_pdf(img_pdf, os.path.join(path, str(i).rjust(4, '0')+'.'))
                            browser.close()
                    
                    else:
                        #urllib.request.urlretrieve(im, os.path.join(path, str(i).rjust(4, '0')+'.'+file_extension))
                        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
                        request = urllib.request.Request(url=im, headers=headers)
                        with open(os.path.join(path, str(i).rjust(4, '0')+'.'+file_extension), "wb") as f:
                            f.write(urllib.request.urlopen(request).read())
                
                except KeyboardInterrupt:
                    break
                #except Exception as e:
                #    print('DOWNLOAD-ERROR:', e, path, im)
                if log:bar.update(1)
                i = i + 1
        else:
            print('ERROR: img_url should be str or list.')

    exist_bool = os.path.exists(path)
    if exist_bool == True and dl_on_exist_dir == True:
        dl_img()
    elif exist_bool == True and dl_on_exist_dir == False:
        print(path, 'is already exist. download canceled.')
    else:
        os.mkdir(path)
        dl_img()
    