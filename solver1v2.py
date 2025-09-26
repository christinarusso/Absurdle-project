""" This solver only looks one step into the future (which word in the next step will produce the smallest biggest bucket). 
It gives many solutions but not all solutions."""
from rich.console import Console
import absurdlev2
from dataclasses import dataclass, field
from typing import List
import time #https://www.geeksforgeeks.org/time-process_time-function-in-python/
import sys


@dataclass # https://docs.python.org/3/library/dataclasses.html
class BiggestBucketInfo:
    startingWord: str = ''
    biggestBucketPattern: str = ''
    biggestBucketWords: List[str] = field(default_factory=list)
    biggestBucketSize: int = 0

@dataclass
class RouteInfo:
    wordsOnRoute: List[str] = field(default_factory=list)
    length: int = 0

"""Returns the bucket info of the smallest biggest bucket produced in the next turn for a given wordlist"""
def getSmallestBiggestBucketInWordListInfo(wordlist):
    smallestBiggestBucketInfo = None
    for word in wordlist: # iterates through all words in the current wordlist 
        currentBuckets = absurdlev2.generateBuckets(word, wordlist)
        currentBiggestBucketPattern = absurdlev2.getBiggestBucketPattern(currentBuckets)
        currentBiggestBucketWords = absurdlev2.getBiggestBucketWords(currentBuckets, currentBiggestBucketPattern)
        currentBiggestBucketInfo = BiggestBucketInfo(
            startingWord = word, 
            biggestBucketPattern = currentBiggestBucketPattern, 
            biggestBucketWords = currentBiggestBucketWords, 
            biggestBucketSize = len(currentBiggestBucketWords)) # gets the pattern, words contained and size of the biggest bucket generated if that word is chosen
                                                                # and record the word used to generate it 
        if not smallestBiggestBucketInfo or (currentBiggestBucketInfo.biggestBucketSize < smallestBiggestBucketInfo.biggestBucketSize) :
            smallestBiggestBucketInfo = currentBiggestBucketInfo # update the information about the smallest biggest bucket if this buckert is smaller than all 
                                                                 # those already produced  
    return smallestBiggestBucketInfo

"""Makes the assumption that the shortest route is found by finding the word with the smallest biggest bucket each time"""
def newFindShortestRoute(startword, wordlist):
    shortestRouteInfo = RouteInfo(wordsOnRoute = [startword], length = 1)
    buckets = absurdlev2.generateBuckets(startword, wordlist)
    biggestBucketPattern = absurdlev2.getBiggestBucketPattern(buckets)
    biggestBucketWords = absurdlev2.getBiggestBucketWords(buckets, biggestBucketPattern)
    while not (biggestBucketPattern == '🟩' * 5): # keeps on finding the smallest biggest bucket based on remaining
                                                  # words in the wordlist after each guess made until a solution is found
        smallestBiggestBucketInfoInWordList = getSmallestBiggestBucketInWordListInfo(biggestBucketWords)
        shortestRouteInfo.wordsOnRoute.append(smallestBiggestBucketInfoInWordList.startingWord)
        shortestRouteInfo.length +=1
        biggestBucketWords = smallestBiggestBucketInfoInWordList.biggestBucketWords
        biggestBucketPattern = smallestBiggestBucketInfoInWordList.biggestBucketPattern
    return shortestRouteInfo

"""
Returns all word sequences with the minimum number of guesses. Also used for tetsing and comparison with other solvers.
""" 
def getMinLengthRoutes(wordList):
    minLength = None
    minLengthRoutes = []
    for word in wordList: # finds the shortest route for all possible starting words based on the heuristic
        route = newFindShortestRoute(word, wordList)
        if minLength is None or route.length < minLength: #if the route is shorter than all the ones found or the first route found
            #so far then the list of routes of minimum length should currently only contain the current route 
            minLength = route.length
            minLengthRoutes = [route.wordsOnRoute]
        elif route.length == minLength: # if the route is the same length as the shortest routes found so far then it should be added to the list
            minLengthRoutes.append(route.wordsOnRoute)
    return minLengthRoutes   

def runForAlgorithmEvaluation(wordlist_file):
    start_time = time.process_time() # to measure CPU time
    wordList = absurdlev2.wordsToArray(wordlist_file)
    console = Console()
    routes = getMinLengthRoutes(wordList)
    end_time = time.process_time() # to measure CPU time 
    console.print(f"{wordlist_file} CPU time used: {end_time - start_time} seconds; Number of Routes: {len(routes)}; Length of minimum length routes: {len(routes[0])}")


def main(wordListFile):
    wordList = absurdlev2.wordsToArray(wordListFile)
    console = Console()
    routes = getMinLengthRoutes(wordList)
    console.print(routes)

if __name__ == "__main__":
    main(sys.argv[1])