import unittest
import absurdlev2

class Tests(unittest.TestCase) : # https://docs.python.org/3/library/unittest.html
    #TESTING PATTERN GENERATION
    # testing the same word produces all green tiles 
    def test1(self) :
        self.assertEqual(absurdlev2.generatePattern('HELLO', 'HELLO'), ('🟩' * 5))
    #testing that two words with no letters in common produces all white tiles 
    def test2(self) :
        self.assertEqual(absurdlev2.generatePattern('HELLO', 'AGAIN'), ('⬜' * 5))
    #testing anagrams 
    def test3(self) : 
        self.assertEqual(absurdlev2.generatePattern('CIDER', 'CRIED'), '🟩🟨🟨🟩🟨') 
    #testing whether if the target word has just one of a letter that a guess with two of that letter (with one in the right position) will give a white tile to the other instance
    def test4(self) :
        self.assertEqual(absurdlev2.generatePattern('DRIED', 'DRAMA'), '🟩🟩⬜⬜⬜') 
    #testing whether if the target word has one instance of that letter but the guess has 3 instances of that letter (both in the wrong place) then the first instance is yellow and the others are white 
    def test5(self) :
       self.assertEqual(absurdlev2.generatePattern('RARER', 'DRAMA'), '🟨🟨⬜⬜⬜') 
    #TESTING SAMPLE PROGRAMS
    #this example ends up with two final buckets each of 1 word but the word with the first pattern in sorted order is chosen, guesses are found in the biggest bucket
    def test6(self) :
        self.assertEqual(absurdlev2.testMain(['WORST', 'WORTH', 'WOULD', 'WOUND', 'WRITE', 'WRONG', 'WROTE', 'YIELD', 'YOUNG', 'YOUTH'], ['YOUNG', 'WORST','WORTH']), ['⬜🟩⬜⬜⬜', '🟩🟩🟩⬜🟨','🟩🟩🟩🟩🟩'])
    #this example ends up with two final buckets each of 1 word but the word with the second pattern in sorted order is chosen (compared to test 7 there should be one more step), guesses are found in the biggest bucket
    def test7(self) :    
        self.assertEqual(absurdlev2.testMain(['WORST', 'WORTH', 'WOULD', 'WOUND', 'WRITE', 'WRONG', 'WROTE', 'YIELD', 'YOUNG', 'YOUTH'], ['YOUNG', 'WORTH', 'WORST']), ['⬜🟩⬜⬜⬜', '🟩🟩🟩🟨⬜','🟩🟩🟩🟩🟩'])
    #this example always picks the first word in the biggest bucket 
    def test8(self) :
        self.assertEqual(absurdlev2.testMain(['PROOF', 'PROUD', 'PROVE', 'QUEEN', 'QUICK', 'QUIET', 'QUITE', 'RADIO', 'RAISE', 'RANGE', 'RAPID', 'RATIO'], ['RAPID', 'QUICK', 'QUIET', 'QUITE']),['⬜⬜⬜🟨⬜', '🟩🟩🟩⬜⬜','🟩🟩🟩🟨🟨', '🟩🟩🟩🟩🟩'])
    #same as last but picks the second word in biggest bucket so compared to test 8 there should be one more step, guesses are found in the biggest bucket
    def test9(self) :
        self.assertEqual(absurdlev2.testMain(['PROOF', 'PROUD', 'PROVE', 'QUEEN', 'QUICK', 'QUIET', 'QUITE', 'RADIO', 'RAISE', 'RANGE', 'RAPID', 'RATIO', 'REACH', 'READY', 'REFER', 'RIGHT', 'RIVAL', 'RIVER', 'ROBIN', 'ROGER', 'ROMAN', 'ROUGH', 'ROUND'], ['RAPID', 'QUICK', 'QUITE', 'QUIET']),['⬜⬜⬜🟨⬜','🟩🟩🟩⬜⬜', '🟩🟩🟩🟨🟨', '🟩🟩🟩🟩🟩'])
    #if a wordlist has two words then there must be two guesses needed
    def test10(self) :
        self.assertEqual(absurdlev2.testMain(['PROOF', 'PROUD'],['PROOF', 'PROUD']), ['🟩🟩🟩⬜⬜', '🟩🟩🟩🟩🟩'])
    #changing order of guesses should mean two gueses are still needed
    def test11(self) :
        self.assertEqual(absurdlev2.testMain(['PROOF', 'PROUD'],['PROUD', 'PROOF']), ['🟩🟩🟩⬜⬜', '🟩🟩🟩🟩🟩'])
if __name__ == "__main__":
    unittest.main()