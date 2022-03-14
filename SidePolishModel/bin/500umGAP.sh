#!/bin/bash
#SBATCH -t 07:00:00         
#SBATCH --ntasks=32

module load meep

srun python3 ../SidePolishModel/twoDsolve.py 500 1000 500um_SquareDips squaredips
