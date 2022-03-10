import TwoDimensionModeSolving.TwoDsolve as TwoDsolve
import sys

print ('Argument List:', str(sys.argv))

Solver = TwoDsolve.TwoDsolve()

arg3 = ""

try:
    Solver.M.GAP = float(sys.argv[1])
    Solver.M.filename = str(sys.argv[2])
except:
    print("That didn't work")

try: 
    arg3 = str(sys.argv[3])
except:
    print("No worries, no extra args")


print("argument3" + str(arg3))


if arg3 == "justplot":
    print("Just plotting")
    Solver.pltStructure()
else:
    print("Normal run")
    Solver.run()