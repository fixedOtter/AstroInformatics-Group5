#!/bin/bash
#SBATCH --job-name=run-python                   # the name of your job
#SBATCH --output=/scratch/gj392/output.txt	# this is the file your output and errors go to
#SBATCH --time=30:00				# 20 min, shorter time, quicker start, max run time 
#SBATCH --chdir=/scratch/gj392			# your work directory
#SBATCH --mem=4000                              # 2GB of memory
#SBATCH --cpus-per-task=4			# i guess -c 4 would do the same thing

# pulling in anaconda module & then activating the conda environment
module load anaconda3
conda activate astroinformatics

# goes and run the main.py file from local dir
srun /home/gj392/astroinformatics/AstroInformatics-Group5/main.py
