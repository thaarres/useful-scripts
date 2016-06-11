import os

wn = []

for i in range(10,41):
  wn.append(i)
  
for w in wn:
 cmd =   "qrsh -q debug.q -l hostname=t3wn%i ls /scratch/$USER" %w
 print cmd
 os.system(cmd)
 cmd = "qrsh -q debug.q -l hostname=t3wn%i find /scratch/$USER/ -user $USER -exec rm -rf {} \\;" %w
 print cmd
 os.system(cmd)