
"""This solver iteratively finds many routes for the minimal length. It works by looking two steps into the future. It first checks for solutions of length 3 and
if there are none then it checks solutions of length 4 and so on until solutions are found of that length."""
from rich.console import Console
import absurdlev2
from dataclasses import dataclass, field
from typing import List
import time #https://www.geeksforgeeks.org/time-process_time-function-in-python/
import sys

""" checks whether all buckets contain just one word """
def allBucketsAreLengthOne(buckets) :
    for pattern in buckets:
       if buckets[pattern].size != 1:
            return False #immediately returns 
    return True 


@dataclass
class UnsuccessfulRouteInfo: 
    unsuccessful_route_words: List[str] = field(default_factory=list)
    biggestBucketWords: List[str] = field(default_factory=list)


"""
This function will return all solution routes for the same initial guess word.
If solutions exist of length nOfSolutionWords, then these solutions will be returned. Otherwise an empty list will be returned. 
This function works by looking two steps ahead. When the number of guesses so far is two less than the nOfSolutionWords, the solver will check whether a valid
solution can be found in the next two gos. This will not be posible if not all the buckets contain just one word in the next step, so the solver will move onto
the next possible guess word. If they are all one length, then a solution route must be all guesses made so far + the word that generated buckets of length one + the word contained in the first bucket
The index refers to the number of guesses already made when creating a possible solution route. 

"""
def solver4Updated(biggestBucketWords, prevGuesses, nOfSolutionWords, index):
    routes = [] #routes will contain solutions if there are any but is initiallised to be empty
    unsuccessful_routes_info = []
    for word in biggestBucketWords :
        buckets = absurdlev2.generateBuckets(word, biggestBucketWords)
        #if (index == (nOfSolutionWords - 2)) : # will look two steps ahead if the current index (indicating how many guesses have already been made on the route)
                                               # is two less than the goal number of words in a solution (nOfSolutionWords)
            
        if not allBucketsAreLengthOne(buckets) : # if looking at the next step, not all the buckets are length one, then it is a dead end
            biggestBucketPattern = absurdlev2.getBiggestBucketPattern(buckets)
            biggestBucketWordsNext = absurdlev2.getBiggestBucketWords(buckets, biggestBucketPattern)
            unsuccessful_routes_info.append(UnsuccessfulRouteInfo(unsuccessful_route_words=prevGuesses + [word], biggestBucketWords=biggestBucketWordsNext))
        else:
            route = prevGuesses + [word] + [list(buckets.values())[0].words[0]] # if all buckets are length one then a solution route must be all previous guesses in route + that word+ the word in the first bucket
            if not (route in routes) : 
                routes.append(route) # ensures that all solution word sequences are unique 
    return routes, unsuccessful_routes_info # return all solutions 

"""
This will return all possible solution sequences of words which have a length of nOfSolutionWords. 
"""
def solver4helper(wordlist, nOfSolutionWords, old_unsuccessful_routes_info) :
    allroutes = [] # initially empty 
    all_unsuccessful_routes_info = []
    if nOfSolutionWords == 3:
        for word in wordlist: # iterates through all the words in the wordlist and finds solution sequences of words starting with that word if they exist
                buckets = absurdlev2.generateBuckets(word, wordlist)
                biggestBucketWords = absurdlev2.getBiggestBucketWords(buckets, absurdlev2.getBiggestBucketPattern(buckets))
                routes, unsuccessful_routes_info = solver4Updated(biggestBucketWords, [word], nOfSolutionWords, 1) # routes will contain all solution sequences of words with the same starting guess word
                if routes != []: # if solutions exist then they will be added to allroutes 
                    allroutes = allroutes + routes
                else:
                    all_unsuccessful_routes_info = all_unsuccessful_routes_info + unsuccessful_routes_info
    else: 
        for old_route_info in old_unsuccessful_routes_info:
            routes, unsuccessful_routes_info = solver4Updated(old_route_info.biggestBucketWords, old_route_info.unsuccessful_route_words, nOfSolutionWords, len(old_route_info.unsuccessful_route_words))
            if routes != []: # if solutions exist then they will be added to allroutes 
                allroutes = allroutes + routes
            else:
                all_unsuccessful_routes_info = all_unsuccessful_routes_info + unsuccessful_routes_info
    
    return allroutes, all_unsuccessful_routes_info
        
def main(wordListFile):
    start_time = time.process_time() # to measure CPU time 
    wordList = absurdlev2.wordsToArray(wordListFile) # initial wordlist 
    console = Console()
    nOfSolutionWords = 3 # the solver will first check if there are any solutions that are sequences of three guesses. If this is not found then it will continue
                         #increementing this number until solutions are found of that length 
    old_unsuccessful_routes_info = [UnsuccessfulRouteInfo(unsuccessful_route_words= [], biggestBucketWords = [])]
    unsuccessful_routes_info = old_unsuccessful_routes_info
    while True:
        routes, unsuccessful_routes_info = solver4helper(wordList, nOfSolutionWords, old_unsuccessful_routes_info) #kept console for debugging
        if routes != [] : # when there are solution word sequences of that length then all solutions of that length are returned 
            console.print("minimum solution is " + str(nOfSolutionWords) + " words and possible routes are " + str(routes))
            console.print("Number of solution routes = " + str(len(routes))) # for comparison of solver algorithms 
            end_time = time.process_time() # to measure CPU time 
            console.print(f"CPU time used: {end_time - start_time} seconds")
            break
        else:
            console.print("no solution with " + str(nOfSolutionWords) + " words")
            old_unsuccessful_routes_info = unsuccessful_routes_info 
            nOfSolutionWords += 1 # if no solution sequences of that length are found then checks for solutions with one more guess 

 
def runForAlgorithmEvaluation(wordlist_file):
    start_time = time.process_time() # to measure CPU time 
    wordList = absurdlev2.wordsToArray(wordlist_file) # initial wordlist 
    console = Console()
    #console.log(str(wordList))
    nOfSolutionWords = 3 # the solver will first check if there are any solutions that are sequences of three guesses. If this is not found then it will continue
                         #increementing this number until solutions are found of that length 
    old_unsuccessful_routes_info = [UnsuccessfulRouteInfo(unsuccessful_route_words= [], biggestBucketWords = [])]
    unsuccessful_routes_info = old_unsuccessful_routes_info
    while True:
        routes, unsuccessful_routes_info = solver4helper(wordList, nOfSolutionWords, old_unsuccessful_routes_info)
        if routes != [] : # when there are solution word sequences of that length then all solutions of that length are returned 
            end_time = time.process_time() # to measure CPU time 
            console.print(f"{wordlist_file} CPU time used: {end_time - start_time} seconds; Number of Routes: {str(len(routes))}; Length of minimum length routes: {str(nOfSolutionWords)}")
            break
        else:
            old_unsuccessful_routes_info = unsuccessful_routes_info 
            nOfSolutionWords += 1 # if no solution sequences of that length are found then checks for solutions with one more guess 


"""instead of printing, returns list of routes of minimal length for testing purposes """
def getMinLengthRoutes(wordList):
    console = Console()
    nOfSolutionWords = 3 
    minLengthRoutes = []
    old_unsuccessful_routes_info = [UnsuccessfulRouteInfo(unsuccessful_route_words= [], biggestBucketWords = [])]
    unsuccessful_routes_info = old_unsuccessful_routes_info
    while minLengthRoutes == []:
        routes, unsuccessful_routes_info = solver4helper(wordList, nOfSolutionWords, old_unsuccessful_routes_info)
        if routes != [] :
            minLengthRoutes = routes
        else:
            old_unsuccessful_routes_info = unsuccessful_routes_info 
            nOfSolutionWords += 1
    return minLengthRoutes

 
            
     
if __name__ == "__main__":
    main(sys.argv[1])