__author__ = 'serajago'

import urllib
import sys
import wget
import os
baseDir = os.getcwd() + "\\Images\\"

mobilePicDataFile = open("mobilePicDataFile.tsv", "r", encoding="utf-8")
mobileImagesScrappingStsFile = open("mobileImagesScrappingStsFile.tsv", "r", encoding="utf-8")

mobileImagesScrappingSts = []
mobilePicData = []

for l in mobilePicDataFile:
    for u in l[:-1].split("\t")[1].split("|"):
        if u == "":
            continue
        mobilePicData.append(u)

for l in mobileImagesScrappingStsFile:
    if l[:-1].split("\t")[1] == "DONE":
        mobileImagesScrappingSts.append(l[:-1].split("\t")[0])

mobileImagesScrappingStsFile.close()
mobileImagesScrappingStsFile = open("mobileImagesScrappingStsFile.tsv", "w", encoding="utf-8")

for link in mobileImagesScrappingSts:
    mobileImagesScrappingStsFile.write(link + "\tDONE\n")
mobileImagesScrappingStsFile.flush()

print(mobilePicData[:10])
print(mobileImagesScrappingSts)

imageCount = 0
for link in mobilePicData:
    imageCount += 1
    if link in mobileImagesScrappingSts:
        print("sts: Skipping product " + link[0:25] + "...")
        continue
    print("sts: Processing product " + link[0:25])
    outFile = link.split("/")[-1:][0]
    print(outFile)
    wget.download(link, out=baseDir + outFile)

    #validation
    if os.path.getsize(baseDir + outFile) > 0:
        mobileImagesScrappingStsFile.write(link + "\tDONE\n")
    else:
        mobileImagesScrappingStsFile.write(link + "\tFAILED\n")

    mobileImagesScrappingStsFile.flush()
    mobilePicDataFile.flush()
    print("sts: done product " + link + " total " + str(imageCount))

mobilePicDataFile.close()
mobileImagesScrappingStsFile.close()

