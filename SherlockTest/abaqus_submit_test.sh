#!/bin/bash
#Set up resources
#SBATCH -N 1 						#Node count
#SBATCH --ntasks-per-node=1			#threads
#SBATCH --job-name=abaqus_test		#Name of slurm job
#SBATCH --time=10:00				#Max time
#SBATCH --ntasks=1					
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH -o process_%j.out
#SBATCH -e process_%j.err

#Change to execution directory
#Run job
#Fix for "<IBM Platform MPI>: : warning, dlopen of libhwloc.so failed (null)/lib/linux_amd64/libhwloc.so: cannot open shared object file: No such file or directory"
# unset LD_LIBRARY_PATH
# unset SLURM_GTIDS

srun /home/groups/fkchang/SIMULIA_Abaqus_CAE_2019/linux_a64/code/bin/ABQLauncher job=Job-1 input=Job-1 scratch=. interactive 

#When done, copy ODB from execution directory to where we started from
yourfilenames="ls ./*.*"
for eachfile in $yourfilenames
do
   echo $eachfile
done