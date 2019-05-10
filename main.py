import numpy as np
import os
from abaqus_functions import *
from optimization_functions import *

#Todo:
#Run abaqus from within python script rather than claling this from the command line


#As anthony said, want to optimize over just the rivet x, y, r
def abaqus_evaluation_deflection(xs,ys,rs):
    ## Inputs: vector x location, y location, r location of the 
    # rivets. Must all be the same length (num rivets long)

    ## Global definitions of the part
    #Material definitions are in the abaqus_functions file
    #Idea: add material properties to a config file, pass in what material
    #through the configf

    #Dont pollute my directory
    #Make a new model, 
    #And then get new job number
    os.chdir(r"C:\Users\lpbro\gitrepos\RivetOptimization\JobFiles")
    Mdb()
    mylist = [item for item in os.listdir(os.getcwd()) if item.endswith(".odb")] 
    myints = [int(re.findall(r'\b\d+\b',item)[0]) for item in mylist]
    jobname = "Job-"+str(max(myints)+1)


    #Load to be applied (3 point bending)
    #and the width of strip it is applied to
    load= 10;  
    loadW = 5.00;

    #Cell sizing
    cellL = 220.00
    cellW = 110.00
    frameW = 10.00
    t_bat = 3.00

    #Clip the input rivet locations so they are valid (within the battery)
    dist_tol = 1.0      #Due to meshing
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
    mesh_part('CF',      size=15.0)
    mesh_part('Battery', size=15.0)
    mesh_part('Polymer', size=15.0)

    #Analyze
    create_job(name=jobname)
    run_model(name=jobname)

    maxu3,minu3 = get_max_min_disp(name=jobname)
    return max(abs(maxu3),abs(minu3))

def abaqus_evaluation_deflection_vec(vec):
    #Runs abaquas eval with vector input
    total_length = len(vec)
    n = total_length/3
    xs = vec[0:n]
    ys = vec[n:2*n]
    rs = vec[2*n:3*n]
    return abaqus_evaluation_deflection(xs,ys,rs)

def optimize(f,c,ndim,neval):
    xmin = 0
    xmax = 220
    ymin = 0
    ymax = 100
    rmin = 0
    rmax = 15

    S = np.random.random_sample((ndim+1,ndim))
    
    #Assumes only 1 rivet for now
    S[:,0] = S[:,0]*(xmax-xmin) + xmin
    S[:,1] = S[:,1]*(ymax-ymin) + ymin
    S[:,2] = S[:,2]*(rmax-rmin) + rmin

    S,best = nelder_mead(f,S,neval)
    return best

# xs = np.array([1000.0])
# ys = np.array([-10.0])
# rs = np.array([5.0])

best = optimize(abaqus_evaluation_deflection_vec, None, 3, 10)
