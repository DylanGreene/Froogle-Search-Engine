CXX=		g++
CXXFLAGS=	-g -gdwarf-2 -Wall -std=gnu++11
SHELL=		bash
PROGRAMS=	src/resultsServer src/indexer

all:		src/resultsServer src/indexer

resultsServer: src/resultsServer.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	rm -f $(PROGRAMS)

test: test-output test-memory test-time

test-output: src/resultsServer
	
