#!/bin/bash
#SBATCH -t 01:00:00          
#SBATCH --ntasks=64

module load meep

 
srun python3 RunModel.py


