# A simple python script to find frequent trajectories
# First: take in vectors, for each coordinate, regionalize - find frequent 1-size regions

import sys
import itertools
import time

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
MIN_SUP = 90
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


def safe_increment(table, key, value=1):
  try:
    table[key] += value
  except KeyError:
    table[key] = value

def gather_new_frequent_items(resultTable, frequent_k_itemsets):
  final_itemsets.append({})
  for key in frequent_k_itemsets:
    if frequent_k_itemsets[key] >= MIN_SUP:
      final_itemsets[-1][key] = frequent_k_itemsets[key] 

def timeseries_candidate_generation(frequent_k_itemsets):
  # We have our L_k, use suffix-prefix to get C_k+1
  x = sorted(frequent_k_itemsets, key=lambda k: (k[1], k[0]))
  for item in x:
    print item
  return []

with open(sys.argv[1], 'r') as vectors, open(sys.argv[2], 'w') as patterns:
  level = 1
  candidate_itemsets = [] # Store C_k before pruning/reading
  final_itemsets = [] # For each level, dict of itemsets

  while level == 1 or len(candidate_itemsets) >= level+1:
    freqs = {}
    # On each level, do the following:
    # - candidate generation
    # - prune
    # - actually scan
    print "Level %d" % level
    if level == 1: # level 1, just build singletons with basic scan
      for line in vectors:
        coords = gatherCoordinateList(line)
        for co in coords:
          region = regionalize(co)
          safe_increment(freqs, region)

      # we have all the singletons. Gather the frequent ones
      gather_new_frequent_items(final_itemsets, freqs)

      # generate candidates for next level here. Cand generation is a little different for first round
      candidate_itemsets = list(itertools.permutations(final_itemsets[0], 2))
      print len(final_itemsets[-1].keys())
      level += 1

    else: # cand gen/prune
      # we are given C_k, prune, read table, add L_k+1 to final result, generate C_k+1, incr level

      # if we are past level 2, we can prune the candidate list
      if level != 2:
        print "prune..."

      for line in vectors:
        coords = gatherCoordinateList(line)
        regions = [regionalize(co) for co in coords]
        # update counts of candidates we find
        for cand in candidate_itemsets:
          if set(cand).issubset(regions):
            safe_increment(freqs, cand)

      gather_new_frequent_items(final_itemsets, freqs)
      print len(final_itemsets[-1].keys())
      level += 1
      # use freqs 

      # use prefix-suffix to generate C_k+1 (next level will do the pruning)
      candidate_itemsets = timeseries_candidate_generation(final_itemsets[-1].keys())

    vectors.seek(0)



