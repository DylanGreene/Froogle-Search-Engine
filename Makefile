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

test-output: src/resultsServer src/.searchTerms.txt src/.urlText.txt
	@echo Testing output...
	@[`./src/resultsServer`]
	@test -s ./src/.mapFile.txt || exit 1;

test-memory: src/resultsServer src/.searchTerms.txt src/.urlText.txt
	@echo Testing memory...
#	@[ `valgrind --leak-check=full ./src/resultsServer 2>&1 | grep ERROR | awk '{print $$4}'` = 0 ]
	@ valgrind --leak-check=full ./src/resultsServer 2>&1 | grep ERROR | awk '{print $$4}'

test-time: src/resultsServer src/.searchTerms.txt src/.urlText.txt
	@echo Testing time...
	@./measure src/resultsServer | tail -n 1 | awk '{ if ($$1 > 1.0) { print "Time limit exceeded"; exit 1} }'
	@./measure src/crawler.py | tail -n 1 | awk '{ if ($$1 > 600) { print "Time limit exceeded"; exit 1} }'
