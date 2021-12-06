#!/bin/bash
#SBATCH -t 5:00:00          
#SBATCH --ntasks=24

module load meep

 
srun python3 BulkSingle.py


