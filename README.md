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
