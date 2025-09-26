"""
This file was used to generate all the wordlist files e.g. 100words1, 500words2...
"""
import absurdlev2
from random import sample

def create_wordlist_size_n(all_words, n, j):
    subset_words = sample(all_words, n) #took a random subset of lines from words2.txt which contains over 3000 words - the number of words dependend on n (the intended size of the wordlist)
    with open(f'{n}words{j}.txt', 'w+') as f:
        for line in subset_words:
            f.write('%s\n' %line)





def main():
    all_words = absurdlev2.wordsToArray("words2.txt")
    for i in range(1, 15):
        n = i * 100
        for j in range (1, 4): # so that there are three word lists of each size to calculate averages 
            create_wordlist_size_n(all_words, n, j)

if __name__ == "__main__":
    main() 