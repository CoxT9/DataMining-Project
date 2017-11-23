# Another quick n dirty python script to generate association rules given a list of frequent itemsets
# It is assumed that each line in the file is of the form (IS) : Supp
# Where IS is a ", " delimited series of numbers, which correspond to regions
# Don't look at singletons, they cannot produce rules

import sys
import time
import re

MIN_CONF = 0.25

def getRawRules(itemset):
  divider = len(itemset) - 1
  rules = [] # Antecedent, Consequent pairs
  while divider > 0:
    antecedent = itemset[0:divider]
    consequent = itemset[divider:]
    rules.append( (antecedent, consequent) )
    divider -= 1

  return rules

def convertToSearchLine(antecedentArray):
  if len(antecedentArray) == 1:
    line = antecedentArray[0]
  else:
    line = "(" + ", ".join(map(str, antecedentArray)) + ")"

  # Will have to change this to parse strings correctly
  return str(line).replace("'", "")

def getAntecedentSupport(itemsetsFile, searchLine):
  with open(itemsetsFile, "r") as itemsets:
    for line in itemsets:
      contents = line.split(":")
      if contents[0].strip() == searchLine:
        result = int(contents[1].strip())

  return result

def generateRules(itemsetsFile, currItemsetLine): # String line of form (t, t, t) : s
  generatedRules = []

  currItemsetLine = currItemsetLine.replace(" ", "")
  currItemsetParsed = currItemsetLine.split(":")

  currItemsetSupport = int(currItemsetParsed[1])

  # Change this to list of tuples
  currItemset = convertToTupleList(currItemsetParsed[0])
  # Now we have the full itemset, and its support
  # These are ordered rules, so we grow the antecedent and shrink the consequent together
  # ABC, AB>C, A>BC
  rulePartitions = getRawRules(currItemset)

  # To find confidence, we need support of antecedent
  for rule in rulePartitions:
    searchLine = convertToSearchLine(rule[0])
    # Do a search in the file for the corresponding frequent itemset, and get its support
    # That gives the confidence of the rule to be inserted
    antecedentSupport = getAntecedentSupport(itemsetsFile, searchLine)

    conf = float(currItemsetSupport) / float(antecedentSupport)
    if conf >= MIN_CONF:
      generatedRules.append( (rule[0], rule[1], conf) )

  return generatedRules

def convertToTupleList(line):
  # turn the raw string into a list of lat,lon tuples
  # Str is ( (x, y), x2, y2), ... )
  tupleList = []
  line = line[1:len(line)-1] # Drop outer brackets

  # now line is (x, y), (x2, y2) ...
  rawTuples = re.findall("\([0-9-,]+\)" , line)
  for rawTuple in rawTuples:
    parsedLeftTuple, parsedRightTuple = rawTuple[1:len(rawTuple)-1].split(",")
    tupleList.append( (parsedLeftTuple, parsedRightTuple) )

  return tupleList
  

def createRulesFile():
  totalRules = 0
  with open(sys.argv[1], 'r') as itemsets, open(sys.argv[2], 'w') as rules:
    for line in itemsets:

      if line[1] == "(": # Multi tuple pattern
        currRules = generateRules(sys.argv[1], line)
        totalRules += len(currRules)
        for rule in currRules:
          rules.write(
            str((rule[0])) + 
            " => " + 
            str((rule[1])) + 
            " : " + 
            str(round(rule[2], 2)) +
            "\n"
          )

  print "Total rules generated:", totalRules

def main():
  if len(sys.argv) != 3:
    print "Usage: {0} <PatternsInput> <RulesOutput>".format(sys.argv[0])
  else:
    createRulesFile()

if __name__ == '__main__':
  main()
else:
  print __name__