#PYTHON 2 SINCE CALLED BY ABAQUS
import numpy as np
import os
import sys
import csv
import time
import ConfigParser

from HelperModule.abaqus_functions import *
from HelperModule.helper_functions import read_full_csv

def abaqus_run_job(jobname,xs,ys,rs):
	## Inputs: vector x location, y location, r size of the 
	# rivets. Must all be the same length (num rivets long)

	#Get info from config
	config = ConfigParser.ConfigParser()
 	config.read('optimization_config.ini')

 	mesh_size = float(config.get('Abaqus','mesh_size'))
 	num_cores = int(float(config.get('Abaqus','num_cores')))
 	memory    = int(float(config.get('Abaqus','memory')))
	load      = float(config.get('CellGeometry','load'))
	loadW     = float(config.get('CellGeometry','loadW'))
	cellL     = float(config.get('CellGeometry','cellL'))
	cellW     = float(config.get('CellGeometry','cellW'))
	frameW    = float(config.get('CellGeometry','frameW'))
	t_bat     = float(config.get('CellGeometry','t_bat'))

	#Face sheet layups
	face_layup = [0,90,90,0]
	t_ply = 0.2
	t_FS = len(face_layup)*t_ply

	#Move into scratch files, start a new model, generate parts
	os.chdir('ScratchFiles')
	Mdb()
	generate_facesheet(cellL=cellL, cellW=cellW, loadW=loadW,   layup=face_layup, t_ply=t_ply)
	generate_battery(  cellL=cellL, cellW=cellW, frameW=frameW, t_bat=t_bat)
	generate_polymer(  cellL=cellL, cellW=cellW, frameW=frameW, t_bat=t_bat)

	#Add the rivets, then add a corresponding surface
	num_rivets = len(xs)
	for i in range(0,num_rivets):
		add_rivet(x=xs[i],y=ys[i],r=rs[i], rivet_num=i, t_bat=t_bat, frameW=frameW)

	#Put the parts together, and then tie / make contact interactions 
	#Then constrain the assembly
	assemble(frameW=frameW, t_bat=t_bat, t_FS=t_FS)
	define_contact(num_rivets=num_rivets)
	constrain_assembly(cellL=cellL, cellW=cellW, t_FS=t_FS)
	load_part(cellL=cellL, cellW=cellW, t_bat=t_bat, t_FS=t_FS, load=load)

	#Mesh everything
	mesh_part('CF',      size=mesh_size)
	mesh_part('Battery', size=mesh_size)
	mesh_part('Polymer', size=mesh_size)

	# Create job, write inp, run it, save cae
	create_job(name=jobname, variables=('U','UT','UR','EVOL','RF'), num_cores=num_cores, memory=memory)
	write_inp(name=jobname)
	run_model(name=jobname)
	save_cae(name=jobname)

	#Sleep to let abaqus finish cleaning up the model that just ran before we query it
	time.sleep(5)

	#Extract needed values
	maxu3,minu3 = get_max_min_disp(name=jobname)
	delta = max(abs(np.array([maxu3,minu3])))
	G = simple_sandwich_theory_G(delta, cellW=cellW, cellL=cellL, layup=face_layup, t_ply=t_ply, t_bat=t_bat, load=load)
	battery_volume = get_part_volume('Battery')
	
	os.chdir('..')
	return [jobname, battery_volume, G]

if __name__ == "__main__":

	data = read_full_csv(os.getcwd()+'/InpFiles/input_vec.csv')
	jobname = data[-1][0]
	inpvec = data[-1][1:]

	num_rivets = int(inpvec[0])
	xs = inpvec[1::3]
	xs = [float(x) for x in xs]

	ys = inpvec[2::3]
	ys = [float(y) for y in ys]

	rs = inpvec[3::3]
	rs = [float(r) for r in rs]

	output_vec = abaqus_run_job(jobname,xs,ys,rs)

	#Save input vector to be accessed by abaqus
	with open(os.getcwd()+'/OutputFiles/output_vec.csv', mode='a+') as f:
		writer = csv.writer(f)
		writer.writerow(output_vec)
	sys.exit()
