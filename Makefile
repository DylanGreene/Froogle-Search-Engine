CXX=		g++
CXXFLAGS=	-g -gdwarf-2 -Wall -std=gnu++11
SHELL=		bash
PROGRAMS=	src/resultsServer

all:		src/resultsServer

src/resultsServer: src/Indexer.cpp src/resultsServer.cpp
	$(CXX) $(CXXFLAGS) $^ -o $@

clean:
	rm -f $(PROGRAMS)

src/.urlText.txt:
	src/crawler.py -f -t

src/.searchTerms.txt:
	@echo "google" > src/.searchTerms.txt

#test: test-output test-memory test-time
test: test-memory

#test-output: src/resultsServer

test-memory: src/resultsServer src/.searchTerms.txt src/.urlText.txt
	@echo Testing memory...
	@[ `valgrind --leak-check=full ./src/resultsServer < src/.urlText.txt 2>&1 | grep ERROR | awk '{print $$4}'` = 0 ]
