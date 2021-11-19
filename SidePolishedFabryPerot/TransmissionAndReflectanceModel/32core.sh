#!/bin/bash
#SBATCH -t 00:45:00          
#SBATCH --ntasks=32

module load meep

 
srun python3 RunBulkExperiment.py


