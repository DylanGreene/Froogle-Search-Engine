#!/bin/bash

# benchmark
# iterate through depths of 1, 2, and 3
# then run crawler with and without threading
for i in `seq 3`; do
    echo "Depth: " $i
    echo "with threading..."
    timeout 1h ./crawler.py -n $i -t -f -b
    echo "without threading..."
    timeout 1h ./crawler.py -n $i -t -f -p -b
    echo "resultsServer..." $i
    ./measure ./resultsServer 2>&1 | tail -n 1
done
