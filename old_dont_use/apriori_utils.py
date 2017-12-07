LATITUDE_DIVISIONS = 11
LONGITUDE_DIVISIONS = 18

LAT_MAX_DEGREES = 50.0
LAT_MIN_DEGREES = 0.0
LONG_MAX_DEGREES = 100.0
LONG_MIN_DEGREES = 20.0

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

  # Latitude is counted as degrees N/S of equator => y coords
  # Longitude is counted as degrees W/E of meridian => x coords

  lat_interval = (LAT_MAX_DEGREES - LAT_MIN_DEGREES) / LATITUDE_DIVISIONS
  long_interval = (LONG_MAX_DEGREES - LONG_MIN_DEGREES) / LONGITUDE_DIVISIONS

  lat_region = int( (coordinate[0] - LAT_MIN_DEGREES) / lat_interval)
  # long coords are negative, and go from [100 - 20], so have to reverse
  long_region = LONGITUDE_DIVISIONS - int( (-coordinate[1] - LONG_MIN_DEGREES) / long_interval)

  # TODO: remove this once we have bounds checking for data
  if lat_region < 0 or lat_region > LATITUDE_DIVISIONS:
    # TODO: it's out of our bounds, for now remove it
    lat_region = -1
  if long_region < 0 or long_region > LONGITUDE_DIVISIONS:
    # TODO: it's out of our bounds, for now remove it
    long_region = -1

  return long_region * LONGITUDE_DIVISIONS + lat_region

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

def safe_increment(table, key, value=1):
  try:
    table[key] += value
  except KeyError:
    table[key] = value