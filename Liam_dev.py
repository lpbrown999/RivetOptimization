from helper_functions import *

from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from regionToolset import *

#Idea;
#Write the locations etc in the optimization program to a database file like a .txt or CSV
#Read them in using the script that gets called
#Consider re-rewiting, using shells instead of solids -> done

## todo:
# material orientation for composite
# Examine anthony code to see exactly what is tied vs contact

#session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
load= 0.1;  
loadW = 5.00;

cellL = 200.00
cellW = 110.00
frameW = 10.00
t_bat = 3.00

face_layup = [0,90,0]
t_ply = 0.01
t_FS = len(face_layup)*t_ply

generate_facesheet(cellL=cellL, cellW=cellW, loadW=loadW ,layup=face_layup, t_ply=t_ply)
generate_battery(  cellL=cellL, cellW=cellW, frameW=frameW,    t_bat=t_bat)
generate_polymer(  cellL=cellL, cellW=cellW, frameW=frameW,    t_bat=t_bat)

#Add the rivets, then add a corresponding surface
add_rivet(x=50,y=50,r=3,rivet_num=1)
# add_rivet(x=60,y=30,r=3,rivet_num=2)

#Put the parts together, and then tie / make contact interactions 
#Then constrain the assembly
assemble(frameW=frameW, t_bat=t_bat, t_FS=t_FS)
define_contact(num_rivets=1)
constrain_assembly(cellL=cellL, cellW=cellW, t_FS=t_FS)
load_part(cellL=cellL, cellW=cellW, t_bat=t_bat, t_FS=t_FS, load=load)

mesh_part('CF',      size=15.0)
mesh_part('Battery', size=15.0)
mesh_part('Polymer', size=15.0)

run_model()

# # Output Displacement

# import odbAccess
# odb = session.openOdb('Tension.odb')
# timeFrame = odb.steps['Loading'].frames[1]
# displacement = timeFrame.fieldOutputs['U']
# loadnode = odb.rootAssembly.nodeSets['CONTINUITY']
# loadnodeDisp = displacement.getSubset(region=loadnode)
# for v in loadnodeDisp.values:
#   myoutfile.write(str(v.data[0]))
#   myoutfile.write(' ')
#   myoutfile.write(str(v.data[1]))
#   myoutfile.write(' ')
#   myoutfile.write(str(v.data[2]))
#   myoutfile.write("\n")
# myoutfile.close()
# odb.close()
# #