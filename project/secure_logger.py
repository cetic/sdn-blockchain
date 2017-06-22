import base64, M2Crypto
import hmac
import hashlib
import rsa
import sys
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import os

# Generate Random Session ID
def generate_session_id(num_bytes = 16):
    return get_random_bytes(num_bytes)

#Calculate First Line Hash
def first_line_hash(session_id, log_text):
    digest_maker = hmac.new(session_id, log_text, hashlib.sha1)
    return digest_maker.hexdigest()

#Calculate Remaining Lines Hashes
def line_hash(session_id, previous_hash, log_text):
    digest_maker = hmac.new(session_id, previous_hash + log_text, hashlib.sha1)
    return digest_maker.hexdigest()

#Calculate Checkpoint Hash
def checkpoint_line_hash(new_session_id, old_session_id, previous_hash, log_text):
    digest_maker = hmac.new(new_session_id, old_session_id + previous_hash + log_text, hashlib.sha1)
    return digest_maker.hexdigest()

secret = os.urandom(16)
aes_key = AES.new(os.urandom(32), AES.MODE_CTR, counter=lambda: secret)
random_generator = Random.new().read
rsa_key = RSA.generate(1024, random_generator)
cipher = PKCS1_OAEP.new(rsa_key.publickey())
#Checkpoint Signature Generator
def generate_checkpoint_signature(previous_hash, current_hash, old_session_id, new_session_id, count, s):
    s = 'Checkpoint number '
    code = cipher.encrypt(new_session_id)
    md_signature = hashlib.md5(previous_hash + old_session_id + str(code) +  current_hash + s + str(count))
    return md_signature.hexdigest()

file=open("tacker_test.txt","r")

lines=file.readlines()

session_id = generate_session_id(num_bytes = 16)
checkpoint_count = 1
with open('secure_logs.txt',"r+b") as f1:
    for line in lines:
      line_count = (lines.index(line)+1)%50
      if line_count == 1:
        hash = first_line_hash(session_id, line.rstrip('\n'))
        f1.write(line.rstrip('\n') + ', this line hash is: ' + hash + '\n')
      else:
        if line_count == 0:
          old_hash = line_hash(session_id, hash, line.rstrip('\n'))
          f1.write(line.rstrip('\n') + ', this line hash is: ' + old_hash + '\n')
          old_session_id =  session_id
          session_id = generate_session_id(num_bytes = 16)
          hash = line_hash(session_id, old_hash, 'Checkpoint number ' + str(checkpoint_count))
          checkpoint_signature = generate_checkpoint_signature(old_hash, hash, old_session_id, session_id, str(checkpoint_count), ' Checkpoint number ')
          f1.write('Checkpoint number ' + str(checkpoint_count) + ' Previous session id is ' + base64.b64encode(str(old_session_id)) + ' Encrypted new session id is ' + base64.b64encode(cipher.encrypt(session_id)) + ' Checkpoint signature is ' + str(checkpoint_signature) + ' Previous entry hash is ' + str(old_hash) + ' Checkpoint entry hash is ' + str(hash) +  '\n') 
          checkpoint_count += 1
        hash = line_hash(session_id, hash, line.rstrip('\n'))
        f1.write(line.rstrip('\n') + ', this line hash is: ' + hash + '\n')

