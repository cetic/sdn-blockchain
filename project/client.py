import pika 
import json


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='validation_message')

def callback(ch, method, properties, body):
   validation_message = json.loads(body)
   message = validation_message['message']
   print message

channel.basic_consume(callback,
                      queue='validation_message',
                      no_ack=True)
print("Waiting for Messages")

channel.start_consuming()
