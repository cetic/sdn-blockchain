import hashlib
import OP_RETURN

file=open("secure_logs.txt","r")

lines=file.readlines()
term = "Checkpoint"
with open('checkpoint_hashes.txt',"r+b") as f1:
  for line in lines:
    entry = str(line)
    if term in entry:
      checkpoint_hash = hashlib.sha256(entry).hexdigest()
      f1.write(str(checkpoint_hash) +'\n')
