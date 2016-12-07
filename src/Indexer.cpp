//John Nolan
//Indexer.cpp
//Accepts input with a list of urls and the included text, as:
//url1 word1 word2...
//url2 word1 word2...
//url3 ...
//...
//And organizes them into a map of strings and heaps, the heap containing the all the
//urls in which that word occurs and their frequencies.
//TODO: make this a class

#include <iostream>
#include <sstream>
#include <unordered_map>
//#include <queue>
#include <vector>
#include <algorithm>
#include <string>
#include "Indexer.h"
using namespace std;

Indexer::Indexer(){}



void Indexer::initializeIndex(){	
    string url_line;
    string url;
    string word;
    istringstream ss;
    unordered_map<string, unsigned int> frequency;

    while (!cin.eof()) {

        // get url followed by all the words
        getline(cin, url_line);

        ss.str(url_line);

        ss >> url;

        
        while (ss >> word) {
            // count the frequency of each word
            if (frequency.find(word) == frequency.end()) {
                if (indexer.find(word) == indexer.end()) {
                    URLheap heap; 
                    indexer[word] = heap;
                    // make a new heap since the word is not in our indexer
                }
                frequency[word] = 1;
            } else {
                frequency[word] += 1;
            }
        }

        // add those frequency pairs to the wolrd indexer
        for (auto it = frequency.begin(); it != frequency.end(); it++) {
            indexer[it->first].push_back(pair<string, unsigned int>(url, it->second));
            push_heap(indexer[it->first].begin(), indexer[it->first].end(), index_sort());
        }

        url_line.clear();
        url.clear();
        ss.clear();
        frequency.clear();

    }
/*
    //Test prints
    for (auto it = indexer.begin(); it != indexer.end(); it++) {

        cout << it->first << endl;

        for (auto jt = it->second.begin(); jt != it->second.end(); jt++) {
            cout << jt->first << ": " << jt->second << "   ";
        }

        cout << endl;
    }
*/
}

map<string, URLheap > Indexer::getIndexer(){
    return indexer;
}

//make_map() { }
//
//reduce_map() { }
