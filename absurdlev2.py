"""
This is the correct version of absurdle: in this version buckets are sorted based on how much info they give so if there is a tie between buckets then the one with the least info is chosen
"""
#  from https://www.freecodecamp.org/news/how-to-build-a-wordle-clone-using-python-and-rich/ for formatting 
from rich.console import Console 
from dataclasses import dataclass, field
from typing import List
import enchant
import unittest

WORDLIST_FILE = "wordlists/100words2.txt"


def wordsToArray(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip().upper())
    return lines
    

#to change the colour of a tile at a specific index in a pattern 
def changeTile (pattern, new_tile, index) :
    return pattern[0:index] + new_tile + pattern[(index + 1): len(pattern) + 2]


#assign green then yellow then grey tiles 
def generatePattern(guess, target) :
    pattern = "⬜" * 5 
    i = 0 
    remainingTargetLetters = target 
    #first checks for green
    while i < len(target) :
        if guess[i] == target[i] :
            pattern = changeTile (pattern, '🟩', i)
            remainingTargetLetters = remainingTargetLetters.replace(target[i],"", 1)
            i +=1
        else :
            i +=1
    #then checks for yellow
    i = 0
    while i < len(target) :
        if pattern[i] == '🟩' :
            i +=1
        elif guess[i] in remainingTargetLetters:
            pattern = changeTile (pattern, '🟨', i)
            remainingTargetLetters = remainingTargetLetters.replace(guess[i],"", 1)
            i +=1
            
        else: 
            i +=1
    return pattern

@dataclass
class BucketInfo: 
    words: List[str] = field(default_factory=list)
    size: int = 0

def generateBuckets (guess, wordlist) :
    buckets = {} # maps patterns to BucketInfo instances - starts off empty
    for word in wordlist: 
        pattern = generatePattern (guess, word)
        if pattern in buckets :
            buckets[pattern].words.append(word)
            buckets[pattern].size += 1
        else : 
            buckets[pattern] = BucketInfo(words= [word], size= 1)
    sortedBuckets = sortBucketsByPatternScore(buckets)
    return sortedBuckets
    
def getBiggestBucketPattern(buckets) :
    biggestBucketPattern = ''
    biggestBucketSize = 0 
    for pattern, bucketInfo in buckets.items():
        if bucketInfo.size > biggestBucketSize: # if biggest buckets are tied for number of words then the first one will be chosen (https://kevinl.info/absurdle/)
            biggestBucketPattern = pattern
            biggestBucketSize = bucketInfo.size
    return biggestBucketPattern

  

def getBiggestBucketWords(buckets, biggestBucketPattern) :
    return buckets[biggestBucketPattern].words 


#  from https://www.freecodecamp.org/news/how-to-build-a-wordle-clone-using-python-and-rich/ for formatting 
#for formatted printing 
def correctLetterAndPlace (letter) :
    return f'[white on green]{letter}[/]'
#for formatted printing 
def correctLetterWrongPlace (letter) :
    return f'[white on yellow]{letter}[/]'
#for formatted printing 
def incorrect_letter (letter) :
    return f'[black on gray]{letter}[/]'


def formatWordWithPattern (word, pattern): 
    formattedWord = ''
    for i in range (len(pattern)):
        if pattern[i] == '🟩':
            formattedWord = formattedWord + correctLetterAndPlace(word[i]) + " "
        elif pattern[i] == '🟨':
            formattedWord = formattedWord + correctLetterWrongPlace(word[i]) +  " "
        else :
            formattedWord = formattedWord + incorrect_letter (word[i]) + " "
    return formattedWord

"""
this is what makes absurdle.py different to absurdle2.0.py:
buckets are given a score based on how much information they provide the user green = 2, yellow = 1, grey = 0 and position of tile
"""
#generates unique score for each pattern: 
def patternToPatternScore(pattern):
    score = 0
    greenWeight = 7
    yellowWeight = 3
    whiteWeight = 1
    for i in range (len(pattern)):
        if pattern[i] == '🟩':
            score = score + ((1 + ((4 - i) / 10)) * greenWeight)
        elif pattern[i] == '🟨':
            score = score + ((1 + ((4 - i) / 10)) * yellowWeight)
        elif pattern[i] == '⬜':
            score = score + ((1 + ((4 - i) / 10)) * whiteWeight)
    return score

#sorts buckets by information they give: lowest amount of info to highest 
def sortBucketsByPatternScore(buckets):
    sortedBucketsList = sorted(buckets.items(), key=lambda item: patternToPatternScore(item[0]))
    sortedBucketsDict = {pattern: bucketInfo for pattern, bucketInfo in sortedBucketsList}
    return sortedBucketsDict



def main():
    console = Console()
    d = enchant.Dict("en_GB") # https://pyenchant.github.io/pyenchant/tutorial.html
    wordlist = wordsToArray(WORDLIST_FILE)
    current_pattern = ''
    while True : # cannot do a do while in Python https://www.freecodecamp.org/news/python-do-while-loop-example/
        guess = (input("Enter Guess: ")).upper()
        if not (len(guess) == 5) or (not (d.check(guess)) and not(guess in wordlist)) : #TODO come back and make this a while 
            break 
        else: 
            buckets = generateBuckets(guess, wordlist)
            current_pattern = getBiggestBucketPattern(buckets)
            console.print(formatWordWithPattern(guess, current_pattern))
            #console.print("wordlist before pruning:" + str(wordlist))
            if (current_pattern == '🟩' * 5) :
                break
            else :
                wordlist = getBiggestBucketWords(buckets, current_pattern)
                #console.print("wordlist after pruning: " + str(wordlist))

def testMain(wordlist, guesses):
    current_pattern = ''
    patterns = []
    for guess in guesses : # cannot do a do while in Python https://www.freecodecamp.org/news/python-do-while-loop-example/  
        buckets = generateBuckets(guess, wordlist)
        current_pattern = getBiggestBucketPattern(buckets)
        patterns.append(current_pattern)
        if (current_pattern == '🟩' * 5) :
            return patterns
        else: 
            wordlist = getBiggestBucketWords(buckets, current_pattern)
    return patterns

if __name__ == "__main__":
    main() 