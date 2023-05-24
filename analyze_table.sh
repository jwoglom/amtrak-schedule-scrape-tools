#!/bin/bash
echo -e "Departure\t\tCurrent\t(For)\tMin\t(For)\t(At)  \tMode\tMean $\tTrain Name"
jq -r '.[] | to_entries[] | [.value["start"], .value["curPrice"], .value["curPriceFor"], .value["minPrice"], .value["minPriceFor"], .value["minPriceAt"], .value["modePrice"], (.value["meanPrice"]*100 | tonumber|floor / 100), .key] | @tsv' < /dev/stdin
