# A simple python script to find frequent trajectories
# First: take in vectors, for each coordinate, regionalize - find frequent 1-size regions

import sys

# Need to dedupe raw vectors

# For regionalization, need to represent vectors as a scalar and modulo by their bucket
# How to make vector into a scalar? Norm of vector? Eigenvalue?

# Some of the data entries are impossible (latitude cannot exceed 180. BTW the negative indicates west)

# From some analysis, height is from 7.2->81.0, width from -109.5->63. 73.8 H-H, 172.5 W-W

# As a first pass on regionalization, consider the following:
""" Suppose we want to group the map into a 10x10 grid
The question becomes "what sector does my x,y belong to"
answer:
73.8 / 10 -> 7.38. So take candidate x / 7.38, truncate to int, that's the x-region. If on the line (modulo = 0), take -1
ditto for y.
result: x*10 + y = region #


"""
REGION_DIMENSION = 20
MIN_SUP = 500
x_interval = 73.8/REGION_DIMENSION
y_interval = 172.5/REGION_DIMENSION

# Should be careful though. Regionalization is not the same as assigning buckets

# Take a string of the form ID,xy,xy,xy... and turn into vector


# Next steps:
# - Find more data
# - Implement ordered Apriori(with suffix-prefix attachment for supersets)
# - Look into fitness function for assoc rule
# - Dig into dynamic region partitioning

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

  x_region = int(coordinate[0] / x_interval)
  y_region = int(coordinate[1] / y_interval)

  if coordinate[0] % x_interval == 0:
    x_region -= 1

  if coordinate[1] % y_interval == 0:
    y_region -= 1

  return x_region*REGION_DIMENSION + y_region
freqs = {}

with open(sys.argv[1], 'r') as vectors:
  for line in vectors:
    coords = gatherCoordinateList(line)
    for co in coords:
      region = regionalize(co)
      try:
        freqs[region] += 1
      except KeyError:
        freqs[region] = 1

num_freqs = 0
for key in freqs:
  if freqs[key] >= MIN_SUP:
    print "frequent!"
    num_freqs += 1
    print key, freqs[key]

print num_freqs

print max(freqs.values())
