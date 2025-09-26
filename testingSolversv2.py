import absurdlev2
import solver1v2
import solver3v2
import solver4v2
from rich.console import Console
import sys

"""
For a solver to be sound, each solution route it finds must be correct. 
"""
def testSoundness2(routes, wordListFileName, wordList, console):
    console = Console()
    for route in routes:
        if testSoundnessRoute(route, wordList, console) == False:
            console.log(f"{wordListFileName}: Soundness: False")
            return False
    console.log(f"{wordListFileName}: Soundness: True")
    return True   
                  
"""
The last pattern produced by a solution route must be 5 green tiles for it to be correct. 
"""
def testSoundnessRoute(route, wordList, console) :
    patterns = absurdlev2.testMain(wordList, route)
    if (patterns[-1] != '🟩🟩🟩🟩🟩'):
        return False
    else: 
        return True
    

#SOLVER1V2 
def testSoundnessSolver1(wordListFile, wordList, console):
    routes = solver1v2.getMinLengthRoutes(wordList)
    isSound = testSoundness2(routes, wordListFile, wordList, console)
    return isSound

#SOLVER3V2 

def testSoundnessSolver3(wordListFile, wordList, console) :
    routes = solver3v2.getMinLengthRoutes(wordList)
    isSound = testSoundness2(routes, wordListFile, wordList, console)
    return isSound

# SOLVER4V2
def testSoundnessSolver4(wordListFile, wordList, console) :
    routes = solver4v2.getMinLengthRoutes(wordList)
    isSound = testSoundness2(routes, wordListFile, wordList, console)
    return isSound


def testSolver3SolutionsContainSolver1Solutions(wordListFile, wordList, console):
    routes1 = solver1v2.getMinLengthRoutes(wordList)
    routes3 = solver3v2.getMinLengthRoutes(wordList)
    for route in routes1:
        if route not in routes3:
            console.print(f"{wordListFile}: Solver 3 solutions contain solver 1 solutions: False")
            return False
    console.print(f"{wordListFile}: Solver 3 solutions contain solver 1 solutions: True")
    return True
            
    
def main(solver):
    console = Console()
    for i in range (1, 15):
        n = i * 100
        for j in range (1, 4):
            wordListFile = f"wordlists/{i}00words{j}.txt"
            wordList = absurdlev2.wordsToArray(wordListFile)
            if solver == "solver1v2":
                testSoundnessSolver1(wordListFile, wordList, console)
            elif solver == "solver3v2":
                testSoundnessSolver3(wordListFile, wordList, console)
            elif solver == "solver4v2":
                testSoundnessSolver4(wordListFile, wordList, console)
            elif solver == "3contains1":
                testSolver3SolutionsContainSolver1Solutions(wordListFile, wordList, console)
            else:
                console.print("Invalid Solver")

if __name__ == "__main__":
    main(sys.argv[1]) 