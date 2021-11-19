#!/bin/bash
#SBATCH -t 02:00:00          
#SBATCH --ntasks=64

module load meep

 
srun python3 RunBulkExperiment.py


