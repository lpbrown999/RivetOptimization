#PYTHON 2 SINCE CALLED BY ABAQUS
import numpy as np
import os
import sys
import csv
import time

from HelperModule.abaqus_functions import *

def abaqus_run_job(jobname,xs,ys,rs):
    ## Inputs: vector x location, y location, r size of the 
    # rivets. Must all be the same length (num rivets long)

    ## Global definitions of the part
    #  Material definitions are in the abaqus_functions file

    #New model
    Mdb()
    mesh_size = 3.0

    #Load to be applied (3 point bending)
    #and the width of strip it is applied to
    load = 100 
    loadW = 5.00

    #Cell sizing
    cellL = 110.00
    cellW = 110.00
    frameW = 10.00
    t_bat = 5.00

    #Face sheet layups
    face_layup = [0,90,90,0]
    t_ply = 0.2
    t_FS = len(face_layup)*t_ply

    #generate parts, add rivets
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

    #Create job, write inp, run it, save cae
    # create_job(name=jobname, variables=('U','UT','UR','EVOL'))
    # write_inp(name=jobname)
    # run_model(name=jobname)?

    # #Sleep to let abaqus finish cleaning up the model that just ran before we query it
    # time.sleep(5)

    # #Extract needed values
    # maxu3,minu3 = get_max_min_disp(name=jobname)
    # delta = max(abs(np.array([maxu3,minu3])))
    # G = simple_sandwich_theory_G(delta, cellW=cellW, cellL=cellL, layup=face_layup, t_ply=t_ply, t_bat=t_bat, load=load)
    # battery_volume = get_part_volume('Battery')

    # return [battery_volume, G]

if __name__ == "__main__":

    vec = np.genfromtxt(os.getcwd()+'/InpFiles/input_vec.csv', delimiter=',')[-1]
    os.chdir('ScratchFiles')
    total_length = len(vec)
    n = int(total_length/3)
    
    xs = vec[0*n:1*n]
    ys = vec[1*n:2*n]
    rs = vec[2*n:3*n]

    jobname = sys.argv[-1]
    output_vec = abaqus_run_job(jobname,xs,ys,rs)
    os.chdir('..')

    # #Save input vector to be accessed by abaqus
    # with open(os.getcwd()+'/OutputFiles/output_vec.csv', mode='a+') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(output_vec)
    # sys.exit()
