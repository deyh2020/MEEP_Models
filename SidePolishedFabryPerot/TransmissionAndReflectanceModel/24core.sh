#!/bin/bash
#SBATCH -t 4:00:00         
#SBATCH --ntasks=24

module load meep

 
srun python3 WholeFibre.py


