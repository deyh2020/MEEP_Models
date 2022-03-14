#!/bin/bash
#SBATCH -t 07:00:00         
#SBATCH --ntasks=32

module load meep

srun python3 ../SidePolishModel/twoDsolve.py 500 1000 2D_GAP-500um_PAD-1000_allRHS
