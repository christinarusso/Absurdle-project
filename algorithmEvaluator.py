import solver1v2
import solver3v2
import solver4v2
import sys
from rich.console import Console

solvers = {
    "solver1v2": solver1v2,
    "solver3v2": solver3v2,
    "solver4v2": solver4v2,
}

def main(solver):
    console = Console()  
    if solver in solvers: 
        for i in range (1, 15): # evaluates wordlists of length 100 up to 1400 (steps of 100) 
            n = i * 100
            for j in range (1, 4): # evaluates three word lists of same length so average can later be computed 
                solvers[solver].runForAlgorithmEvaluation(f"wordlists/{n}words{j}.txt")
    else:
        console.print(solver)
        console.print("Invalid solver name")

if __name__ == "__main__":
    main(sys.argv[1]) 