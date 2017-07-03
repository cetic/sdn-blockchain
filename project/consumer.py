import pika
import json
import os


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='transactions')
channel.queue_declare(queue='op_return_hashes')
op_return_hashes = {
                    "$schema": "http://json-schema.org/draft-04/schema#",

                     "type": "object",
                       "properties": {
                          "hash": { "type": "string" },
                                     }
                   }



def callback(ch, method, properties, body):
    transactions = json.loads(body)
    transaction_id = transactions['TxID']
    bashCommand = "bitcoin-cli getrawtransaction " + transaction_id
    raw_transaction = os.popen(bashCommand).read()
    raw_transaction = str(raw_transaction[0:len(raw_transaction)-1])
    op_return_hashes["hash"] = raw_transaction
    message = json.dumps(op_return_hashes)
    channel.basic_publish(exchange='',
                          routing_key='op_return_hashes',
                          body=message)


channel.basic_consume(callback,
                      queue='transactions',
                      no_ack=True)
print("Waiting for tasks")

channel.start_consuming()

