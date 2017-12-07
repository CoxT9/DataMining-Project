
from apriori_utils import *
import sys
import itertools
import time

WEIGHT_INTERVAL_NOMINAL = 756
WEIGHT_INTERVAL_YEAR = 50
HURRICANE_ID_PLACEHOLDER = "AL015555"
WEIGHT_SCALE = 2.5
# For weighted data:
# Data can be weighted nominally or year-over-year
# Careful! Right now these values are dependent on the specific training data input. This must be fixed
# A good minsupport value for weight training data appears to be 10. Minconf can stay the same

def gather_new_frequent_items(resultTable, frequent_k_itemsets, minsup):
  resultTable.append({})
  for key in frequent_k_itemsets:
    if frequent_k_itemsets[key] >= minsup:
      resultTable[-1][key] = frequent_k_itemsets[key] 

def timeseries_candidate_generation(frequent_k_itemsets, chunk_size):
  # this is the candidate generation and pruning
  # We have our L_k, use suffix-prefix to get C_k+1

  frequent_k_itemsets_dict = { tuple(item):None for item in frequent_k_itemsets }
  candidates = []
  for curr_index, curr_item in enumerate(frequent_k_itemsets):

    compare_index = 0
    found = False
    leftChunk = curr_item[(chunk_size*-1):]

    while compare_index < len(frequent_k_itemsets) and not found:
      found = leftChunk == frequent_k_itemsets[compare_index][:chunk_size]
      if not found:
        compare_index += 1

    while compare_index < len(frequent_k_itemsets) and leftChunk == frequent_k_itemsets[compare_index][:chunk_size]:
      new_candidate = join_entries(curr_item, frequent_k_itemsets[compare_index], chunk_size)
      required_itemset_checks = itertools.combinations(new_candidate, chunk_size+1)

      if all(item == curr_item or item == frequent_k_itemsets[compare_index] or tuple(item) in frequent_k_itemsets_dict for item in required_itemset_checks):
        candidates.append(new_candidate)
      compare_index += 1

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

def init_support_weight(weightedData, weightedNominal):
  w = 1.0
  if weightedData:
    if weightedNominal:
      w = WEIGHT_SCALE / WEIGHT_INTERVAL_NOMINAL
    else:
      w = WEIGHT_SCALE / WEIGHT_INTERVAL_YEAR

  return w

def check_weight_update(weightedNominal, w, currId, iterId):
  newId = currId
  newW = w
  if weightedNominal:
    newW = min(w + (WEIGHT_SCALE / WEIGHT_INTERVAL_NOMINAL), 2.5)
  elif currId[-4:] != iterId[-4:]:
    newW = min(w + (WEIGHT_SCALE / WEIGHT_INTERVAL_YEAR), 2.5)
    newId = iterId

  return newW, newId

def execute_apriori():
  totalPatterns = 0
  minimumsupport = float( sys.argv[3] )
  weightedData  = bool( int( sys.argv[4] ) )
  weightedNominal = bool( int( sys.argv[5] ) )

  with open(sys.argv[1], 'r') as vectors_file:
    vectors = []
    for line in vectors_file:
      vectors.append( (line.split(" ")[0], gatherDedupedRegionList(line)) )

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

      w = init_support_weight(weightedData, weightedNominal)
      currId = HURRICANE_ID_PLACEHOLDER

      for _id, regions in vectors:
        for region in regions:
          safe_increment(freqs, region, w)

        if weightedData:
          w, currId = check_weight_update(weightedNominal, w, currId, _id)

      # we have all the singletons. Gather the frequent ones
      gather_new_frequent_items(final_itemsets, freqs, minimumsupport)

      # generate candidates for next level here. Cand generation is a little different for first round
      candidate_itemsets = list(itertools.permutations(final_itemsets[0], 2))
      print len(final_itemsets[-1].keys()), "Number of Frequent k itemsets"
      totalPatterns += len(final_itemsets[-1].keys())
      level += 1

    else: # cand gen/prune
      # scan
      # we are given C_k, , read table, add L_k to final result, generate/prune C_k+1, incr level
      # may want to optimize this too. faster search needed
      # gonna have to eat this one. no faster way it seems
      w = init_support_weight(weightedData, weightedNominal)
      currId = HURRICANE_ID_PLACEHOLDER

      currId = "AL025555"
      for _id, regions in vectors:
        # update counts of candidates we find
        for cand in candidate_itemsets:
          # for all cands where regions issuperset cand, incr cand
          # here's how: make itertools permute deduped regions. compare each against cand. if match, add.
          candSet = set(cand)
          if candSet.issubset(regions):
            safe_increment(freqs, cand, w)

        if weightedData:
          w, currId = check_weight_update(weightedNominal, w, currId, _id)

      gather_new_frequent_items(final_itemsets, freqs, minimumsupport)
      print len(final_itemsets[-1].keys()), "Number of Frequent k itemsets"
      totalPatterns += len(final_itemsets[-1].keys())
      # use prefix-suffix to generate and prune C_k+1 (next level will do the pruning)
      candidate_itemsets = timeseries_candidate_generation(sorted(final_itemsets[-1]), level-1)
      print len(candidate_itemsets), "Number of level k+1 Candidates"
      level += 1

  print "Total Frequent Patterns: %d" % totalPatterns
  with open(sys.argv[2], 'w') as patterns:
    for level in final_itemsets:
      for itemset in level:
        patterns.write(str(itemset) + " : " + str(level[itemset]) + "\n")

def main():
  if len(sys.argv) != 6:
    # Weight change every year: 0
    # Weight change every index: 1
    print "Usage: {0} <VectorsInput> <PatternsOutput> <MinSupport> <Weighted0/1> <WeightedYearOrNominal0/1>".format(sys.argv[0])
  else:
    execute_apriori()

if __name__ == '__main__':
  main()
else:
  print __name__