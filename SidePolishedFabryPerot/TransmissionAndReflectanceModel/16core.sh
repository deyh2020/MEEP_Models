#!/bin/bash
#SBATCH -t 01:00:00          
#SBATCH --ntasks=16

module load meep

 
srun python3 BulkSingle.py


