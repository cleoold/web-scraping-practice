# fetches all image page urls in the form 'https://imagebed.net/album/AAAA' with selenium module
# requires Firefox
# requires webdriver
#
# (c) cos in July 2019

import os
import re
import time

import requests
from selenium import common, webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


def firefoxProfile() -> FirefoxProfile:
    firefoxProfile = FirefoxProfile()
    #firefoxProfile.set_preference('permissions.default.stylesheet', 2)
    firefoxProfile.set_preference('permissions.default.image', 2)
    #firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',
    #                              'false')
    return firefoxProfile


def printlog(*args, **kwargs):
    currentTime = time.localtime()
    timeStr = time.strftime('[%y/%m/%d %H:%M:%S]', currentTime)
    print(timeStr, end=' '), print(*args, **kwargs)


def fetchOneArtwork(url: str):
    # getting artwork title with requests
    title = re.search(r'<title>(.+?)</title>',
        requests.get(url).text).group(1).replace(' - Imagebed-The best free Imagebed', '')
    printlog(f'got artwork title {title}')

    browser = webdriver.Firefox(firefoxProfile())

    browser.get(url)

    workingDir = os.path.join(os.path.dirname(__file__), 'urls_to_one_pics')
    os.makedirs(workingDir, exist_ok=True)
    filename = os.path.join(workingDir, title + '.txt')
    while True:

        url2PicElems = browser.find_elements_by_class_name('image-container')

        with open(filename, mode='a', encoding='utf-8') as txtfile:
            printlog('writting urls to file')
            for url2PicElem in url2PicElems:
                txtfile.write(url2PicElem.get_attribute('href') + '\n')
            printlog('urls for this page written; proceeding to next page...')
        
        try:
            button = browser.find_element_by_class_name('pagination-next')
            button.click()
        except (common.exceptions.ElementNotInteractableException, 
                common.exceptions.NoSuchElementException):
            break

    browser.close()
    printlog(f'done for {title}')


if __name__ == '__main__':
    WELCOME_MSG = 'input the urls here:\n'
    urls = []
    myInput = input(WELCOME_MSG).strip()
    while myInput != '':
        urls.append(myInput)
        myInput = input().strip()
    
    for url in urls:
        fetchOneArtwork(url)
    printlog('finished for getting image pages.')
