import TwoDimensionTR.TwoDsolve as TwoDsolve
import sys

print ('Argument List:', str(sys.argv))

Solver = TwoDsolve.TwoDsolve()

try:
    Solver.M.GAP = float(sys.argv[1])
except:
    print("That didn't work")


Solver.run()