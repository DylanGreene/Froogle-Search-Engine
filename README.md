# Froogle Search Engine
A basic search engine with a built in web crawler

Benchmarking
------------

### Web Crawler: Crawl sites for other URLs and generate graph

| Depth | Threading | Time               | Memory      | URLs  |
|-------|-----------|--------------------|-------------|-------|
| 1     | no        | 0:00:00.411293 sec | 35.696 MB   | 109   |
| 1     | yes       | 0:00:00.482051 sec | 35.904 MB   | 109   |
| 2     | no        | 0:01:17.381260 sec | 62.816 MB   | 1212  |
| 2     | yes       | 0:00:10.655629 sec | 244.704 MB  | 1212  |
| 3     | no        | 0:11:20.715703 sec | 143.656 MB  | 24265 |
| 3     | yes       | 0:02:45.644075 sec | 1588.604 MB | 24241 |

### resultsServer: rank top urls based on search terms and links
### constant search terms "froogle is better than bing" will be used for benchmarking

| Depth | Time       | Memory   | URLs  |
|-------|------------|----------|-------|
| 1     | 0.220 sec  | 30.00 MB | 103   |
| 2     | 0.232 sec  | 30.17 MB | 1107  |
| 3     | 0.272 sec  | 30.16 MB | 11244 |

* Set up: Our project uses both c++ and python. Initially, you 
  need to run ./crawler.py -t -f in order to generate a list 
  of urls and write them to the file .urlText.txt. Then, you 
  can use the Makefile to compile the c++ in the src folder 
  (the Makefile isn't in the src directory but compiles code 
  in the src directory). Now there are two different ways to 
  run our project. ./search.sh [...search terms...] will run 
  the application in the terminal whereas ./runWebServer.sh 
  will run the application in browser (to use you must 
  terminal
