TO PLAY GUI VERSION OF ABSURDLE AND ABSURDL-SCORED:

python3 ./absurdleandabsurdlescoredgui.py


TO PLAY COMMAND LINE VERSION OF ABSURDLE:

python3 ./absurdlev2.py


TO RUN TESTS FOR COMMAND LINE VERSION OF ABSURDLE:

python3 ./testabsurdlev2.py


TO PLAY COMMAND LINE VERSION OF ABSURDLE-SCORED:

python3 ./absurdlescoredcl.py


TO EVALUATE THE PERFORMANCE OF THE SOLVERS ON DIFFERENT WORD LISTS (CPU TIME, NUMBER OF ROUTES, MINIMUM LENGTH OF ROUTES):
for solver1v2:
python3 ./algorithmEvaluator.py solver1v2

for solver3v2:
python3 ./algorithmEvaluator.py solver3v2

for solver4v2: 
python3 ./algorithmEvaluator.py solver4v2


TO RUN solver1v2 ON A GIVEN WORDLIST:

python3 ./solver1v2.py wordlists/{wordlist file e.g. 100words1}.txt


TO RUN solver3v2 ON A GIVEN WORDLIST:

python3 ./solver3v2.py wordlists/{wordlist file e.g. 100words1}.txt


TO RUN solver4v2 ON A GIVEN WORDLIST:

python3 ./solver4v2.py wordlists/{wordlist file e.g. 100words1}.txt


TO TEST SOUNDNESS OF A SOLVER:
for solver1v2:
python3 ./testingSolversv2.py solver1v2

for solver3v2:
python3 ./testingSolversv2.py solver3v2

for solver4v2:
python3 ./testingSolversv2.py solver4v2

TO TEST solver3v2 CONTAINS SOLUTIONS FOUND BY solver1v2:
python3 ./testingSolversv2.py 3contains1





