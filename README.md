### AA290 - MESC Polymer Rivet Optimization using Abaqus + Python

## Descriptions
	1. main.py is the main script, called by python main.py
			abaqus_evaluation is the penalized objective function that is optimized
			Since we always minimize, it currently returns the -battery_volume + a penalty on violated constraints
	2. abaqus_script.py is the script that is called by abaqus to construct and run a model configuration
	3. HelperModule containts three files with functions that assist in different tasks
			abaqus_functions.py contains wrappers for abaqus functionality for making MESC cells
			optimization_functions.py contains the nelder-mead, quadratic penalty, optimize, and simplex generation
			helper_functions.py contains misc functions (get job name etc)
	4. optimization_config.ini is a config file where parameters can be changed

## How it works
	1. In main.py, the config file is read, the working directories (OutputFiles, InpFiles, ScratchFiles) are cleared, and /Outputfiles/output_vec.csv and /InpFiles/inp_vec.csv are made
	2. the function "optimize" from the helpermodule.optimization_functions is called on the abaqus_evaluation function
	3. this runs nelder mead on the objective function.
			nelder-mead requries many function evaluations
	4. within each function evaluation (abaqus_evaluation), an input vector and penalty are given. 
			* the input vector is decoded (number of rivets, x,y,r of 1:num_rivets_max)
			* the configuration is loaded from the config file
			* a job name is grabbed (sequentially from ScratchFiles)
			* n,x,y,r are clipped / modified to make sure they are viable.
			* an input vector is saved
			*** A subprocess is started that calls abaqus cae with no gui and the abaqus_script.py
					* Within the abaqus_script.py, the input vector is read from the csv where it was saved
					* The model is constructed
					* the job is run
					* the desired quantities (battery volume, G) are extracted and saved to the output csv
	5. As nelder-mead runs, it adjusts the simplex based on the different function evaluations. 
	6. Once it has run, plot_script.py provides a starting idea for how to plot the output information


## Usage
	1. Specify optimization parameters, constraints, geometry, mesh size, job details in
		optimization_config.ini
	2. from main directory, run "python main.py"

## Todo
	1. Currently G is computed using beam theory and should be switched to advanced sandwich theory
	2. More parameters?
	3. Pareto Frontier?
	4. Mesh convergence study?
