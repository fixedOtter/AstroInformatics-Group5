#!/bin/bash
#SBATCH --job-name=calc-rotper6                   # the name of your job
#SBATCH --output=/scratch/gj392/attempt6/output.txt	# this is the file your output and errors go
#SBATCH --error=/scratch/gj392/attempt6/output.err	  # error file
#SBATCH --time=3:00:00			              	# 20 min, shorter time, quicker start, max run time 
#SBATCH --chdir=/scratch/gj392/attempt6			        # your work directory
#SBATCH --mem=16384                        # 2GB of memory
#SBATCH --cpus-per-task=28			            # i guess -c 4 would do the same thing

# pulling in anaconda module & then activating the conda environment
module load anaconda3
conda activate astroinformatics

# goes and run the main.py file from local dir
srun python3 /home/gj392/astroinformatics/AstroInformatics-Group5/main.py 6
