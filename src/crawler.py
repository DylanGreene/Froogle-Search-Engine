#!/usr/bin/python3

# Web Crawler: Recursively follows and finds all links on a webpage using
# multiple threads for faster thread-based parallel processing. Also creates a
# graph to display the connection of all the links visited

# Library Imports
# ------------------------------------------------------------------------

import re
import string
import os
import sys
import getopt
import httplib2
import requests
import urllib.request
from collections import defaultdict
from threading import Thread
from bs4 import BeautifulSoup, SoupStrainer

# Global Variables
# -------------------------------------------------------------------------

PROGRAM_NAME = os.path.basename(sys.argv[0])

STARTURLS = [
            'https://en.wikipedia.org/wiki/Web_crawler',
            'https://www.nd.edu/',
            'http://www.espn.com'
            'https://www3.nd.edu/~pbui/teaching/cse.30331.fa16/reading03.html'
            'http://stackoverflow.com/questions/927358/how-to-undo-last-commits-in-git'
            ]

DEPTH = 2
GETTEXT = False
GETFREQS = False

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

    def add_edge(self, src, dst):
        if src in self.__graph and dst not in self.__graph[src]:
            self.__graph[src].append(dst)
            if dst in self.__freqs:
                self.__freqs[dst] += 1
            else:
                self.__freqs[dst] = 1
        elif src not in self.__graph:
            self.__graph[src] = [dst]
            if dst in self.__freqs:
                self.__freqs[dst] += 1
            else:
                self.__freqs[dst] = 1

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

# Error function to display error messages

def error(message, exit_code = 1):
    print(message, file=sys.stderr)
    sys.exit(exit_code)

# Usage function for help messages

def usage(exit_code = 0):
    error('''Usage: {} [ [-t -f] -n DEPTH ]

    Options:

        -n DEPTH    Set the depth to follow links
        -t          Write the text of each URL to a .urlText.txt
        -f          Write the number of URLs linking to a URL to .urlFreqs.txt
        -h          Show this help message'''
        .format(PROGRAM_NAME, exit_code))


# Crawler function which gathers all links from a certain url

def crawler(url, graph):
    urls = []
    http = httplib2.Http(timeout=50)
    try:
        status, response = http.request(url)
    except:
        return crawled

    # Use BeautifulSoup to find all links on a page
    soup = BeautifulSoup(response.decode('utf-8', 'ignore'), 'lxml')
    for link in soup.find_all('a'):
        if link.has_attr('href') and link['href'].startswith("http"):
            graph.add_edge(url, link['href'])
            urls.append(link['href'])
    return urls

# Recursive crawler function

def recursive_crawler(url, crawled, graph, depth):
    if url not in crawled:
        crawled.add(url)
    if len(crawled) > 1000 or depth > DEPTH:
        return crawled
    http = httplib2.Http(timeout=50)
    try:
        status, response = http.request(url)
    except:
        return crawled

    # Use BeautifulSoup to find all links on a page
    soup = BeautifulSoup(response, 'lxml')
    for link in soup.find_all('a'):
        if link.has_attr('href') and link['href'].startswith("http"):
            graph.add_edge(url, link['href'])
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

def textParser(url, f):
    line = url + " "
    http = httplib2.Http(timeout=10)
    try:
        status, response = http.request(url)
    except:
        return

    soup = BeautifulSoup(response.decode('utf-8', 'ignore'), 'lxml')
    # Format html and only print text from webpage:
    for word in soup.find_all(text=True):
        if filterText(word):
            pattern = re.compile('[\W_]+') #, re.UNICODE)
            pattern.sub('', word)
            filter(str.isalpha, word)
            word = word.lower()
            word = word.strip()
            word = " ".join(word.split())
            if not len(word) == 0:
                line += word + " "
    print(line, file=f)

# Parse command
# -----------------------------------------------------------------------

try:
    options, arguments = getopt.getopt(sys.argv[1:], "htfn:")
except getopt.GetoptError as e:
    error(e)

for option, value in options:
    if option == '-h':
        usage(0)
    elif option == '-t':
        GETTEXT = True
    elif option == '-f':
        GETFREQS = True
    elif option == '-n': # Option for setting the depth to follow links
        DEPTH = int(value)
    else:
        usage(1)

if not len(arguments) == 0:
    usage(1)

# Main exection
# -----------------------------------------------------------------------

if __name__ == "__main__":
    graph = Graph()

    urls = set()
    crawled = set()

    for url in STARTURLS:
        urls.add(url)

    # Loop a certain depth
    for i in range(DEPTH):
        threads = []
        for url in urls:
            if url not in crawled:
                thread = ThreadWithReturn(target=crawler, args=(url,graph,))
                threads.append(thread)
                crawled.add(url)
        # Start and join the threads
        for thread in threads:
            thread.start()
        for thread in threads:
            found = thread.join()
            for url in found:
                urls.add(url)

    # Get the number of links to each URL
    if GETFREQS:
        urlsFile = open('.urlCounts.txt', 'w')
        print(graph, file=urlsFile)
        urlsFile.close()

    # Get the text for each page
    if GETTEXT:
        textFile = open('.urlText.txt', 'w')
        del threads[:]
        for url in urls:
            # print(url)
            thread = Thread(target=textParser, args=(url,textFile,))
            threads.append(thread)
        for thread in threads:
            if not thread.is_alive():
                thread.start()
        for thread in threads:
            thread.join()

        textFile.close()
