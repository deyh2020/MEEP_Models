#!/bin/bash
#SBATCH -t 3:00:00          
#SBATCH --ntasks=16 

module load meep

 
srun python3 Test.py


