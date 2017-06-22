#!/bin/bash

#while IFS='' read -r line || [[ -n "$line" ]]; do
#file="~/Downloads/project/checkpoint_hashes.txt"
#line=$(head -n 1 file)
#python ~/Downloads/project/send-OP_RETURN.py n1L6W6MR2qq82L741PA2FpzpHjLLFeV2ZC 0.1 $line 1

#echo $line
while read p; do
  python ~/Downloads/project/send-OP_RETURN.py n1L6W6MR2qq82L741PA2FpzpHjLLFeV2ZC 0.1 $p 1 >> txs_id.txt
  sleep 5s
  python ~/Downloads/project/producer.py
  sleep 1h
done <checkpoint_hashes.txt
