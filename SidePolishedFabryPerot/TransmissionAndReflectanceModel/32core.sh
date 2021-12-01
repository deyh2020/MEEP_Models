#!/bin/bash
#SBATCH -t 04:00:00          
#SBATCH --ntasks=32

module load meep

 
srun python3 BulkSingle.py


