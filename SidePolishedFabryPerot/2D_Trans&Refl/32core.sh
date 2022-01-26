#!/bin/bash
#SBATCH -t 6:00:00          
#SBATCH --ntasks=32

module load meep

 
srun python3 PolishedFibre.py

srun python3 WholeFibre.py


