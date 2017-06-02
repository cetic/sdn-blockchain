import base64, M2Crypto
import hmac
import hashlib
import rsa
import sys
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import os

# Generate Random Session ID
def generate_session_id(num_bytes = 16):
    return base64.b64encode(M2Crypto.m2.rand_bytes(num_bytes))

#Calculate First Line Hash
def first_line_hash(session_number, log_text):
    digest_maker = hmac.new(session_number, log_text, hashlib.sha1)
    return digest_maker.hexdigest()

#Calculate Remaining Lines Hashes
def line_hash(session_number, previous_hash, log_text):
    digest_maker = hmac.new(session_number, previous_hash + log_text, hashlib.sha1)
    return digest_maker.hexdigest()

#Calculate Checkpoint Hash
def checkpoint_line_hash(new_session_number, old_session_number, previous_hash, log_text):
    digest_maker = hmac.new(new_session_number, old_session_number + previous_hash + log_text, hashlib.sha1)
    return digest_maker.hexdigest()

secret = os.urandom(16)
aes_key = AES.new(os.urandom(32), AES.MODE_CTR, counter=lambda: secret)

#Checkpoint Signature Generator
def generate_checkpoint_signature(previous_hash, current_hash, old_session_number, new_session_number, count, s):
    s = 'this is checkpoint number '
    code = aes_key.encrypt(new_session_number)
    md_signature = hashlib.md5(previous_hash + old_session_number + str(code) +  current_hash + s + str(count))
    return md_signature.hexdigest()

file=open("tacker_test.txt","r")

lines=file.readlines()

session_number = generate_session_id(num_bytes = 16)
checkpoint_count = 1
with open('secure_logs.txt',"r+b") as f1:
    for line in lines:
      line_count = (lines.index(line)+1)%50
      if line_count == 1:
        hash = first_line_hash(session_number, line.rstrip('\n'))
        f1.write(line.rstrip('\n') + ', this line hash is: ' + hash + '\n')
      else:
        if line_count == 0:
          old_hash = line_hash(session_number, hash, line.rstrip('\n'))
          f1.write(line.rstrip('\n') + ', this line hash is: ' + old_hash + '\n')
          old_session_number =  session_number
          session_number = generate_session_id(num_bytes = 16)
          hash = line_hash(session_number, old_hash, 'This is checkpoint number ' + str(checkpoint_count))
          checkpoint_signature = generate_checkpoint_signature(old_hash, hash, old_session_number, session_number, str(checkpoint_count), 'this is checkpt number ')
          f1.write('this is checkpoint number ' + str(checkpoint_count) + ' previous session number is ' + str(old_session_number) + ' encrypted new session number is ' + aes_key.encrypt(session_number) $
          checkpoint_count += 1
        hash = line_hash(session_number, hash, line.rstrip('\n'))
        f1.write(line.rstrip('\n') + ', this line hash is: ' + hash + '\n')



