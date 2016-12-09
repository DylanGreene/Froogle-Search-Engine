#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <cmath>
#include <queue>
#include "Indexer.h"
#include <fstream>
#include <sstream>


using namespace std;

int calcSearchTermWeight(unsigned int val){
    int toReturn = 0;
    for(int i = 1; i <= val; i++){
        toReturn += 100/pow(2, (i-1));
    }
    return toReturn;
}

struct compareFunc{
    bool operator()(const pair<string, int>& p1, const pair<string, int>& p2){
        return p1.second < p2.second;
    }
};

int main(void){
    string searchTerm;
	ifstream checkIfGood("mapFile.txt");
	if(!checkIfGood.good())
	{
    	Indexer ind;
    	ind.initializeIndex();
		ind.toFile();
	}
	checkIfGood.close();
    ifstream searchTerms;
    searchTerms.open(".searchTerms.txt");
    vector<string> searchList;
    while(searchTerms >> searchTerm){
        searchList.push_back(searchTerm);
    }
	searchTerms.close();
    unordered_map<string, int> urlRanking;
	unordered_map<string, int> urlFrequencies;
	ifstream checkUrlCounts(".urlCounts.txt");
	if(checkUrlCounts.good())
	{
		string url;
		int urlNums;
		while(checkUrlCounts >> url)
		{
			checkUrlCounts >> urlNums;
			urlFrequencies[url] = urlNums;
		}
	}
	checkUrlCounts.close();
	unordered_map<string, URLheap> index;
	ifstream mapInFile;
	string line;
	string word;
	mapInFile.open("mapFile.txt");
	while(getline(mapInFile, line))
	{
		stringstream ss;
		ss.str(line);
		ss >> word;
		URLheap urlHeap;
		string url;
		int urlCount;
		while(ss >> url)
		{
			ss >> urlCount;	
			urlHeap.push_back(pair<string, int>(url, urlCount));
		}
		index[word] = urlHeap;
	}

    for(int i = 0; i < searchList.size(); i++){
        auto vec = index[searchList[i]];
        for(int j = 0; j < vec.size(); j++){
            int weight = calcSearchTermWeight(vec[j].second);
            urlRanking[vec[j].first] += (weight + 5*urlFrequencies[vec[j].first]);
        }
    }

    priority_queue< pair<string, int>, vector< pair<string, int> >, compareFunc> finalRank;
    for(auto it = urlRanking.begin(); it != urlRanking.end(); it++){
        finalRank.push(*it);
    }
    for(int i = 0; i < 10; i++){
        auto it = finalRank.top();
        finalRank.pop();
        cout << it.first << endl;
    }
}
