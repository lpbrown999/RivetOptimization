from assembly_generation import *
from part_generation import *
from rivet_generation import *
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


### Rivet functions
def cut_battery_rivet_hole(x,y,r):
    m = mdb.models['Model-1']
    p = m.parts["Battery"]

    #Sketch
    s1 = m.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    s1.CircleByCenterPerimeter(center=(x,y), point1=(x+r,y))

    #Cut
    p.CutExtrude(sketchPlane=p.datums[5], sketchUpEdge=p.datums[6], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)

    del m.sketches['__profile__']
    return True

def add_polymer_rivet(x,y,r, t_bat):
    m = mdb.models['Model-1']
    p = m.parts["Polymer"]
    #Sketch
    s1 = m.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    s1.CircleByCenterPerimeter(center=(x,y), point1=(x+r,y))
    #Extrude
    p.SolidExtrude(sketchPlane=p.datums[5], sketchUpEdge=p.datums[6], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1, depth=t_bat, flipExtrudeDirection=OFF)
    


    del m.sketches['__profile__']
    return True

def add_rivet(x,y,r,rivet_num,t_bat=3.00,frameW=10.00):
    
    #First we cut the battery, then extrude for the polymer
    cut_battery_rivet_hole(x-frameW,y-frameW,r)
    add_polymer_rivet(x,y,r,t_bat=t_bat)

    #Then we add a surface for the rivet to the battery and polymer. These are on the sides
    m = mdb.models['Model-1']
    p = m.parts['Battery']
    p.Surface(side1Faces=p.faces.findAt(((x+r-frameW, y-frameW, t_bat/2), ),), name='Battery-rivet-'+str(rivet_num))

    p = m.parts['Polymer']
    p.Surface(side1Faces=p.faces.findAt(((x+r, y, t_bat/2), ),), name='Polymer-rivet-'+str(rivet_num))

    #And lastly we add surfaces to the top and bottom of the rivet for tying to the face sheets
    p = m.parts['Polymer']
    p.Surface(side1Faces=p.faces.findAt(((x, y, t_bat), ),), name='Polymer-rivet-top-'+str(rivet_num))
    p.Surface(side1Faces=p.faces.findAt(((x, y,     0), ),), name='Polymer-rivet-bot-'+str(rivet_num))

    #And actually lastly add material to the rivets
    c = p.cells
    cells = c.findAt(((x, y, t_bat/2), ))
    region = Region(cells=cells)
    p.SectionAssignment(region=region, sectionName='PolySec', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

    return True