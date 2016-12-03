#include <iostream>
#include <sstream>
#include <map>
#include <queue>
#include <string>

using namespace std;

struct index_sort {
 bool operator()(pair<string, unsigned int> const & a, pair<string, unsigned int> const & b) {
	return a.second > b.second; // sort by frequencies
 }
};

typedef priority_queue<pair<string, unsigned int>, vector< pair<string, unsigned int> >, index_sort> URLpq;

int main(int argc, char *argv[]) {

 string url_line;
 string url;
 string word;
 istringstream ss;
 map<string, URLpq > indexer;
 map<string, unsigned int> frequency;
 
 while (!cin.eof()) {
	
	// get url followed by all the words
	getline(cin, url_line);
	
	ss.str(url_line);
	
	ss >> url;
	
	URLpq pq;
	indexer[url] = pq;
	while (ss >> word) {
	 if (frequency.find(word) == frequency.end()) {
		frequency[word] = 1;
	 } else {
		frequency[word] += 1;
	 }
	}
	
	for (auto it = frequency.begin(); it != frequency.end(); it++) {
	 indexer[url].push(*it);
	}
	
	
 }
	return 0;
}

//make_map() { }
//
//reduce_map() { }
