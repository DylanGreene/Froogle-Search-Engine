CXX=		g++
CXXFLAGS=	-g -gdwarf-2 -Wall -std=c++11
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

src/measure: src/measure.cpp
	$(CXX) $(CXXFLAGS) $^ -o $@

#test: test-output test-memory test-time
test: test-output test-time test-memory

test-output: src/resultsServer src/.searchTerms.txt src/.urlText.txt
	@echo Testing output...
	@cd src; ./resultsServer > /dev/null 2>&1; cd ..
	@test -s ./src/.mapFile.txt || exit 1;

test-memory: src/resultsServer src/.searchTerms.txt src/.urlText.txt
	@echo Testing memory...
	@cd src; [ `valgrind --leak-check=full ./resultsServer 2>&1 | grep ERROR | awk '{print $$4}'` == 0 ]

test-time: src/resultsServer src/.searchTerms.txt src/.urlText.txt src/measure
	@echo Testing time...
	@cd src; ./measure ./resultsServer > /dev/null | tail -n 1 | awk '{ if ($$0 > 30.0) { print "Time limit exceeded"; exit 1} }'
