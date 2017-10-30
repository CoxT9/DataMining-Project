def gatherCoordinateList(inputStr):
  parseStr = inputStr.split(' ')[1]
  if parseStr[-1] == ',':
    parseStr = parseStr[:-1]

  result = []
  parseStr = parseStr.strip()

  for vecStr in parseStr.split(','):
    if len(vecStr):
      currVec = vecStr.replace('(', '').replace(')', '').split(':')
      result.append( (float(currVec[0]), float(currVec[1])) )

  return result



import sys

minX = 1000000000
minY = 1000000000

maxX = 0
maxY = 0

with open(sys.argv[1], 'r') as vectors:
  for line in vectors:
    coords = gatherCoordinateList(line)
    for co in coords:
      if co[0] < minX:
        minX = co[0]

      if co[0] > maxX:
        maxX = co[0]

      if co[1] < minY:
        minY = co[1]

      if co[1] > maxY:
        maxY = co[1]

print minX, maxX, minY, maxY
print maxX - minX, maxY - minY
