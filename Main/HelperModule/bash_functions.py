def write_generate_inp_script(jobname,scriptname):
	#job -> ex "Job-1"
	#script -> ex abaqus_generate_inp.sh
    with open(scriptname,'w') as fh:

        #Begin script, describe requests to slurm
        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH -N 1\n")
        fh.writelines("#SBATCH --ntasks=1\n")
        fh.writelines("#SBATCH --job-name=inp_%s\n" % jobname)
        fh.writelines("#SBATCH --time=10:00\n")
        fh.writelines("#SBATCH --mem=4Gb\n")
        fh.writelines("#SBATCH --output=./SlurmReports/output=log_%j.output\n")
        
        #fixes for abaqus running on slurm
        fh.writelines("#The follwing are abaqus fixes for slurm\n")
        fh.writelines("unset SLURM_GTIDS\n")
        fh.writelines("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/share/software/user/open/libjpeg-turbo/1.5.1/lib\n")

        #Directory locations
        fh.writelines('base_dir="/home/users/lpbrown/SRCC"\n')
        fh.writelines('input_dir="$base_dir/InpFiles"\n')
        fh.writelines('output_dir="$base_dir/OutputFiles"\n')
        fh.writelines('scratch_dir="$base_dir/ScratchFiles"\n')

        #File names
        fh.writelines('job_name="%s"\n' % jobname)
        fh.writelines('input_file="$job_name.inp"\n')
        fh.writelines('output_file="$job_name.odb"\n')

        #run the input file generation
        fh.writelines("/home/groups/fkchang/SIMULIA_Abaqus_CAE_2019/linux_a64/code/bin/ABQLauncher cae nogui=abaqus_generate_inp.py -- %s\n" % jobname)

        #copy the input file to the input files folder and copy the battery volume to output files.
        fh.writelines('cp "$scratch_dir/$job_name""_bat_vol.npy"  "$output_dir" ')
        fh.writelines('cp "$scratch_dir/$input_file" "$input_dir"\n')

        fh.writelines('echo Completed input file generation.')
        
def write_job_submission_script(jobname,scriptname):
    #job -> ex "Job-1"
    #script -> ex abaqus_job_submit_inp.sh
    with open(scriptname,'w') as fh:

        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH -N 1\n")
        fh.writelines("#SBATCH --ntasks=1\n")
        fh.writelines("#SBATCH --job-name=run_%s\n" % jobname)
        fh.writelines("#SBATCH --time=10:00\n")
        fh.writelines("#SBATCH --mem=8Gb\n")
        fh.writelines("#SBATCH --output=./SlurmReports/output=log_%j.output")
        
        #fixes for abaqus running on slurm
        fh.writelines("#The follwing are abaqus fixes for slurm\n")
        fh.writelines("unset SLURM_GTIDS\n")
        fh.writelines("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/share/software/user/open/libjpeg-turbo/1.5.1/lib\n")

        #Directory locations
        fh.writelines('base_dir="/home/users/lpbrown/SRCC"\n')
        fh.writelines('input_dir="$base_dir/InpFiles"\n')
        fh.writelines('output_dir="$base_dir/OutputFiles"\n')
        fh.writelines('scratch_dir="$base_dir/ScratchFiles"\n')

        #File names
        fh.writelines('job_name="%s"\n' % jobname)
        fh.writelines('input_file="$job_name.inp"\n')
        fh.writelines('output_file="$job_name.odb"\n')

        #Copy the input file to the scratch directory
        fh.writelines('cd "$scratch_dir"\n')
        fh.writelines('cp "$input_dir/$input_file" "$scratch_dir"\n')

        #Run the job
        fh.writelines('/home/groups/fkchang/SIMULIA_Abaqus_CAE_2019/linux_a64/code/bin/ABQLauncher job="$job_name" input="$input_file" mp_mode=mpi interactive scratch="$scratch_dir"\n')

        #Copy the output file to the output directory
        fh.writelines('cp "$scratch_dir/$output_file" "$output_dir"\n')
        fh.writelines('cd ..\n')
        fh.writelines('echo Finished job run.\n')

def write_odb_extraction_script(jobname,scriptname):
    #job -> ex "Job-1"
    #script -> ex abaqus_generate_inp.sh
    with open(scriptname,'w') as fh:

        #Begin script, describe requests to slurm
        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH -N 1\n")
        fh.writelines("#SBATCH --ntasks=1\n")
        fh.writelines("#SBATCH --job-name=odb_%s\n" % jobname)
        fh.writelines("#SBATCH --time=10:00\n")
        fh.writelines("#SBATCH --mem=4Gb\n")
        fh.writelines("#SBATCH --output=./SlurmReports/output=log_%j.output\n")
        
        #fixes for abaqus running on slurm
        fh.writelines("#The follwing are abaqus fixes for slurm\n")
        fh.writelines("unset SLURM_GTIDS\n")
        fh.writelines("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/share/software/user/open/libjpeg-turbo/1.5.1/lib\n")

        #Directory locations
        fh.writelines('base_dir="/home/users/lpbrown/SRCC"\n')
        fh.writelines('input_dir="$base_dir/InpFiles"\n')
        fh.writelines('output_dir="$base_dir/OutputFiles"\n')
        fh.writelines('scratch_dir="$base_dir/ScratchFiles"\n')

        #File names
        fh.writelines('job_name="%s"\n' % jobname)
        fh.writelines('input_file="$job_name.inp"\n')
        fh.writelines('output_file="$job_name.odb"\n')

        #run the input file generation
        fh.writelines("/home/groups/fkchang/SIMULIA_Abaqus_CAE_2019/linux_a64/code/bin/ABQLauncher cae nogui=abaqus_extract_odb.py -- %s\n" % jobname)

        fh.writelines('echo Completed odb extraction.')