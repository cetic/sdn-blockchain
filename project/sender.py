from OP_RETURN import *
import os
import sys, string

#file = open("checkpoint_hashes.txt","r")
#lines = file.readlines()
#testnet = True
#def length_of_file(file):
  #with open(file) as f:
    #return sum(1 for _ in f)

#number_of_txs = length_of_file("checkpoint_hashes.txt")

#if number_of_txs%2 ==0:
  #for line:
    #OP_RETURN_send(mu1NzH3NHFMPwY4v1DwW3k73oNqNqj1xVX, 0.001, str(line), testnet)
#hash_list = []
#count = 1
#size = length_of_file("checkpoint_hashes.txt")
#is_odd = (size%2 == 1)
#for line in lines:
    # strip ending whitespaces including newline char
    #line = line.rstrip()
    # concatenate every two lines
    #if count % 2 == 0:
        #hash_list.append(old_line + ' ' + line)
    #else:
        #old_line = line
    #if is_odd and size == count:
      #hash_list.append(old_line)
    #count += 1
#for hash in hash_list:
   #if not is_odd:
     #hash_list.remove(hash_list[len(hash_list)-1])
os.system('~/Downloads/project/test.sh >> tx_ids.txt')
file = open("tx_ids.txt","r")
lines = file.readlines()
for line in lines:
  line = str(line)
  if line.startswith('TxID'):
   transaction_id = line[6:]
  print transaction_id
