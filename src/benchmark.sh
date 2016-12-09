#!/bin/bash

# benchmark
# iterate through depths of 1, 2, and 3
# then run crawler with and without threading
for i in `seq 3`; do
    echo "Depth: " $i
    echo "without threading..."
    timeout 1h ./crawler.py -n $i -f -t -p -b
    if [ $? -ne 0 ]; then
        echo "  timed out"
    fi
    echo "with threading..."
    timeout 1h ./crawler.py -n $i -f -t -b
    if [ $? -ne 0 ]; then
        echo "  timed out"
    fi
    echo "resultsServer..." $i
    ./measure ./resultsServer 2>&1 | tail -n 1
done
