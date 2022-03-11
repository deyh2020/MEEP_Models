#!/bin/bash
#SBATCH -t 10:00:00         
#SBATCH --ntasks=48

module load meep

srun python3 ../SidePolishModel/twoDsolve.py 2000 1000 2D_2mm_PAD-1000