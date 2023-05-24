#!/bin/bash
ERRORS=$(grep '{"error' data/*/*/*|wc -l)
TOTAL=$(find data/ -name '*.json'|wc -l)

echo $ERRORS / $TOTAL
