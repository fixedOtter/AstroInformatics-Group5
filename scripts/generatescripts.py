# stolen from aiden

templateScript = """
#!/bin/bash
#SBATCH --job-name=calc-rotper{i}                   # the name of your job
#SBATCH --output=/scratch/gj392/attempt{i}/output.txt	# this is the file your output and errors go
#SBATCH --error=/scratch/gj392/attempt{i}/output.err	  # error file
#SBATCH --time=1:00:00			              	# 20 min, shorter time, quicker start, max run time 
#SBATCH --chdir=/scratch/gj392/attempt{i}			        # your work directory
#SBATCH --mem=32768                        # 2GB of memory
#SBATCH --cpus-per-task=32			            # i guess -c 4 would do the same thing
#SBATCH -C amd					                    # makes sure we're using the AMD cpus

# pulling in anaconda module & then activating the conda environment
module load anaconda3
conda activate astroinformatics

# goes and run the main.py file from local dir
srun python3 /home/gj392/astroinformatics/AstroInformatics-Group5/main.py {i}
"""

for i in range(15):
  filename = f"runThatShit{i}.sh"
  with open(filename, "w") as f:
    f.write(templateScript.format(i=i))
  print(f"Created {filename}")