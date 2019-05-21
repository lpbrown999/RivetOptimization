#PYTHON 2 SINCE CALLED BY ABAQUS
import numpy as np
import os
import sys
from HelperModule.abaqus_functions import *

def abaqus_generate_inp(jobname,xs,ys,rs):
    ## Inputs: vector x location, y location, r size of the 
    # rivets. Must all be the same length (num rivets long)

    ## Global definitions of the part
    #  Material definitions are in the abaqus_functions file

    #New model
    Mdb()
    mesh_size = 10.0

    #Load to be applied (3 point bending)
    #and the width of strip it is applied to
    load= 10  
    loadW = 5.00

    #Cell sizing
    cellL = 220.00
    cellW = 110.00
    frameW = 10.00
    t_bat = 3.00

    #Clip the input rivet locations so they are valid (within the battery)
    dist_tol = 1.0                                                  #Due to meshing
    rs = np.clip(rs,dist_tol,min(cellL/4,cellW/4))                  #Rivets cannot be bigger than half of the shortest dimension
    xs = np.clip(xs-rs,frameW+rs+dist_tol,cellL-frameW-rs-dist_tol) #Cannot be inside polymer at all
    ys = np.clip(ys-rs,frameW+rs+dist_tol,cellW-frameW-rs-dist_tol)

    #Face sheet layups
    face_layup = [0,90,0]
    t_ply = 0.01
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

    #Create job, write inp
    create_job(name=jobname)
    write_inp(name=jobname)

    #Save npy file with job name to pass back to main script
    # os.chdir("..")
    # np.save("jobname",jobname)

 	#Run model, return min and max displacements
    # run_model(name=jobname)
    # maxu3,minu3 = get_max_min_disp(name=jobname)
    # return max(abs(maxu3),abs(minu3))
    return True

if __name__ == "__main__":
    os.chdir("/home/users/lpbrown/SRCC/ScratchFiles/")
    xs = np.load("xs.npy")
    ys = np.load("ys.npy")
    rs = np.load("rs.npy")
    jobname = sys.argv[-1]
    abaqus_generate_inp(jobname,xs,ys,rs)

