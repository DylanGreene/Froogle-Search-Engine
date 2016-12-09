#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <cmath>
#include <queue>
#include "Indexer.h"
#include <fstream>
#include <sstream>

//ResultsServer class takes results of web crawl and combines them with search terms to calculate 10 best URLs
using namespace std;

//Calculates the weight of each search term
//Weights are diminishing as url frequencies increase
int calcSearchTermWeight(unsigned int val){
    int toReturn = 0;
    for(unsigned i = 1; i <= val; i++){
        toReturn += 100/pow(2, (i-1));
    }
    return toReturn;
}

//Sorts priority queue based on highest ranking
struct compareFunc{
    bool operator()(const pair<string, int>& p1, const pair<string, int>& p2){
        return p1.second < p2.second;
    }
};

int main(void){
    string searchTerm;
	ifstream checkIfGood(".mapFile.txt");
	//Updates the web crawler's results only if the web crawler has been run recently
	if(!checkIfGood.good()){
    	Indexer ind;
    	ind.initializeIndex();
		ind.toFile();
	}
	checkIfGood.close();
    ifstream checkIfGood2(".searchTerms.txt");
    if(!checkIfGood2.good()){
        cout << "Enter a search term: ";
        string searchstring;
        cin >> searchstring;
        ofstream terms;
        terms.open(".searchTerms.txt");
        terms << searchstring;
        terms.close();
    }
    ifstream searchTerms;
    searchTerms.open(".searchTerms.txt");
    vector<string> searchList;
	//Gets the search terms from a file
    while(searchTerms >> searchTerm){
        searchList.push_back(searchTerm);
    }
	searchTerms.close();
    unordered_map<string, int> urlRanking;
	unordered_map<string, int> urlFrequencies;
	ifstream checkUrlCounts(".urlCounts.txt");
	//Gets the url frequencies
	if(checkUrlCounts.good()){
		string url;
		int urlNums;
		while(checkUrlCounts >> url){
			checkUrlCounts >> urlNums;
			urlFrequencies[url] = urlNums;
		}
	}
	checkUrlCounts.close();
	unordered_map<string, URLheap> index;
	ifstream mapInFile;
	string line;
	string word;
	mapInFile.open(".mapFile.txt");
	//Gets the map that maps a string to its urls and the frequency it appears in each url
	while(getline(mapInFile, line)){
        stringstream ss;
		ss.str(line);
		ss >> word;
		URLheap urlHeap;
		string url;
		int urlCount;
		while(ss >> url){
			ss >> urlCount;
			urlHeap.push_back(pair<string, int>(url, urlCount));
		}
		index[word] = urlHeap;
	}

	//Calculates the ranking of the urls based on the weight and the frequencies
    for(int i = 0; (size_t)i < searchList.size(); i++){
        auto vec = index[searchList[i]];
        for(int j = 0; (size_t)j < vec.size(); j++){
            int weight = calcSearchTermWeight(vec[j].second);
            urlRanking[vec[j].first] += (weight + urlFrequencies[vec[j].first]);
        }
    }

	//Pushes the ranks into a priority queue to sort them
    priority_queue< pair<string, int>, vector< pair<string, int> >, compareFunc> finalRank;
    for(auto it = urlRanking.begin(); it != urlRanking.end(); it++){
        finalRank.push(*it);
    }
	//Prints the top 10 ranks
    for(int i = 0; i < 10; i++){
        auto it = finalRank.top();
        finalRank.pop();
        cout << it.first << endl;
    }
}
