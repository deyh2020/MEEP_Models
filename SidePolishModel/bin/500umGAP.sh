#!/bin/bash
#SBATCH -t 06:00:00         
#SBATCH --ntasks=32

module load meep

srun python3 ../SidePolishModel/twoDsolve.py 500 2D_GAP-500um_PAD-1000_allRHS
