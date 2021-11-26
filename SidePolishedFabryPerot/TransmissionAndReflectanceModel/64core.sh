#!/bin/bash
#SBATCH -t 04:00:00          
#SBATCH --ntasks=64

module load meep

 
srun python3 RunBulkExperiment.py


