import TwoDimensionTR.TwoDsolve as TwoDsolve
import sys

print ('Argument List:', str(sys.argv))

Solver = TwoDsolve.TwoDsolve()

try:
    Solver.M.GAP = float(sys.argv[1])
    Solver.M.filename = str(sys.argv[2])
except:
    print("That didn't work")


Solver.run()