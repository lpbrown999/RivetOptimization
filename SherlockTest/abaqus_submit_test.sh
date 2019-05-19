#!/bin/bash
#Set up resources
#SBATCH -N 1 						#Number of nodes
#SBATCH --ntasks-per-node=1 		#How many cores required. Will checkout many tokens
#SBATCH --job-name=abaqus_test		#Name of slurm job
#SBATCH --time=10:00				#Max time
#SBATCH --mem=4G					#Memory requested
#SBATCH --output=log_%j.output		#output log

#Fix for "<IBM Platform MPI>: : warning, dlopen of libhwloc.so failed (null)/lib/linux_amd64/libhwloc.so: cannot open shared object file: No such file or directory"
unset SLURM_GTIDS

#Run the job
/home/groups/fkchang/SIMULIA_Abaqus_CAE_2019/linux_a64/code/bin/ABQLauncher job=Job-1 input=Job-1.inp mp_mode=mpi interactive scratch=. 

#When done, copy ODB from execution directory to where we started from
echo "Reached end of bash script"