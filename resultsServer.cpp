#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <cmath>
#include <queue>
#include "Indexer.h"

using namespace std;

int calcSearchTermWeight(unsigned int val)
{
    int toReturn = 0;
    for(int i = 1; i <= val; i++)
    {
        toReturn += 100/pow(2, (i-1));
    }
    return toReturn;
}

struct compareFunc
{
    bool operator()(const pair<string, int>& p1, const pair<string, int>& p2)
    {
        return p1.second < p2.second;
    }
};

int main(void)
{
    Indexer ind;
    vector<string> searchList;
    searchList.push_back("wikipedia");
    searchList.push_back("violation");
    searchList.push_back("top");
    searchList.push_back("bottom");
    searchList.push_back("espn");
    searchList.push_back("Cabin");
    searchList.push_back("trust");
    searchList.push_back("us");
    searchList.push_back("Home");
    searchList.push_back("Upload");
    searchList.push_back("Recommended");
    searchList.push_back("minutes");
    searchList.push_back("Help");
    searchList.push_back("Airbnb");
    searchList.push_back("About");
    ind.initializeIndex();
    map<string, int> urlRanking;
    map<string, URLheap > index = ind.getIndexer();
    /*map<string, vector< pair<string, unsigned int> > > index;
      pair<string, unsigned int> p1("URL2", 10);
      pair<string, unsigned int> p2("URL1", 3);
      pair<string, unsigned int> p3("URL4", 69);
      pair<string, unsigned int> p4("URL3", 32);
      pair<string, unsigned int> p5("URL2", 4);
      pair<string, unsigned int> p6("URL1", 12);
      pair<string, unsigned int> p7("URL4", 6);
      pair<string, unsigned int> p8("URL3", 69);
      pair<string, unsigned int> p9("URL8", 100);
      pair<string, unsigned int> p10("URL1", 2);
      pair<string, unsigned int> p11("URL8", 100);
      pair<string, unsigned int> p12("URL1", 23);
      pair<string, unsigned int> p13("URL7", 2);
      pair<string, unsigned int> p14("URL6", 10);
      pair<string, unsigned int> p15("URL3", 42);

      vector< pair<string, unsigned int> > v1;
      v1.push_back(p1);
      v1.push_back(p2);
      v1.push_back(p3);
      v1.push_back(p4);
      vector< pair<string, unsigned int> > v2;
      v2.push_back(p5);
      v2.push_back(p6);
      v2.push_back(p7);
      v2.push_back(p8);
      vector< pair<string, unsigned int> > v3;
      v3.push_back(p9);
      v3.push_back(p10);
      vector< pair<string, unsigned int> > v4;
      v4.push_back(p11);
      v4.push_back(p12);
      vector< pair<string, unsigned int> > v5;
      v5.push_back(p13);
      v5.push_back(p14);
      v5.push_back(p15);
      index["word"] = v1;
      index["kyle"] = v2;
      index["charlie"] = v3;
      index["ann"] = v4;
      index["zach"] = v5;
      */

    for(int i = 0; i < searchList.size(); i++)
    {
        auto vec = index[searchList[i]];
        for(int j = 0; j < vec.size(); j++){
            int weight = calcSearchTermWeight(vec[j].second);
            urlRanking[vec[j].first] += weight;
        }
    } 


    for(auto it = urlRanking.begin(); it != urlRanking.end(); it++)
    {
        cout << "URL Weights: " << it->first << "-" << it->second << endl;
    }
    string url;
    while(cin >> url)
    {
        int numEdges;
        cin >> numEdges;
        auto it = urlRanking.find(url);
        if(it != urlRanking.end())
        {
            it->second += 5* numEdges;
        }
    }
    priority_queue< pair<string, int>, vector< pair<string, int> >, compareFunc> finalRank;
    for(auto it = urlRanking.begin(); it != urlRanking.end(); it++)
    {
        finalRank.push(*it);
    }
    while(!finalRank.empty())
    {
        auto it = finalRank.top();
        finalRank.pop();
        cout << it.first << " " << it.second << endl;
    }
}


