#include <iostream>
#include <sstream>
#include <map>
//#include <queue>
#include <vector>
#include <algorithm>
#include <string>

using namespace std;

struct index_sort {
 bool operator()(pair<string, unsigned int> const & a, pair<string, unsigned int> const & b) {
	 return a.second > b.second; // sort by frequencies
 }
};

typedef vector< pair<string, unsigned int> > URLheap;

int main(int argc, char *argv[]) {
	
 string url_line;
 string url;
 string word;
 istringstream ss;
 map<string, URLheap > indexer;
 map<string, unsigned int> frequency;
 
 while (!cin.eof()) {
	 
	 // get url followed by all the words
	 getline(cin, url_line);
	 
	 ss.str(url_line);
	 
	 ss >> url;
	 
	 URLheap heap; // adding on to same heap, this is a problem, might need new pointer
	 indexer[url] = heap;
	 
	 while (ss >> word) {
		 // count the frequency of each word
		 if (frequency.find(word) == frequency.end()) {
			 frequency[word] = 1;
		 } else {
			 frequency[word] += 1;
		 }
	 }
	 
	 // add those frequency pairs to the url indexer
	 for (auto it = frequency.begin(); it != frequency.end(); it++) {
		 indexer[url].push_back(*it);
		 push_heap(indexer[url].begin(), indexer[url].end(), index_sort());
	 }
	 
	 url_line.clear();
	 ss.clear();
	 //url.clear();
	 
 }
 
 //Test prints
 for (auto it = indexer.begin(); it != indexer.end(); it++) {
	 
	 cout << it->first << endl;
	 
	 for (auto jt = it->second.begin(); jt != it->second.end(); jt++) {
		 cout << jt->first << ": " << jt->second << "   ";
	 }
	 
	 cout << endl;
 }
 
 return 0;
}

//make_map() { }
//
//reduce_map() { }
