# Given an incoming trajectory:
# Cut it into two pieces: check, confirm
# Check "check" against rule antecedents, get best fit (or show "missing")
# if not missing, see if "confirm" was right

# To do this, we will need to cut the patterns into two pieces. Training and Testing.
# First try: quarters. 1335 training 445 testing

# First try: divide test line in half. First half looks for antecedent

# Parse a line into the antecedent, list of strings

import math
import sys
import time
from apriori_utils import *

def getAttributes(ruleLine):
  ruleLine = ruleLine.replace(" ", "")
  confParsed = ruleLine.split(":")

  confidence = float(confParsed[1])

  ruleParsed = confParsed[0].split("=>")

  antecedent = strToArray(ruleParsed[0])
  consequent = strToArray(ruleParsed[1])

  return antecedent, consequent, confidence

def getMatchingLen(antecedent, checkRegions):
  # We have antecedent A1 A2 ... An
  # and regions R1 R1 ... Rm
  # What is the longest sequence of A's present in R's?
  # Note that the sequence has to be ordered too
  maxLen = 0
  i = 0
  j = 0

  while i < len(checkRegions):
    currLen = 0
    currItem = checkRegions[i]
    if currItem in antecedent:
      index = antecedent.index(currItem)
      j = i

      while j < len(checkRegions) and index < len(antecedent) and checkRegions[j] == antecedent[index]:
        j += 1
        index += 1
        currLen += 1

    if currLen > maxLen:
      maxLen = currLen
    i += 1

  return maxLen

def strToArray(arrayString): # Some hacky parsing
  return arrayString.replace("'", "").replace("[", "").replace("]", "").split(",")


with open(sys.argv[1], 'r') as test_vectors, open(sys.argv[2], 'r') as rules:
  correctCount = 0
  totalCount = 0
  for line in test_vectors:
    regions = [str(region) for region in gatherDedupedRegionList(line)]

    # Now see the rules
    checkRegions = regions[:len(regions)/2]
    confirmRegions = regions[len(regions)/2:]

    bestRuleScore = 0

    for rule in rules:
      antecedent, consequent, confidence = getAttributes(rule)
      
      # We have antecedent, consequent, confidence, checkRegions, confirmRegions
      # First: See if any part of antecedent appears in checkRegions

      # Get largest congruent subsequence, that is matching len
      matchingLen = getMatchingLen(antecedent, checkRegions)
      if matchingLen > 0:

        ruleScore = confidence * (1 - math.exp( matchingLen*-1 ) )
        if ruleScore > bestRuleScore:
          bestRuleScore = ruleScore
          bestRuleConsequent = consequent
          bestRuleAntecedent = antecedent

        # Given matching len and confidence of rule, determine rule fit based on fitness function

      # Right now we are answering the question 
      #"Is a rule antecedent anywhere in this regionlist?"

      # Next we have to answer:
      # What is the best rule fit to this regionCheck?
      # We need to figure out matching length and use rule confidence
    rules.seek(0)
    if bestRuleScore > 0:
      print "The best-fit rule had a score of %d and its consequent is:" % bestRuleScore
      print bestRuleConsequent
      print "The actual final regions of the current trajectory is"
      print confirmRegions
      matchLen = getMatchingLen(bestRuleConsequent, confirmRegions)
      print "The rule prediction had a matching length of %d." % matchLen
      if matchLen != 0:
        print "The prediction was correct (At least in terms of current analysis)"
        correctCount += 1
      else:
        print "The prediction was incorrect (At least in terms of current analysis)"
      totalCount += 1

  correctRatio = float(correctCount) / float(totalCount)
  print "Correct to incorrect ratio was %f. This does not consider trajectories with no matching rule" % correctRatio
   # else:
   #   print "Could not find unmodified matching rule"