#!/usr/bin/python3

# Web Crawler: Recursively follows and finds all links on a webpage using
# multiple threads for faster thread-based parallel processing. Also creates a
# graph to display the connection of all the links visited

# Library Imports
# ------------------------------------------------------------------------

from threading import Thread
import urllib.request
import httplib2
import requests
import sys
from collections import defaultdict
from bs4 import BeautifulSoup, SoupStrainer

# Classes and Fuctions
# ------------------------------------------------------------------------

# Graph class to represent links to and fro different urls

class Graph(object):

    # Inits a graph object. If no dict is given, an empty dict will be used
    def __init__(self, graph=None):
        if graph == None:
            graph = {}
            freqs = {}
        self.__graph = graph
        self.__freqs = freqs

    def add_vertex(self, vertex):
        if vertex not in self.__graph:
            self.__graph[vertex] = []

    def add_edge(self, edge):
        edge = set(edge)
        vertex1 = edge.pop()
        if edge:
            vertex2 = edge.pop()
        else: # Self loop
            vertex2 = vertex1
        if vertex1 in self.__graph:
            self.__graph[vertex1].append(vertex2)
        else:
            self.__graph[vertex1] = [vertex2]
        if vertex2 in self.__freqs:
            self.__freqs[vertex2] += 1
        else:
            self.__freqs[vertex2] = 1

    def __generate_edges(self):
        edges = []
        for vertex in self.__graph:
            for neighbour in self.__graph[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        ret = ""
        for k in self.__freqs:
            ret += str(k) + "\t" + str(self.__freqs[k]) + "\n"
        ret = ret[:len(ret)-1]
        return ret

# Thread class to allow return values

class ThreadWithReturn(Thread):
    def __init__(self, target=None, args=()):
        Thread.__init__(self)
        self.target = target
        self.args = args
        self._return = None

    def run(self):
        if self.target is not None:
            self._return = self.target(*self.args)

    def join(self):
        Thread.join(self)
        return self._return

# Crawler function which gathers all links from a certain url

def crawler(url, graph):
    urls = []
    http = httplib2.Http(timeout=50)
    try:
        status, response = http.request(url)
    except:
        return crawled

    soup = BeautifulSoup(response, 'lxml')
    for link in soup.find_all('a'):
        if link.has_attr('href') and link['href'].startswith("http"):
            graph.add_edge((url, link['href']))
            urls.append(link['href'])
    return urls

# Recursive crawler function

def recursive_crawler(url, crawled, graph, depth):
    if url not in crawled:
        crawled.add(url)
    if len(crawled) > 1000 or depth > 1:
        return crawled
    http = httplib2.Http(timeout=50)
    try:
        status, response = http.request(url)
    except:
        return crawled

    soup = BeautifulSoup(response, 'lxml')
    for link in soup.find_all('a'):
        if link.has_attr('href') and link['href'].startswith("http"):
            graph.add_edge((url, link['href']))
            if link['href'] not in crawled:
                # print(link['href'])
                crawled.add(link['href'])
                print(crawled)
                depth += 1
                recursive_crawler(link['href'], crawled, graph, depth)

# Filters through text from soup and strips text of whitespace

def filterText(text):
    if text.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    return True

# Prints out url with all text from url on one line

def textParser(url):
    print (url, end='')
    webPage = requests.get(url)
    # Format html and only print text from webpage:
    soup = BeautifulSoup(webPage.content, "lxml")
    allText = soup.findAll(text=True)
    for i in allText:
        if filterText(i):
            i = i.lower()
            print (i.replace('\n',' '), end='')


# Main exection
# -----------------------------------------------------------------------

startURLs = ['https://en.wikipedia.org/wiki/Web_crawler',
'https://www3.nd.edu/~pbui/teaching/cse.30331.fa16/reading07.html',
'https://www.youtube.com/', 'http://www.espn.com']
graph = Graph()

'''
found = set()
for url in startURLs:
    found.add(crawler(url,graph))

print(found)
'''

urls = set()
foundurls = set()
crawled = set()
for url in startURLs:
    urls.add(url)
for i in range(2):
    threads = []
    for url in urls:
        if url not in crawled:
            thread = ThreadWithReturn(target=crawler, args=(url,graph,))
            threads.append(thread)
            '''
            found = test_crawler(url, graph)
            crawled.add(url)
            for newly in found:
                foundurls.add(newly)
            for url in foundurls:
                urls.add(url)
            '''
            crawled.add(url)
    for thread in threads:
        thread.start()
    for thread in threads:
        found = thread.join()
        for url in found:
            urls.add(url)
for url in urls:
    print(url)
    # textParser(url)

'''
threads = [threading.Thread(target=crawler, args=(url,graph,)) for url in startURLs]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
'''

# print(graph)
