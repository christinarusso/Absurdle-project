"""
This solver finds a single sequence of guesses with the minimum number of guesses necesary. Uses similar logic to solver 3v2 but returns just the one solution.
"""
from rich.console import Console
import absurdlev2
import time #https://www.geeksforgeeks.org/time-process_time-function-in-python/
import sys

"""
Checks if all buckets contain just a single word
"""
def allBucketsAreLengthOne(buckets) :
    for pattern in buckets:
       if buckets[pattern].size != 1:
            return False # if a bucket with more than one word, return False immediately 
    return True 

"""
This function will return a single solution route for a given initial guess word. 
If a solution exists of length nOfSolutionWords, it will be returned. Otherwise an empty list will be returned. 
This function works by looking two steps ahead. When the number of guesses so far is two less than the nOfSolutionWords, the solver will check whether a valid
solution can be found in the next two gos. This will not be posible if not all the buckets contain just one word in the next step, so the solver will move onto
the next possible guess word. If it was the case, a pattern for all other words will be generated against the word in the first bucket. Patterns must all be 
unique for a solution to be achieved in the desired number of guesses. If they are unique, the final guess must be the word with the lowest pattern score. 
The index refers to the number of guesses already made when creating a possible solution route. 

"""
def solver2Updated(biggestBucketWords, prevGuesses, nOfSolutionWords, index):
    for word in biggestBucketWords :
        buckets = absurdlev2.generateBuckets(word, biggestBucketWords)
        if (index == (nOfSolutionWords - 2)) :  # will look two steps ahead if the current index (indicating how many guesses have already been made on the route)
                                               # is two less than the goal number of words in a solution (nOfSolutionWords)
                if allBucketsAreLengthOne(buckets) : # all buckets must be length one for a solution sequence 
                    route = prevGuesses + [word] + [list(buckets.values())[0].words[0]] #+ [lowestScoreWord] # if they are all unique then a solution must have been found
                    return route
                else:
                    return []
        else : # when the index is too low to look two steps ahead, the word will be added to a possible solution sequence
                newBiggestBucketWords1 = absurdlev2.getBiggestBucketWords(buckets, absurdlev2.getBiggestBucketPattern(buckets))
                newPrevGuesses = prevGuesses + [word]
                return solver2Updated(newBiggestBucketWords1, newPrevGuesses, nOfSolutionWords, index + 1)

"""
Checks if there is a solution route but iterating through all words in the wordlist and using it as a starter guess word until a solution is found 
"""
def solver2helper(wordlist, nOfSolutionWords) :
    for word in wordlist: #iterates through words in wordlist until a solution is found 
        buckets = absurdlev2.generateBuckets(word, wordlist)
        biggestBucketWords = absurdlev2.getBiggestBucketWords(buckets, absurdlev2.getBiggestBucketPattern(buckets))
        route = solver2Updated(biggestBucketWords, [word], nOfSolutionWords, 1) # checks if there is a solution if that word is used as the first guess
        if  route != []:
             return route # returns solution if one found
    return []

"""instead of printing, returns list of routes of minimal length for testing purposes """
def getMinLengthRoute(wordList) :
    nOfSolutionWords = 3
    minLengthRoute = []
    while minLengthRoute == []:
         minLengthRoute = solver2helper(wordList, nOfSolutionWords)
         nOfSolutionWords += 1
    return minLengthRoute


def main(wordListFile):
    start_time = time.process_time() # to measure CPU time 
    wordList = absurdlev2.wordsToArray(wordListFile)
    console = Console()
    nOfSolutionWords = 3 # first checks for a solution sequence of length 3 but this will be incremented by one if no solution is found
    while True:
        route = solver2helper(wordList, nOfSolutionWords) 
        if route != [] :
            console.print("minimum solution is " + str(nOfSolutionWords) + " words and possible route is " + str(route))
            end_time = time.process_time() # to measure CPU time 
            console.print(f"CPU time used: {end_time - start_time} seconds")
            break
        else:
            console.print("no solution with " + str(nOfSolutionWords) + " words")
            nOfSolutionWords += 1


if __name__ == "__main__":
    main(sys.argv[1]) 