#!/bin/bash

for f in tests/input*.txt; do
    x="${f#tests/input}"   # strip the "tests/input" prefix
    x="${x%.txt}"          # strip the ".txt" suffix
    python3 new_main.py < "$f" > "our_tests/${x}.txt"
    echo "Done: $f -> our_tests/${x}.txt"
done
