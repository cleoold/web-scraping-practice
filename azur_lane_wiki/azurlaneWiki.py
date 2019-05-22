
import os
import re
from random import randint

import bs4
import requests

from blhxhsj import blhxhsjDownload

_DEBUG = False

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' }
mainUrl = r'https://azurlane.wikiru.jp/index.php?%A5%AD%A5%E3%A5%E9%A5%AF%A5%BF%A1%BC%2F%B4%CF%BC%EF%CA%CC'

class azurwikiruDownload(blhxhsjDownload):
    def __init__(self, links2Shipgirls=[]):
        #blhxhsjDownload.__init__(self, links2Shipgirls)
        self.links2Shipgirls = links2Shipgirls
    def getUrls2Shipgirls(self):
        'gets links to each shipgirl'
        try:
            resMain = requests.get(mainUrl, headers=HEADERS)
            resMain.raise_for_status()
            soupMain = bs4.BeautifulSoup(resMain.text, features='lxml')
            if _DEBUG:
                with open('azurwikiru.html', 'w', encoding='utf-8') as src:
                    src.write(str(soupMain))
            # initialises list with keys [category]
            for each in soupMain.find_all('h2', id=re.compile(r'content_1')):
                                             #omits redundant chars
                self.links2Shipgirls.append([re.sub(r' |†', '', each.getText())])
            del self.links2Shipgirls[-1] # last one is "コメントフォーム"
            # gets urls to each shipgirl's page
            matchedTables = soupMain.select('.ie5') # tables contaning ship urls in each category
            # each category is named ie5 and separate. the first match is useless. the reduced length
            # of matchedTables should be the same as for the above reduced category match (h2)
            del matchedTables[0]
            #if len(self.links2Shipgirls) != len(matchedTables): print('warning')
            for j in range(len(self.links2Shipgirls)):
                links2aKind = [ [(each['title'], each['href']) , []] for each in matchedTables[j].select('a')]
                self.links2Shipgirls[j].append(links2aKind)
        except Exception as exc:
            print(exc)
    def getUrls2Images(self):
        'gets links to every image after getting links to characters'
        'MUST BE RUN AFTER getUrls2Shipgirl'
        def getUrls2Images4OneCategory(category):
            # gets image links for each shipgirl page
            for correspondence in category[1]:
                # shipgirlUrl = correspondence[0][1]
                resShipgirl = requests.get(correspondence[0][1], headers=HEADERS)
                soupShipgirl = bs4.BeautifulSoup(resShipgirl.text, features='lxml')
                # getting ALL character images
                links2Images = soupShipgirl.select('.style_td img[src]')
                for each in links2Images:
                    if int(each['width']) > 90: # skip skill, equipment iamges
                        correspondence[1].append({each['alt'] : 'https://azurlane.wikiru.jp/' + each['src']})
                        print('got one shipgirl link' + '.' * randint(3, 6))
        try:
            for category in self.links2Shipgirls:
                getUrls2Images4OneCategory(category)
        except Exception as exc:
            print(exc)

if __name__ == '__main__':
    print('SCRIPT STARTED.')
    x = azurwikiruDownload()
    x.getUrls2Shipgirls()
    x.getUrls2Images()
    if _DEBUG:
        x.writeUrls()
    elif not _DEBUG:
        x.download()
        # below is a reference for multithread downloading as this site is slow
#        total = x.links2Shipgirls
#        del x
#        downloadObjects = []
#        for j in range(len(total)):
#            y = azurwikiruDownload([total[j]])
#            downloadObjects.append(y)
#        import threading
#
#        def downloadOne(downloadObject):
#            downloadObject.download()
#        
#        threads = []
#        for each in downloadObjects:
#            thread = threading.Thread(target=downloadOne, args=[each])
#            threads.append(thread)
#            thread.start()