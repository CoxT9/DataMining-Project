# Given an incoming trajectory:
# Cut it into two pieces: check, confirm
# Check "check" against rule antecedents, get best fit (or show "missing")
# if not missing, see if "confirm" was right

# To do this, we will need to cut the patterns into two pieces. Training and Testing.
# First try: quarters. 1335 training 445 testing

# First try: divide test line in half. First half looks for antecedent

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

# Parse a line into the antecedent, list of strings
def getAttributes(ruleLine):
  ruleLine = ruleLine.replace(" ", "")
  confParsed = ruleLine.split(":")

  confidence = float(confParsed[1])

  ruleParsed = confParsed[0].split("=>")

  antecedent = strToArray(ruleParsed[0])
  consequent = strToArray(ruleParsed[1])

  return antecedent, consequent, confidence

def strToArray(arrayString): # Some hacky parsing
  return arrayString.replace("'", "").replace("[", "").replace("]", "").split(",")

import sys
from apriori_utils import *

with open(sys.argv[1], 'r') as test_vectors, open(sys.argv[2], 'r') as rules:
  for line in test_vectors:
    regions = [str(region) for region in gatherDedupedRegionList(line)]

    # Now see the rules
    checkRegions = regions[:len(regions)/2]
    confirmRegions = regions[len(regions)/2:]

    for rule in rules:
      antecedent, consequent, confidence = getAttributes(rule)
      
      # We have antecedent, consequent, confidence, checkRegions, confirmRegions
      # First: See if any part of antecedent appears in checkRegions

      # There is an interesting thing to consider here:
      # Region has ABC but antecedent is AC. What is the matching len? 1 or 2?
      antecedentLen = len(set(antecedent))
      diffLen = len( set(antecedent) - set(checkRegions) )
      if diffLen < antecedentLen:
        print checkRegions
        print antecedent

      # Right now we are answering the question 
      #"Is a rule antecedent anywhere in this regionlist?"

      # Next we have to answer:
      # What is the best rule fit to this regionCheck?
      # We need to figure out matching length and use rule confidence
