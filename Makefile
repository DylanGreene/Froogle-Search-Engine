CXX=		g++
CXXFLAGS=	-g -gdwarf-2 -Wall -std=gnu++11
SHELL=		bash
PROGRAMS=	src/resultsServer

all:		src/resultsServer

src/resultsServer: src/resultsServer.cpp src/Indexer.cpp
	$(CXX) $(CXXFLAGS) $^ -o $@

clean:
	rm -f $(PROGRAMS)

#test: test-output test-memory test-time

#test-output: src/resultsServer
	
