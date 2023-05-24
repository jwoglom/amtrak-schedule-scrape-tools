#!/bin/bash

while true; do
	python3 collect.py --origin NYP --dest BOS
	sleep $(shuf -i 300-600 -n 1)
	python3 collect.py --origin NYP --dest WAS
	sleep $(shuf -i 300-600 -n 1)
done
