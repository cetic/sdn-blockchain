import pika
import json
import os



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='op_return_hashes')

channel.queue_declare(queue='validation_message')

#Validation Output JSON Schema
validation_message = {
                    "$schema": "http://json-schema.org/draft-04/schema#",

                     "type": "object",
                       "properties": {
                          "message": { "type": "string" },
                                     }
                }

#Open Checkpoint Hashes File For Comparison And Validation
file=open("checkpoint_hashes.txt","r")
lines=file.readlines()

#Chekpoint Validation Counter
count = 1

def callback(ch, method, properties, body):
    for line in lines:
       current_hash = str(line)
       print current_hash
       hash = json.loads(body)
       op_return_message = hash['hash']
       print op_return_message
       index_of_message = op_return_message.find('6a20')
       final_hash = op_return_message[index_of_message + 4: len(op_return_message) ]
       print final_hash
       if final_hash == current_hash:
          validation_message['message'] = 'Checkpoint number ' + str(count) + 'has been validated'
       else:
          validation_message['message'] = 'Some security breach happened between Checkpoint ' + str(count) + 'and Checkpoint number ' + str(count -1)
       data = json.dumps(validation_message)
       channel.basic_publish(exchange='',
                             routing_key='validation_message',
                             body=data)
       count += 1

channel.basic_consume(callback,
                      queue='op_return_hashes',
                      no_ack=True)
print("Waiting for tasks")

channel.start_consuming()
