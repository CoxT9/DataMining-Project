
LATITUDE_DIVISIONS = 11
LONGITUDE_DIVISIONS = 18

LAT_MAX_DEGREES = 50.0
LAT_MIN_DEGREES = 0.0
LONG_MAX_DEGREES = 100.0
LONG_MIN_DEGREES = 20.0

DIMENSIONS_LATITUDE = 5
DIMENSIONS_LONGTITUDE = 5

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

  # lat, N/S, y, 0
  # lon, W/E, x, 1 (negative)
  # Latitude is counted as degrees N/S of equator => y coords
  # Longitude is counted as degrees W/E of meridian => x coords

  # may need region pruning here

  return (int(coordinate[0]/DIMENSIONS_LATITUDE), int(coordinate[1]/DIMENSIONS_LONGTITUDE))

def gatherDedupedRegionList(ruleLine):
  coordinates = gatherCoordinateList(ruleLine)
  regionList = [regionalize(coord) for coord in coordinates]

  dedupedRegions = []
  # TODO: change this once we have bounds checking for data
  i = 0
  while i < len(regionList) and regionList[i] < 0:
    i += 1
  dedupedRegions.append(regionList[i])
  foundItem = regionList[i]

  while i < len(regionList):
    if regionList[i] != foundItem and regionList[i] >= 0:
      foundItem = regionList[i]
      dedupedRegions.append(regionList[i])
    i += 1

  return dedupedRegions

def safe_increment(table, key, value=1.0):
  try:
    table[key] += value
  except KeyError:
    table[key] = value