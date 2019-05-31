# -*- coding: mbcs -*-
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

cellW=110.0;
frameW=10.0;

#rivet pattern n by n
n=4.0;
r=2.0;

F=500.0;

t_FS=1.0;
E_FS=69000.0;
nu_FS=.3;
t_rod=2.0;
mesh_FS=2.0;

t_bat=3.0;
E_bat=10.0;
nu_bat=.3;
mesh_bat=2.0;

E_poly=500.0;
nu_poly=.3;
mesh_poly=r/2;

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(cellW, cellW))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='CF', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['CF'].BaseSolidExtrude(depth=t_FS, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].Material(name='CF')
mdb.models['Model-1'].materials['CF'].Elastic(table=((E_FS, nu_FS), ))
mdb.models['Model-1'].parts['CF'].Set(cells=
    mdb.models['Model-1'].parts['CF'].cells.getSequenceFromMask(('[#1 ]', ), ), 
    name='CFset')
mdb.models['Model-1'].HomogeneousSolidSection(material='CF', name='CFsec', 
    thickness=None)
mdb.models['Model-1'].parts['CF'].SectionAssignment(offset=0.0, offsetField='', 
    offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['CF'].sets['CFset'], sectionName='CFsec', 
    thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=7.77, name='__profile__', 
    sheetSize=311.13, transform=
    mdb.models['Model-1'].parts['CF'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['CF'].faces[4], 
    sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['Model-1'].parts['CF'].edges[7], 
    sketchOrientation=RIGHT, origin=(cellW/2, cellW/2, t_FS)))
mdb.models['Model-1'].parts['CF'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-cellW/2, -t_rod/2), 
    point2=(cellW/2, t_rod/2))
mdb.models['Model-1'].parts['CF'].PartitionFaceBySketch(faces=
    mdb.models['Model-1'].parts['CF'].faces.getSequenceFromMask(('[#10 ]', ), )
    , sketch=mdb.models['Model-1'].sketches['__profile__'], sketchUpEdge=
    mdb.models['Model-1'].parts['CF'].edges[7])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].parts['CF'].Surface(name='CFtop', side1Faces=
    mdb.models['Model-1'].parts['CF'].faces.getSequenceFromMask(('[#43 ]', ), 
    ))
mdb.models['Model-1'].parts['CF'].Surface(name='CFbot', side1Faces=
    mdb.models['Model-1'].parts['CF'].faces.getSequenceFromMask(('[#80 ]', ), 
    ))
mdb.models['Model-1'].parts['CF'].seedPart(deviationFactor=0.1, minSizeFactor=
    0.1, size=mesh_FS)
mdb.models['Model-1'].parts['CF'].generateMesh()


#Make Battery Part

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(cellW-2*frameW, cellW-2*frameW))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Battery', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Battery'].BaseSolidExtrude(depth=t_bat, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].parts['Battery'].Surface(name='BatTop', side1Faces=
    mdb.models['Model-1'].parts['Battery'].faces.getSequenceFromMask(('[#10 ]', 
    ), ))
mdb.models['Model-1'].parts['Battery'].Surface(name='BatBot', side1Faces=
    mdb.models['Model-1'].parts['Battery'].faces.getSequenceFromMask(('[#20 ]', 
    ), ))
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=6.36, name='__profile__', 
    sheetSize=254.62, transform=
    mdb.models['Model-1'].parts['Battery'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['Battery'].faces[4], 
    sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['Model-1'].parts['Battery'].edges[7], 
    sketchOrientation=RIGHT, origin=((cellW-2*frameW)/2.0, (cellW-2*frameW)/2.0, t_bat)))
mdb.models['Model-1'].parts['Battery'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    -(cellW-2*frameW)/2.0+(cellW-2*frameW)/(n+1), -(cellW-2*frameW)/2.0+(cellW-2*frameW)/
	(n+1)), point1=(-(cellW-2*frameW)/2.0+(cellW-2*frameW)/(n+1)+r, -(cellW-2*frameW)/2.0
	+(cellW-2*frameW)/(n+1)))
mdb.models['Model-1'].sketches['__profile__'].linearPattern(angle1=0.0, angle2=
    90.0, geomList=(mdb.models['Model-1'].sketches['__profile__'].geometry[6], 
    ), number1=int(n), number2=int(n), spacing1=(cellW-2*frameW)/(n+1), spacing2=(cellW-
	2*frameW)/(n+1), vertexList=())
mdb.models['Model-1'].parts['Battery'].CutExtrude(flipExtrudeDirection=OFF, 
    sketch=mdb.models['Model-1'].sketches['__profile__'], sketchOrientation=
    RIGHT, sketchPlane=mdb.models['Model-1'].parts['Battery'].faces[4], 
    sketchPlaneSide=SIDE1, sketchUpEdge=
    mdb.models['Model-1'].parts['Battery'].edges[7])
mdb.models['Model-1'].Material(name='BatteryHomo')
mdb.models['Model-1'].materials['BatteryHomo'].Elastic(table=((E_bat, nu_bat), ))
mdb.models['Model-1'].parts['Battery'].Set(cells=
    mdb.models['Model-1'].parts['Battery'].cells.getSequenceFromMask(('[#1 ]', 
    ), ), name='Batset')
mdb.models['Model-1'].HomogeneousSolidSection(material='BatteryHomo', name=
    'BatHomoSec', thickness=None)
mdb.models['Model-1'].parts['Battery'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Battery'].sets['Batset'], sectionName=
    'BatHomoSec', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Battery'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=mesh_bat)
mdb.models['Model-1'].parts['Battery'].generateMesh()


#Make Polymer Surface

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(cellW, cellW))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Polymer', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Polymer'].BaseSolidExtrude(depth=t_bat, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].Material(name='Polymer')
mdb.models['Model-1'].materials['Polymer'].Elastic(table=((E_poly, nu_poly), ))
mdb.models['Model-1'].HomogeneousSolidSection(material='Polymer', name=
    'PolySec', thickness=None)
mdb.models['Model-1'].parts['Polymer'].Set(cells=
    mdb.models['Model-1'].parts['Polymer'].cells.getSequenceFromMask(('[#1 ]', 
    ), ), name='PolySet')
mdb.models['Model-1'].parts['Polymer'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Polymer'].sets['PolySet'], sectionName=
    'PolySec', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Polymer'].Surface(name='PolyTop', side1Faces=
    mdb.models['Model-1'].parts['Polymer'].faces.getSequenceFromMask(('[#10 ]', 
    ), ))
mdb.models['Model-1'].parts['Polymer'].Surface(name='PolyBot', side1Faces=
    mdb.models['Model-1'].parts['Polymer'].faces.getSequenceFromMask(('[#20 ]', 
    ), ))
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=7.77, name='__profile__', 
    sheetSize=311.18, transform=
    mdb.models['Model-1'].parts['Polymer'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['Polymer'].faces[4], 
    sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['Model-1'].parts['Polymer'].edges[7], 
    sketchOrientation=RIGHT, origin=(cellW/2, cellW/2, t_bat)))
mdb.models['Model-1'].parts['Polymer'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-cellW/2+frameW,
	-cellW/2+frameW), point2=(cellW/2-frameW, cellW/2-frameW))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    -cellW/2+frameW+(cellW-2*frameW)/(n+1), -cellW/2+frameW+(cellW-2*frameW)/
	(n+1)), point1=(-cellW/2+frameW+(cellW-2*frameW)/(n+1)+r, -cellW/2+frameW+
	(cellW-2*frameW)/(n+1)))
mdb.models['Model-1'].sketches['__profile__'].linearPattern(angle1=0.0, angle2=
    90.0, geomList=(mdb.models['Model-1'].sketches['__profile__'].geometry[10], 
    ), number1=int(n), number2=int(n), spacing1=(cellW-2*frameW)/(n+1), spacing2=(cellW-2
	*frameW)/(n+1), vertexList=())
mdb.models['Model-1'].parts['Polymer'].CutExtrude(flipExtrudeDirection=OFF, 
    sketch=mdb.models['Model-1'].sketches['__profile__'], sketchOrientation=
    RIGHT, sketchPlane=mdb.models['Model-1'].parts['Polymer'].faces[4], 
    sketchPlaneSide=SIDE1, sketchUpEdge=
    mdb.models['Model-1'].parts['Polymer'].edges[7])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].parts['Polymer'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=mesh_poly)
mdb.models['Model-1'].parts['Polymer'].generateMesh()


# Making the Assembly	
	
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='CF-1', part=
    mdb.models['Model-1'].parts['CF'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Battery-1', 
    part=mdb.models['Model-1'].parts['Battery'])
mdb.models['Model-1'].rootAssembly.instances['Battery-1'].translate(vector=(
    frameW, frameW, -t_bat))
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Polymer-1', 
    part=mdb.models['Model-1'].parts['Polymer'])
mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].translate(vector=(
    0.0, 0.0, -t_bat))
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='CF-2', part=
    mdb.models['Model-1'].parts['CF'])
mdb.models['Model-1'].rootAssembly.instances['CF-2'].translate(vector=(0.0, 
    0.0, -(t_FS+t_bat)))
mdb.models['Model-1'].parts['Polymer'].Surface(name='PolyInside', side1Faces=
    mdb.models['Model-1'].parts['Polymer'].faces.getSequenceFromMask(('[#1 ]', 
    ), ))

# Tie the assembly together	
	
mdb.models['Model-1'].Tie(adjust=ON, master=
    mdb.models['Model-1'].rootAssembly.instances['CF-1'].surfaces['CFbot'], 
    name='CF1Poly', positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].surfaces['PolyTop']
    , thickness=ON, tieRotations=ON)
mdb.models['Model-1'].Tie(adjust=ON, master=
    mdb.models['Model-1'].rootAssembly.instances['CF-1'].surfaces['CFbot'], 
    name='CF1Bat', positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.instances['Battery-1'].surfaces['BatTop']
    , thickness=ON, tieRotations=ON)
mdb.models['Model-1'].Tie(adjust=ON, master=
    mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].surfaces['PolyBot']
    , name='PolyCF2', positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.instances['CF-2'].surfaces['CFtop'], 
    thickness=ON, tieRotations=ON)
mdb.models['Model-1'].Tie(adjust=ON, master=
    mdb.models['Model-1'].rootAssembly.instances['CF-2'].surfaces['CFtop']
    , name='BatCF2', positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.instances['Battery-1'].surfaces['BatBot'], 
    thickness=ON, tieRotations=ON)	

# Create BCs and Load Condition	
	
mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['CF-2'].edges.getSequenceFromMask(
    ('[#22000 ]', ), ), name='BCedges')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='Pin', region=
    mdb.models['Model-1'].rootAssembly.sets['BCedges'], u1=SET, u2=SET, u3=SET, 
    ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].StaticStep(name='Loading', previous='Initial')
mdb.models['Model-1'].rootAssembly.Surface(name='LoadSurf', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['CF-1'].faces.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Loading', 
    distributionType=TOTAL_FORCE, field='', magnitude=F, name='Pressure', 
    region=mdb.models['Model-1'].rootAssembly.surfaces['LoadSurf'])
mdb.models['Model-1'].rootAssembly.ReferencePoint(point=
    mdb.models['Model-1'].rootAssembly.instances['CF-1'].InterestingPoint(
    mdb.models['Model-1'].rootAssembly.instances['CF-1'].edges[6], MIDDLE))
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['CF-1'].faces.getSequenceFromMask(
    ('[#2 ]', ), ), name='LoadSet')
mdb.models['Model-1'].RigidBody(name='RigidDeform', refPointRegion=Region(
    referencePoints=(mdb.models['Model-1'].rootAssembly.referencePoints[11], ))
    , tieRegion=mdb.models['Model-1'].rootAssembly.sets['LoadSet'])
	
	
# Create the Job	
	
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='3PointBend', nodalOutputPrecision=SINGLE
    , numCpus=1, numGPUs=0, queue=None, scratch='', type=ANALYSIS, 
    userSubroutine='', waitHours=0, waitMinutes=0)
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'U', 'UT', 'UR'))	
	
	
# Run Job	

mdb.jobs['3PointBend'].submit(consistencyChecking=OFF)


# Output Displacement

import odbAccess
odb = session.openOdb('3PointBend.odb')
timeFrame = odb.steps['Loading'].frames[1]
displacement = timeFrame.fieldOutputs['U']
loadnode = odb.rootAssembly.nodeSets[' ALL NODES']
loadnodeDisp = displacement.getSubset(region=loadnode)
myoutfile = open('C:/Users/Bombik/Documents/School/GradSchool/AeroAstroMasters/SACL/ParamOptimizer/result.txt','w+')
for v in loadnodeDisp.values:
	myoutfile.write(str(v.data[0]))
	myoutfile.write(' ')
	myoutfile.write(str(v.data[1]))
	myoutfile.write(' ')
	myoutfile.write(str(v.data[2]))
	myoutfile.write("\n")
myoutfile.close()
odb.close()