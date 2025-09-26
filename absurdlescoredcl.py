"""the idea behind this is:
- there are a number of wordlists of equal length and one is chosen randomly per game (/can pick random section of words) - a section of words from the wordlist are picked randomly
- you start with a score of 100
- you can adjust difficulty by chosing a longer list of words : beginner mode = 100 words, intermediate mode = 200 words, advanced mode = 300 words - each file will have 500 words
- -10 for each guess you need to make
- hints: you can chose n number of words that you want to compare the future biggest bucket for resulting from picking that word but for each word you 
  -5 from overall score"""

from rich.console import Console 
from dataclasses import dataclass, field
from typing import List
import enchant
import absurdlev2
from random import sample

BEG_MODE_NO = 50
INT_MODE_NO = 100
ADV_MODE_NO = 150

FILE_LENGTH = 300

INITIAL_SCORE = 100
HINT_PENALTY = 5
GUESS_PENALTY = 10

WORDLIST_FILE = "wordlists/approx3000words.txt"

"""
Returns a random list of uppercase 5 letter words from the file named by WORDLIST_FILE. The number of words in the wordlist depends on the difficulty 
mode chosen by the user. 
"""
def getWordList(totalWords):
        with open(WORDLIST_FILE, 'r') as file:
            lines = file.readlines()
        subset_lines = sample(lines, totalWords) # chooses random sample of words from the words in WORDLIST_FILE (number specified by totalWords)
        formatted_lines = []
        for line in subset_lines:
            formatted_lines.append(line.strip().upper()) #all words correctly formatted 
        return formatted_lines #this will be the original wordlist for the game 

"""
The number of words in the original wordlist is determined by difficult mode chosen by user.
"""
def modeToNumber(mode) :
    if mode == "b":
        return BEG_MODE_NO
    elif mode == "i":
        return INT_MODE_NO
    elif mode == "a":
        return ADV_MODE_NO

"""
Used to check that hint words entered are length 5 and belong to the imported dictionary. 
"""  
def checkValidWords(d, words):
    for word in words:
        if not (len(word) == 5) or not(d.check(word)) :
            return False
    return True

def main():
    console = Console()
    d = enchant.Dict("en_GB") #unlike in qntm's Absurdle, guesses just need to be from this imported dictionary file
    current_pattern = ''
    console.print("START GAME")
    score = INITIAL_SCORE
    mode = ''
    while mode not in ('b', 'i', 'a'):
        mode = input("Enter 'b' to select beginner mode, 'i' to select intermediate mode, and 'a' to select advanced mode") # user selects mode 
    totalWords = modeToNumber(mode)
    wordlist = getWordList(totalWords)
    originalWordList = wordlist
    while True:
        if score < 10: #when score is less than or equal to 0 then game over 
            console.print("You have run out of guesses: game over")
            break
        else: 
            
            hintWords = input("If you would like hint words enter them now e.g. 'apple house' (cost per hint is " + str(HINT_PENALTY)+ ") or press enter: ").split()
            words_are_valid = checkValidWords(d, hintWords)
            while not(words_are_valid) :
                hintWords = input("Invalid hints. If you would like hint words enter them now e.g. 'apple house' (cost per hint is " + str(HINT_PENALTY)+ ") or press enter: ").split()
                words_are_valid = checkValidWords(d, hintWords)
            for hintWord in hintWords :
                hintWord = hintWord.upper()
                score = score - HINT_PENALTY #for every hint word, a penalty is inflicted of 5 points 
                buckets = absurdlev2.generateBuckets(hintWord, wordlist) # checks how advantageous a guess would be by telling user how many words in biggest bucket generated 
                #by that word as that would be the new pruned wordlist on the next guess 
                wordListAfterHint = absurdlev2.getBiggestBucketWords(buckets, absurdlev2.getBiggestBucketPattern(buckets))
                console.print("Choosing the word " + hintWord + " will reduce the number of possible solution words to " + str(len(wordListAfterHint)))
                console.print("Score = " + str(score))
            guess = (input("Enter Guess: ")).upper()
            score = score - GUESS_PENALTY # for every guess a penalty of 10 points is deduced from score 
            while  not (len(guess) == 5) or not(d.check(guess) or not(guess in originalWordList)) :
                guess = (input("Invalid. Enter Guess: ")).upper()
            buckets = absurdlev2.generateBuckets(guess, wordlist) #if guess is valid generates buckets
            current_pattern = absurdlev2.getBiggestBucketPattern(buckets)
            console.print(absurdlev2.formatWordWithPattern(guess, current_pattern))
            console.print("Score = " + str(score))
            if (current_pattern == '🟩' * 5) : # there must only be one word remaining if biggest bucket has a pattern that is 5 green tiles 
                console.print("Your final score is: " + str(score))
                break
            else :
                wordlist = absurdlev2.getBiggestBucketWords(buckets, current_pattern) #must not have narrowed down wordlist to single word 
                

if __name__ == "__main__":
    main()   





