#!/bin/bash
#SBATCH -N 1 						#Number of nodes
#SBATCH --ntasks-per-node=1 		#How many cores required. Will checkout many tokens
#SBATCH --job-name=abaqus_test		#Name of slurm job
#SBATCH --time=10:00				#Max time
#SBATCH --mem=4Gb					#Memory requested
#SBATCH --output=log_%j.output		#output log

#Set up directory locations
base_dir="/home/users/lpbrown/RivetOpt"
input_dir="$base_dir/InpFiles"
output_dir="$base_dir/OutputFiles"
scratch_dir="$base_dir/ScratchFiles"

#Input file
job_name="Job-1"
input_file="$job_name.inp"
output_file="$job_name.odb"

#Change to scratch directoy, copy input file
#file out.
cd "$scratch_dir"
cp "$input_dir/$input_file" "$scratch_dir"

#Run the job
#Fix for "<IBM Platform MPI>: : warning, dlopen of libhwloc.so failed (null)/lib/linux_amd64/libhwloc.so: cannot open shared object file: No such file or directory"
unset SLURM_GTIDS
/home/groups/fkchang/SIMULIA_Abaqus_CAE_2019/linux_a64/code/bin/ABQLauncher job="$job_name" input="$input_file" mp_mode=mpi interactive scratch="$scratch_dir"

#Copy output from scratch to outputfiles
#Go back down
cp "$scratch_dir/$output_file" "$output_dir"
cd ..

echo "Reached end of bash script"