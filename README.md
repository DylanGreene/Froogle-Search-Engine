# Froogle Search Engine

A basic search engine with a built in web crawler

Setup
-----

This suite requires several things (requires superuser permissions):
* Python3
    * `apt-get install python3`
* httplib2
    * `apt-get install python3-httplib2`
* BeautifulSoup4
    * `apt-get install python3-bs4`
* Flask
    * `apt-get install python3-pip`
    * `pip3 install Flask`
* C++11
    * `add-apt-repository ppa:ubuntu-toolchain-r/test`
    * `apt-get update`
    * `apt-get install g++-4.8`

Once it is ensured that these are installed, run the configure script found in
the root of the this repository as `./configure N` where N is the desired
depth (a depth of 2 is recommended). Also, the N may be omitted entirely since there is a default depth of 1. This will build the necessary dependencies to run the search engine.

Use
---

Following this, the search engine can be run in one of two ways: in the
command line using `./search.sh "search string"`, or on the website which can
be run using `./runWebServer.sh`. If the web server is chosen, simply navigate
in the browser of choice to `localhost:5000`. Search terms can then be entered
into the search box on the site.

Additional Options
------------------

The web crawler script has several other options for more advanced use.
* -n DEPTH            Set the depth to follow links
* -u STARTURLSFILE    Provide a file containing one URL per line for the starting URLs
* -t                  Write the text of each URL to a .urlText.txt
* -f                  Write the number of URLs linking to a URL to .urlFreqs.txt
* -p                  Turn off thread-based parallelism
* -b                  Benchmark the execution in time and memory usage

Note: Options -t and -f should always be run when the intent is to update the
data for the search engine. If however, you are interested simply generating
the graph of websites these options may be omitted.

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

### Results Server: Rank top URLs based on search terms and links

Note: Benchmark performed with search string "Froogle is better than bing".

| Depth | Time       | Memory   | URLs  |
|-------|------------|----------|-------|
| 1     | 0.220 sec  | 30.00 MB | 103   |
| 2     | 0.232 sec  | 30.17 MB | 1107  |
| 3     | 0.272 sec  | 30.16 MB | 11244 |
