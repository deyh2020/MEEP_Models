#!/bin/bash
#SBATCH -t 1:00:00         
#SBATCH --ntasks=24

module load meep

 
srun python3 PolishedFibre.py


