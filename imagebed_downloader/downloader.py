# download images based on the information from urls collected
#
# (c) cos in July 2019

import os, sys
import threading
import time

import bs4
import requests

from geturls import printlog

FILEDIRPATH = os.path.dirname(__file__)
TXTPATH = os.path.join(FILEDIRPATH, 'urls_to_one_pics')

TOTAL_LEN = len(os.listdir(TXTPATH))

finished_len = 0

PROXY = {}

def fetchUrlForRealImage(url: str) -> str:
    soup = bs4.BeautifulSoup(
        requests.get(url).text, features='lxml')
    fakeImgUrl = soup.select('.image-viewer-main img')[0]['src']
    realImgUrl = fakeImgUrl.replace('md.', '')
    printlog(f'fetched url {realImgUrl}, downloading')
    return realImgUrl

def download(url: str, path: str):
    req = requests.get(url)
    with open(path, mode='wb') as file:
        for chunk in req.iter_content(1024):
            file.write(chunk)

def downloadOneArtwork(tfile: str):
    printlog(f'starting to download from {tfile}')
    try:
        with open(tfile, mode='r', encoding='utf-8') as file:
            workingDir = os.path.join(FILEDIRPATH, 'crawler',
                os.path.basename(tfile)[:-4])
            os.makedirs(workingDir, exist_ok=True)
            for count, url2Pic in enumerate(file):
                url2Pic = url2Pic.strip()
                if url2Pic:
                    realImgUrl = fetchUrlForRealImage(url2Pic)
                    realImgUrlExtName = '.' + realImgUrl.split('.')[-1]
                    filepath = os.path.join(workingDir, str(count) + realImgUrlExtName)
                    download(realImgUrl, filepath)
        printlog(f'FINISHING downloads from {tfile}')
    finally:
        global finished_len
        finished_len += 1


if __name__ == '__main__':
    threads = []
    for file in os.listdir(TXTPATH):
        thread = threading.Thread(
            target=downloadOneArtwork,
            args=(os.path.join(TXTPATH, file),))
        thread.daemon=True
        threads.append(thread)
        thread.start()
    
    while finished_len < TOTAL_LEN:
        try:
            time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            printlog('exited')
            sys.exit()
    for thread in threads:
        thread.join()
    printlog('ok')

