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
import re
from apriori_utils import *

EXTRAPOLATION_LIMIT = 10
EARTH_RADIUS = 6371
MAX_MINIMUM_MATCH = 5 # Max comparison length from paper

def getAttributes(ruleLine):
  ruleLine = ruleLine.replace(" ", "")
  confParsed = ruleLine.split(":")

  confidence = float(confParsed[1])

  ruleParsed = confParsed[0].split("=>")

  antecedent = strToTupleArray(ruleParsed[0])
  consequent = strToTupleArray(ruleParsed[1])

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

def strToTupleArray(arrayString):
  # May have to fix when we see tuples of size > 1
  # some code repitition here but that's alright for now
  tupleArray = []
  result = arrayString.replace("'", "").replace("[", "").replace("]", "")
  rawTuples = re.findall("\([0-9-,]+\)" , result)
  for rawTuple in rawTuples:
    leftT, rightT = rawTuple[1:len(rawTuple)-1].split(",")
    tupleArray.append( (leftT, rightT) )

  return tupleArray

def getBestRule(rules, checkRegions, flex=False):
  bestRuleScore = 0
  bestRuleConsequent = []
  bestRule = []
  for rule in rules:
    antecedent, consequent, confidence = getAttributes(rule)
    if flex:
      matchingLen = getLongestSimilarSequence(antecedent, checkRegions)
    else:
      matchingLen = getMatchingLen(antecedent, checkRegions)

    if matchingLen > 0:
      ruleScore = confidence * (1 - math.exp( matchingLen*-1 ) )
      if ruleScore > bestRuleScore:
        bestRule = antecedent
        bestRuleScore = ruleScore
        bestRuleConsequent = consequent
  rules.seek(0)
  return bestRule, bestRuleScore, bestRuleConsequent

def getLatLongDistance(startCoord, endCoord, haversine=True):
  if haversine:
    return getHaversineDistance(startCoord, endCoord)
  else:
    return getEuclideanDistance(startCoord, endCoord)

def getEuclideanDistance(startCoord, endCoord):
  # lat, N/S, y, 0
  # lon, W/E, x, 1 (negative)
  # From Wikipedia:
  # d(p, q) = sqrt( (q1-p1)**2 + (q2-p2)**2 )
  return math.sqrt( abs( endCoord[1] - startCoord[1])**2 + abs(endCoord[0] - startCoord[0])**2 )

def getHaversineDistance(startCoord, endCoord):
  # lat, N/S, y, 0
  # lon, W/E, x, 1 (negative)
  lon1, lat1, lon2, lat2 = map(math.radians, [float(startCoord[1]), float(startCoord[0]), float(endCoord[1]), float(endCoord[0])])

  # This will use the haversine formula for distance over a sphere
  distLon = lon2 - lon1
  distLat = lat2 - lat1

  alpha = math.sin(distLat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(distLon/2)**2
  delta = 2 * math.asin(math.sqrt(alpha))

  return delta * EARTH_RADIUS

def getFinalBearing(startCoord, endCoord):
  # lat, N/S, y, 0
  # lon, W/E, x, 1 (negative)

  # Determine the direction of the trajectory at termination (for extrapolation and for similar-region comparison)
  lon1, lat1, lon2, lat2 = map(math.radians, [float(startCoord[1]), float(startCoord[0]), float(endCoord[1]), float(endCoord[0])])

  distLon = lon2 - lon1

  left = math.sin(distLon) * math.cos(lat2)
  right = math.cos(lat1) * math.sin(lat2) - ( math.sin(lat1)*math.cos(lat2)*math.cos(distLon))

  init_bearing = math.degrees(math.atan2(left, right))
  compass_bearing = (init_bearing + 360) % 360 

  final_bearing = (compass_bearing + 180) % 360
  return final_bearing

def extrapolateCoordinate(startCoord, distance, bearing):
  radians_bearing = math.radians(bearing)

  lon1, lat1 = map(math.radians, [startCoord[1], startCoord[0]])

  endLatitude = math.asin(
    math.sin(lat1) *
    math.cos(distance/EARTH_RADIUS) + 
    math.cos(lat1) *
    math.sin(distance/EARTH_RADIUS) *
    math.cos(radians_bearing)
  )

  endLongtitude = lon1 + math.atan2(
    math.sin(radians_bearing) *
    math.sin(distance/EARTH_RADIUS) *
    math.cos(lat1), 

    math.cos(distance/EARTH_RADIUS) -
    math.sin(lat1) *
    math.sin(endLatitude)
  )

  endLongtitude = math.degrees(endLongtitude)
  endLatitude = math.degrees(endLatitude)
  return (endLatitude, endLongtitude)

def getExtrapolatedRegion(coordinateList, checkRegions, searchRounds, useManuscriptExtrap=True):
  lastCoordinate = coordinateList[-1]
  secondLastCoordinate = coordinateList[-2]

  if useManuscriptExtrap:
    # tp = {2latk-latk-1, 2lonk-lonk-1}
    extrapLat = (2*lastCoordinate[0]) - (secondLastCoordinate[0])
    extrapLon = (2*lastCoordinate[1]) - (secondLastCoordinate[1])
    newPoint = (extrapLat, extrapLon)
  else:
    # Take the distance and direction from SL to L coordinates
    distance = getLatLongDistance(secondLastCoordinate, lastCoordinate)
    direction = getFinalBearing(secondLastCoordinate, lastCoordinate)

    # Multiply distance by searchRounds+1 to account for level of extrapolation
    distance = distance*(searchRounds+1)
    # The coordinate from same distance and direction outward from L coordinate is the extrapolated one
    newPoint = extrapolateCoordinate(lastCoordinate, distance, direction+180)
    # Map this new coordinate to a region
  return regionalize(newPoint)

def characteristicCoordinate(discreteCoordinate):
  # Get the coordinate that would be at the center of this region
  # This may not be valid in the paper's style of regionalization
  # lat, N/S, y, 0
  # lon, W/E, x, 1 (negative)

  return (
    str( float(discreteCoordinate[0]) * DIMENSIONS_LATITUDE), 
    str( float(discreteCoordinate[1]) * DIMENSIONS_LONGTITUDE)
    )

def getCoordCriteriaMatch(currCoord, currCoordList, compareCoordList, currCoordIndex):
  # Get the index of first coordinate in compareCoordList that is within distance with currCoord and has similar bearing (use both lists for bearing)
  resultIndex = -1
  i = 0

  while i < len(compareCoordList) and resultIndex == -1:
    if coordsMatchCriteria(currCoord, compareCoordList[i], currCoordList, compareCoordList, currCoordIndex, i):
      resultIndex = i
    i += 1
  return resultIndex

def coordsMatchCriteria(leftCoord, rightCoord, leftCoordList, rightCoordList, leftIndex, rightIndex):
  # See if the two coordinates are within threshold distance and bearing difference
  # These constants are subject to change wrt experiments
  maxDistanceDiff = 450
  maxBearingDiff = 10
  match = False
  # First, check distance comparison
  distance = getLatLongDistance(leftCoord, rightCoord)

  if distance < maxDistanceDiff:
    # Distance within max. Check bearing difference
    # Only consider bearing when both coordLists are greater than 1
    if len(leftCoordList) == 1 or len(rightCoordList) == 1:
      match = True
    else:
      leftBearing = getFinalBearing(leftCoord, leftCoordList[leftIndex+1]) \
      if leftIndex < len(leftCoordList)-1 else \
      getFinalBearing(leftCoordList[leftIndex-1], leftCoord)

      rightBearing = getFinalBearing(rightCoord, rightCoordList[rightIndex+1]) \
      if rightIndex < len(rightCoordList)-1 else \
      getFinalBearing(rightCoordList[rightIndex-1], rightCoord)

      match = abs(leftBearing - rightBearing) < maxBearingDiff

  return match

def formerItemsWithinDistance(bestRuleConsequent, confirmRegions):
  numConseq = len(bestRuleConsequent)
  numConfrm = len(confirmRegions)

  minLen = min(numConseq, numConfrm) \
  if min(numConseq, numConfrm) < MAX_MINIMUM_MATCH \
  else MAX_MINIMUM_MATCH

  if minLen == 0:
    return False
  bestRuleConsequent = [ ( float(x), float(y) ) for x, y in bestRuleConsequent[:minLen]]
  confirmRegions = [ ( float(x), float(y) ) for x, y in confirmRegions[:minLen]]

  # Make sure all entries have distance <= 1
  # euclidean distance or haversine distance?
  distInRange = True
  i = 0
  while i < minLen and distInRange:
    distInRange = int(getHaversineDistance(confirmRegions[i], bestRuleConsequent[i])) <= 450
    i += 1

  return distInRange
def compareResults(bestRuleConsequent, confirmRegions, baseMethod=True):
  # Compare two lists of regions. 
  # If the two region lists have a small distance and similar bearing, the prediction is correct

  # Longest Congruent Subsequence of region pairs with similar bearing within certain distance. If meets minimum, consider correct
  # This is a lot like getMatchingLen except with fuzzier criteria
  if baseMethod:
    return formerItemsWithinDistance(bestRuleConsequent, confirmRegions)
  else:
    shorterLen = min(len(bestRuleConsequent), len(confirmRegions))
    minMatchLen = shorterLen

    if shorterLen == 0:
      return False

    bestRuleConsequent = [ ( float(brc[0]), float(brc[1]) ) for brc in bestRuleConsequent ]
    confirmRegions = [ ( float(cr[0]), float(cr[1]) ) for cr in confirmRegions]

    maxLen = getLongestSimilarSequence(bestRuleConsequent, confirmRegions)

    return maxLen >= minMatchLen

def getLongestSimilarSequence(ruleRegions, testRegions):
  resultLen = 0
  ruleCoordinates = map(characteristicCoordinate, [region for region in ruleRegions])
  testCoordinates = map(characteristicCoordinate, [region for region in testRegions])

  i = 0
  j = 0
  while i < len(testCoordinates):
    currLen = 0
    currCoord = testCoordinates[i]
    index = getCoordCriteriaMatch(currCoord, testCoordinates, ruleCoordinates, i)
    if index > -1:
      j = i

      while j < len(testRegions) and index < len(ruleCoordinates) and \
      coordsMatchCriteria(
        testCoordinates[j],
        ruleCoordinates[index],
        testCoordinates,
        ruleCoordinates,
        j,
        index
      ):
        j += 1
        index += 1
        currLen += 1

    if currLen > resultLen:
      resultLen = currLen
    i += 1

  return resultLen

def testRules():
  ignoreExtrapolation = bool( int( sys.argv[3] ) )

  with open(sys.argv[1], 'r') as test_vectors, open(sys.argv[2], 'r') as rules:
    correctCount = 0
    totalCount = 0
    extrapCount = 0

    extrapWorks = False
    for line in test_vectors:
      regions = [( str(regionalizedCoordinate[0]), str(regionalizedCoordinate[1]) ) for regionalizedCoordinate in gatherDedupedRegionList(line)]
      # Now see the rules. Could also play with where the split happens
      checkRegions = regions[:len(regions)/2]
      confirmRegions = regions[len(regions)/2:]

      searchRounds = 0
      complete = False
      while not complete:
        bestRule, bestRuleScore, bestRuleConsequent = getBestRule(rules, checkRegions, flex=False)
        if bestRuleScore == 0 and ignoreExtrapolation:
          complete = True
          totalCount -= 1
          break

        if bestRuleScore == 0 and searchRounds < EXTRAPOLATION_LIMIT:
          checkRegions.append(
            getExtrapolatedRegion(
              gatherCoordinateList(line), 
              checkRegions,
              searchRounds
              )
            )
          if len(checkRegions) > 1 and checkRegions[-1] == checkRegions[-2]:
            checkRegions = checkRegions[:-1]
          searchRounds += 1
        else:
          if bestRuleScore > 0 and searchRounds > 0:
            extrapWorks = True
          complete = True

      # if bestRuleScore > 0:
      #     match_file.write(line)
      # else:
      #   print bestRuleScore
      #   miss_file.write(line)

      if searchRounds > 0:
        print "Trajectory extrapolation was used"
        print "Total extrapolations performed:", searchRounds
        extrapCount += 1

      print "The best-fit rule had a score of %f and its consequent is:" % bestRuleScore
      print bestRuleConsequent
      print "The actual final regions of the current trajectory is:"
      print confirmRegions

      predictionWithinRange = compareResults(bestRuleConsequent, confirmRegions)

      if predictionWithinRange:
        print "The prediction was correct (At least in terms of current analysis)"

        correctCount += 1
      else:
        print "The prediction was incorrect (At least in terms of current analysis)"
   #   print line
   #   print bestRule
      totalCount += 1

    correctRatio = float(correctCount) / float(totalCount)
    print "Correct to incorrect ratio was %f. This included trajectory extrapolation" % correctRatio

    print "Extrapolation is working:", extrapWorks
    print extrapCount
    print totalCount
    print correctCount

def main():
  if len(sys.argv) != 4:
    print "Usage: {0} <VectorsInput> <RulesInput> <IgnoreExtrapolation0/1>".format(sys.argv[0])
  else:
    testRules()

if __name__ == '__main__':
  main()
else:
  print __name__