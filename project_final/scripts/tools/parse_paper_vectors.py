import sys

YEAR_INDEX = 0
NUM_INDEX = 4

LAT_INDEX = 6
LON_INDEX = 7

def parseHurricanes():
  with open(sys.argv[1], 'r') as inputFile, open(sys.argv[2], 'w') as outputFile:
    currentId = ""
    currentVector = []

    for line in inputFile.readlines()[1:]:
      lineSplit = line.split(" ")
      lineId = lineSplit[YEAR_INDEX] + lineSplit[NUM_INDEX]

      if lineId != currentId: # New ID!
        outputFile.write(currentId+" ")
        for item in currentVector:
          outputFile.write(item)
        outputFile.write("\n")

        currentVector = [] # Print or not, move onto next ID/coordinates
        currentId = lineId

      outStr = "(" + lineSplit[LAT_INDEX] + ":" + lineSplit[LON_INDEX] + "),"
      currentVector.append(outStr)

def main():
  if len(sys.argv) != 3:
    print "Usage: {0} <StormsCsvInput> <VectorsOutput>".format(sys.argv[0])
  else:
    parseHurricanes()

if __name__ == '__main__':
  main()
else:
  print __name__