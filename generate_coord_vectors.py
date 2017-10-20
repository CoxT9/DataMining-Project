# A simple script to parse atlantic_storms.csv into a plaintext list of HurricaneID -> Trajectory
# Hurricanes with fewer than 3 trajectories are not included in the list, but are recorded elsewhere
import sys

with open(sys.argv[1], 'r') as inputFile, open(sys.argv[2], 'w') as outputFile, open(sys.argv[3], 'w') as prunedFile:
  currentId = ""
  currentVector = []

  for line in inputFile.readlines()[1:]:
    lineId = line.split(",")[1]
    if lineId != currentId: # New ID!
      if len(currentVector) >= 3: # Did we build enough data for this hurricane to be interesting?
        outputFile.write(currentId+" "),
        for item in currentVector:
          outputFile.write(item),
        outputFile.write("\n")
      elif len(currentId) > 0:
        prunedFile.write(currentId+"\n")

      currentVector = [] # Print or not, move onto next ID/coordinates
      currentId = lineId

    outStr = "(" + line.split(",")[6] + ":" + line.split(",")[7] + "),"
    currentVector.append(outStr)
    