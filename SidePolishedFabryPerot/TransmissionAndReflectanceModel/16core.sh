#!/bin/bash
#SBATCH -t 03:00:00          
#SBATCH --ntasks=16

module load meep

 
srun python3 TimeSteppingDebug.py


