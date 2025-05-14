#!/bin/bash
#SBATCH --job-name=run-python                   # the name of your job
#SBATCH --output=/scratch/gj392/output.txt	# this is the file your output and errors go to
#SBATCH --time=6:00				# 20 min, shorter time, quicker start, max run time 
#SBATCH --chdir=/scratch/gj392			# your work directory
#SBATCH --mem=1000                              # 2GB of memory

# load a module, for example
# module load anaconda3

# run your application, precede the application command with srun
# a couple example applications ...
srun something.py
