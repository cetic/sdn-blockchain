import pika
import sys
import json


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='transactions')

file = open("txs_id.txt","r")
lines = file.readlines()
transactions = {
                    "$schema": "http://json-schema.org/draft-04/schema#",

                     "type": "object",
                       "properties": {
                          "TxID": { "type": "string" },
                                     }
                }
for line in lines:
  line = str(line)
  if line.startswith('TxID'):
    transaction_id = line[6:]
    transactions["TxID"] = transaction_id
    message = json.dumps(transactions)
    channel.basic_publish(exchange='',
                         routing_key='transactions',
                         body=message)

