# -*- coding: utf-8 -*-
# gets all blog images in the article body from https://bcy.net/item/detail/......
# (c) cos in May 2019

import os
import re

#import bs4
import requests

_DEBUG = False
    # if enabled, matched links will not be downloaded; they will be written to a text file instead

print('this tool worked on 19 May 2019. input urls seperated by enter, press enter twice to end the sequence:')
# the program will then download images from the links given
'sample url: https://bcy.net/item/detail/6543944246305489160'
urls = []

# interface
ipt = input()
while ipt != '':
    urls.append(ipt)
    ipt = input() # do?

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' }

# https:\\u002F\\u002Fp9-bcy.byteimg.com\\u002Fimg\\u002Fbanciyuan\\u002Fuser\\u002F2015226\\u002Fitem\\u002Fc0qsp\\u002Fa9e74a96270c4e579667fd343abe5859.jpg~tplv-banciyuan-w650.image\
for url in urls:
    try:
        #os.makedirs('bcyitem', exist_ok=True)
        #os.chdir('bcyitem')
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        #soup = bs4.BeautifulSoup(res.text, features='lxml')
        jsontext = re.search(r'JSON\.parse\(.+\);', res.text).group()
        matchedUrls = [each[0] for each in re.findall(r'(https:\\.+?\.(jpg|png|jpeg|bmp))', jsontext)]
        for j in range(len(matchedUrls)):
            matchedUrls[j] = re.sub(r'\\\\u002F', '/', matchedUrls[j])
            matchedUrls[j] = re.sub(r'".*"', '', matchedUrls[j])
        matchedUrls = [each for each in matchedUrls if 'img-bcy-qn' in each\
                        and 'bcy.net' not in each and 'bcy.byteimg' not in each\
                        #and 'web' not in each\
                        and 'core' not in each] # experimentally concluded patterns for links to original images
        length = len(matchedUrls)
        if length == 0:
            print('found 0 images. the page might be updated.')
            continue
        title = re.search(r'<title>(.*)</title>', res.text).group(1)
        if _DEBUG:
            with open('bcyitem.html', 'w', encoding='utf-8') as src:
                src.write(jsontext)
            with open('bcyitem.txt', 'a', encoding='utf-8') as txt:
                txt.write(title + '\n')
                for each in matchedUrls:
                    txt.write(each + '\n')
                txt.write('\n')
        # download
        elif not _DEBUG:
            foldername = re.sub(r'/|\\|:|\*|"|<|>|\||\?|\r', '', title)
            os.makedirs(foldername, exist_ok=True)
            os.chdir(foldername)
            for j in range(1, length + 1):
                with open(os.path.basename(matchedUrls[j-1]), 'wb') as file:
                    imgRes = requests.get(matchedUrls[j-1], headers=HEADERS)
                    imgRes.raise_for_status()
                    for chunk in imgRes.iter_content(100000):
                        file.write(chunk)
                print('%d / %d' % (j, length))
            os.chdir('..')
            print()
    except Exception as exc:
        print('an exception needs your attention. hit enter to skip.')
        input(exc)
