#!/bin/bash

#benchmark
# iterate through depths of 1, 2, and 3
# then run crawler with and without threading
for i in `seq 1 2 3`;
do
    echo "Depth: " $i
    echo "with threading..." #> benchMark.md
    ./measure ./crawler.py -n $i -t -f 
    echo "without threading..."
    ./measure ./crawler.py -n $i -t -p
    echo "resultsServer..." $i
    for j in `seq 1 2 3`; do
        ./measure ./resultsServer | grep -v "http"
    done
done
  

