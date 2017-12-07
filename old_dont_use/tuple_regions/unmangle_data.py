import sys

with open(sys.argv[1], 'r') as inFile, open(sys.argv[2], 'w') as outFile:
  for line in inFile:
    for word in line.split(" "):
      if len(word) > 0:
        outFile.write(word+' ')

