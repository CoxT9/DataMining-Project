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

def regionalize(coordinate):

  REGION_DIMENSION = 20
  x_interval = 73.8/REGION_DIMENSION
  y_interval = 172.5/REGION_DIMENSION

  x_region = int(coordinate[0] / x_interval)
  y_region = int(coordinate[1] / y_interval)

  if coordinate[0] % x_interval == 0:
    x_region -= 1

  if coordinate[1] % y_interval == 0:
    y_region -= 1

  return x_region*REGION_DIMENSION + y_region

def gatherDedupedRegionList(ruleLine):
  coordinates = gatherCoordinateList(ruleLine)
  regionList = [regionalize(coord) for coord in coordinates]

  dedupedRegions = []
  dedupedRegions.append(regionList[0])

  foundItem = regionList[0]
  i = 0

  while i < len(regionList):
    if regionList[i] != foundItem:
      foundItem = regionList[i]
      dedupedRegions.append(regionList[i])
    i += 1

  return dedupedRegions

def safe_increment(table, key, value=1):
  try:
    table[key] += value
  except KeyError:
    table[key] = value