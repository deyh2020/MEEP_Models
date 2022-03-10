#!/bin/bash
#SBATCH -t 10:00:00         
#SBATCH --ntasks=32

module load meep

srun python3 ../SidePolishModel/twoDsolve.py 500 2D_500um_PAD-1000
