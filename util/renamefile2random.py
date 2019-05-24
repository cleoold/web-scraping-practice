# renames all files (not folders) in the current folder into random names
# @ cos

import shutil, os, random, re

chars = [chr(j) for j in range(ord('a'), ord('z')+1)] +\
        [chr(j) for j in range(ord('A'), ord('Z')+1)] +\
        [str(j) for j in range(0, 10)]

filenameRegex = re.compile(r'^(.*)(\..+)$') # doesn't work for ones without ext names

fileList = []

def loop(mydir):
    for eachf in os.listdir(mydir):
        now = os.path.join(mydir, eachf)
        if os.path.isfile(now):
            newname = filenameRegex.sub(
                ''.join(random.sample(chars, random.randint(15, 30))) + r'\2', eachf)
            new = os.path.join(mydir, newname)
            print('file "%s"  -->  "%s"' % (now, new))
            fileList.append((now, new))
        else:
            loop(now)

loop('.')
inpt = input('enter confirm: ')
if inpt == 'confirm':
    for each in fileList:
        shutil.move(each[0], each[1])
    input('done.')



