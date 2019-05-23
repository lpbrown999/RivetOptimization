#!/bin/bash
#SBATCH -N 1 							#Number of nodes
#SBATCH --ntasks=1 						#How many cores required. Will checkout many tokens
#SBATCH --job-name=abaqus_rivet_main	#Name of slurm job
#SBATCH --time=1:00:00					#Max time
#SBATCH --mem=512Mb						#Memory requested
#SBATCH --output=./SlurmReports/log_%j.output			#output log

python3 main.py
