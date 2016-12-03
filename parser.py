#!/usr/bin/python3
import requests
import sys
from bs4 import BeautifulSoup

#filters through text from soup and strips text of whitespace
def filterText(text):
    if text.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    if text in ['\n', ' ', '\r', '\t']:
        return False
    return True

#prints out url with all text from url on one line
def textParser(url):
    print (url, end='')
    webPage = requests.get(url)
    #format html and only print text from webpage:
    soup = BeautifulSoup(webPage.content, "lxml")
    allText = soup.findAll(text=True)
    #print (allText[432])
    for i in allText:
        if filterText(i):
            print (i.replace('\n',' '), end='')

def main():
    defaultURLS = "http://en.wikipedia.org/wiki/Web_crawler"
    textParser(defaultURLS)

if __name__ == "__main__":
    main()

