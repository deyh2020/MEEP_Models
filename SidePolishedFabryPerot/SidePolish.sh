#!/bin/bash
#SBATCH -t 3:00:00          
#SBATCH --ntasks=16 

module load meep

 
srun python3 DecayMethod.py -i 0 -o SQRbubblesHiResandLong


