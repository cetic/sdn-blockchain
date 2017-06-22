#!/bin/bash


while read p; do
  python ~/Downloads/project/send-OP_RETURN.py n1L6W6MR2qq82L741PA2FpzpHjLLFeV2ZC 0.1 $p 1 >> txs_id.txt
  sleep 5s
  python ~/Downloads/project/producer.py
  sleep 1h
done <checkpoint_hashes.txt
