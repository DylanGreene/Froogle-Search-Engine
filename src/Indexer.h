#ifndef INDEXER_H
#define INDEXER_H

//John Nolan
//Indexer.h
//header file
//Accepts input with a list of urls and the included text, as:
//url1 word1 word2...
//url2 word1 word2...
//url3 ...
//...
//And organizes them into a map of strings and heaps, the heap containing the all the
//urls in which that word occurs and their frequencies.

#include <iostream>
#include <sstream>
#include <unordered_map>
//#include <queue>
#include <vector>
#include <algorithm>
#include <string>

using namespace std;

typedef vector< pair<string, unsigned int> > URLheap;

class Indexer{

    public:
        Indexer();
        void initializeIndex();
        unordered_map<string, URLheap> getIndexer();

    private:
        unordered_map<string, URLheap> indexer; 
        struct index_sort {
            bool operator()(pair<string, unsigned int> const & a, pair<string, unsigned int> const & b) {
                return a.second > b.second; // sort by frequencies
            }
        };    
};

#endif
