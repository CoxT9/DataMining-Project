
from apriori_utils import *
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

# tuple regions are started but there is more work to do. First make sure multi-tuple-arrays are working correctly
"""
MIN_SUP = 3

# region and safe_incr code moved to util file

def gather_new_frequent_items(resultTable, frequent_k_itemsets):
  print "go"
  resultTable.append({})
  for key in frequent_k_itemsets:
    if frequent_k_itemsets[key] >= MIN_SUP:
      resultTable[-1][key] = frequent_k_itemsets[key] 
  print "done--"

def timeseries_candidate_generation(frequent_k_itemsets, chunk_size):
  # this is the candidate generation and pruning

  # looks like this is the bottleneck right now (at least it's the worst one)
  # need to reduce the search space. Should be able to search only a specific subset of the candidate entries (see lecture slides)
  # We have our L_k, use suffix-prefix to get C_k+1

  # how to speed this way up
  # take advantage of the fact that the data is sorted now

  candidates = []
  for curr_index, curr_item in enumerate(frequent_k_itemsets):
    print curr_index

    compare_index = 0
    found = False
    leftChunk = curr_item[(chunk_size*-1):]
    #print "slower1?"
    while compare_index < len(frequent_k_itemsets) and not found:
      found = leftChunk == frequent_k_itemsets[compare_index][:chunk_size]
      if not found:
        compare_index += 1

    #print "slower2?"
    while compare_index < len(frequent_k_itemsets) and leftChunk == frequent_k_itemsets[compare_index][:chunk_size]:
      new_candidate = join_entries(curr_item, frequent_k_itemsets[compare_index], chunk_size)
      required_itemset_checks = itertools.combinations(new_candidate, chunk_size+1)

      #print "slower3?"
      if all(item == curr_item or item == frequent_k_itemsets[compare_index] or item in frequent_k_itemsets for item in required_itemset_checks):
        candidates.append(new_candidate)
      compare_index += 1
    print "out"
    # read my lips: no new comparisons!

  # candidates = []
  # for curr_index, curr in enumerate(frequent_k_itemsets):
  #   print curr_index
  #   for compare_index, compare in enumerate(frequent_k_itemsets):

  #     # if last chunk size of item equal to first chunksize of item2, add to cands
  #     # cant use key based search because we are comparing array slices
  #     if curr_index != compare_index and curr[(chunk_size*-1):] == compare[:chunk_size]:
  #       # we found a possible candidate but we need to do a prune check using frequent_k_itemsets
  #       new_candidate = join_entries(curr, compare, chunk_size)
  #       required_itemset_checks = itertools.combinations(new_candidate, chunk_size+1)
  #       # key based search helps here
  #       if all(item == curr or item == compare or item in frequent_k_itemsets for item in required_itemset_checks):
  #         candidates.append(new_candidate)

  return candidates

def join_entries(left, right, chunk_size):
  result = left + right[chunk_size:]
  return result

def gather_sublists(region_list):
  result = []
  for size in range(1, len(region_list)):
    for index in range(len(region_list)):
      result.append(region_list[index : index + size])

  return result

def execute_apriori():
  with open(sys.argv[1], 'r') as vectors_file:
    vectors = []
    for line in vectors_file:
      vectors.append(gatherDedupedRegionList(line))

  level = 1
  candidate_itemsets = {} # Store C_k before pruning/reading
  final_itemsets = [] # For each level, dict of itemsets

  while level == 1 or len(candidate_itemsets) >= level+1:
    freqs = {}
    # On each level, do the following:
    # - candidate generation
    # - prune
    # - actually scan
    print "Level %d" % level
    if level == 1: # level 1, just build singletons with basic scan
      for regions in vectors:
        for region in regions:
          safe_increment(freqs, region)

      # we have all the singletons. Gather the frequent ones
      gather_new_frequent_items(final_itemsets, freqs)

      # generate candidates for next level here. Cand generation is a little different for first round
      candidate_itemsets = list(itertools.permutations(final_itemsets[0], 2))
      print len(final_itemsets[-1].keys()), "Number of Frequent k itemsets"
      level += 1

    else: # cand gen/prune
      # we are given C_k, , read table, add L_k to final result, generate/prune C_k+1, incr level
      # may want to optimize this too. faster search needed
      # gonna have to eat this one. no faster way it seems
      for regions in vectors:
        # update counts of candidates we find
        for cand in candidate_itemsets:
          # for all cands where regions issuperset cand, incr cand
          # here's how: make itertools permute deduped regions. compare each against cand. if match, add.
          candSet = set(cand)
          if candSet.issubset(regions):
            safe_increment(freqs, cand)

      gather_new_frequent_items(final_itemsets, freqs)
      print len(final_itemsets[-1].keys()), "Number of Frequent k itemsets"
      # use prefix-suffix to generate and prune C_k+1 (next level will do the pruning)
      candidate_itemsets = timeseries_candidate_generation(sorted(final_itemsets[-1]), level-1)
      print len(candidate_itemsets), "Number of level k+1 Candidates"
      level += 1

  with open(sys.argv[2], 'w') as patterns:
    for level in final_itemsets:
      for itemset in level:
        patterns.write(str(itemset) + " : " + str(level[itemset]) + "\n")

def main():
  if len(sys.argv) != 3:
    print "Usage: {0} <VectorsInput> <PatternsOutput>".format(sys.argv[0])
  else:
    execute_apriori()

if __name__ == '__main__':
  main()
else:
  print __name__