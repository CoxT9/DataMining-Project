# Another quick n dirty python script to generate association rules given a list of frequent itemsets
# It is assumed that each line in the file is of the form (IS) : Supp
# Where IS is a ", " delimited series of numbers, which correspond to regions
# Don't look at singletons, they cannot produce rules

import sys

def getRawRules(itemset):
  divider = len(itemset) - 1
  rules = [] # Antecedent, Consequent pairs
  while divider > 0:
    antecedent = itemset[0:divider]
    consequent = itemset[divider:]
    print antecedent
    print consequent
    rules.append( (antecedent, consequent) )
    divider -= 1

  return rules

def convertToSearchLine(antecedentArray):
  if len(antecedentArray) == 1:
    line = antecedentArray[0]
  else:
    line = "(" + ", ".join(map(str, antecedentArray)) + ")"

  return line

def generateRules(itemsetsFile, currItemsetLine): # String line of form (t, t, t) : s
  generatedRules = []

  currItemsetLine = currItemsetLine.replace(" ", "")
  currItemsetParsed = currItemsetLine.split(":")

  currItemsetSupport = int(currItemsetParsed[1])

  currItemset = currItemsetParsed[0].replace("(", "").replace(")", "").split(",")
  
  # Now we have the full itemset, and its support
  # These are ordered rules, so we grow the antecedent and shrink the consequent together
  # ABC, AB>C, A>BC
  rulePartitions = getRawRules(currItemset)

  # To find confidence, we need support of antecedent
  for rule in rulePartitions:
    searchLine = convertToSearchLine(rule[0])
    # Do a search in the file for the corresponding frequent itemset, and get its support
    # That gives the confidence of the rule to be inserted

with open(sys.argv[1], 'r') as itemsets, open(sys.argv[2], 'w') as rules:
  for line in itemsets:
    if line[0] == "(":
      print generateRules(itemsets, line)
      break