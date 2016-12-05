#!/usr/bin/python3

# Web Crawler: Recursively follows and finds all links on a webpage using
# multiple threads for faster parallel processing. Also creates a graph to
# display the connection of all the links visited

# Library Imports
# ------------------------------------------------------------------------

import threading
import urllib.request
import httplib2
import requests
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
            self.__freqs[vertex1] += 1
        else:
            self.__graph[vertex1] = [vertex2]
            self.__freqs[vertex1] = 1

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

# Recursive crawler function

def crawler(url, crawled, graph, depth):
    if len(crawled) > 100 or depth > 25:
        return
    http = httplib2.Http(timeout=1)
    try:
        status, response = http.request(url)
    except:
        return

    soup = BeautifulSoup(response, 'lxml')
    for link in soup.find_all('a'):
        if link.has_attr('href') and link['href'].startswith("http"):
            graph.add_edge((link['href'], url))
            if link['href'] not in crawled:
                #print(link['href'])
                crawled.add(link['href'])
                depth += 1
                crawler(link['href'], crawled, graph, depth)


# Main exection
# -----------------------------------------------------------------------

startURLs = ['https://en.wikipedia.org/wiki/Web_crawler']
crawled = set()
graph = Graph()

for url in startURLs:
    crawled.add(url)

threads = [threading.Thread(target=crawler, args=(url,crawled,graph,0,)) for url in startURLs]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(graph)
