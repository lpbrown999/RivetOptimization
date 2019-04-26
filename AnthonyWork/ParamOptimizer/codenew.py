cellW=110.00;
frameW=10.00;
n=4.00;
r=4.10;

F=500.00;

t_FS=1.00;
E_FS=69000.00;
nu_FS=0.30;
t_rod=2.00;
mesh_FS=4.00;

t_bat=3.00;
E_bat=10.00;
nu_bat=0.30;
mesh_bat=4.00;

E_poly=500.00;
nu_poly=0.30;
mesh_poly=3.00;

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

mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(cellW, cellW))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='CF', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['CF'].BaseSolidExtrude(depth=t_FS, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].Material(name='CF')
mdb.models['Model-1'].materials['CF'].Elastic(table=((30420.0, 4023.0, 4023.0, 
    0.29, 0.29, 0.3928, 2081.0, 2081.0, 1440.0), ), type=ENGINEERING_CONSTANTS)
mdb.models['Model-1'].parts['CF'].Set(cells=
    mdb.models['Model-1'].parts['CF'].cells.getSequenceFromMask(('[#1 ]', ), ), 
    name='CFset')
mdb.models['Model-1'].HomogeneousSolidSection(material='CF', name='CFsec', 
    thickness=None)
mdb.models['Model-1'].parts['CF'].MaterialOrientation(additionalRotationType=
    ROTATION_NONE, axis=AXIS_3, fieldName='', localCsys=None, orientationType=
    GLOBAL, region=mdb.models['Model-1'].parts['CF'].sets['CFset'], 
    stackDirection=STACK_3)
mdb.models['Model-1'].parts['CF'].DatumCsysByThreePoints(coordSysType=CARTESIAN
    , name='Datum csys-1', origin=(0.0, 0.0, 0.0), point1=(0.0, 1.0, 0.0), 
    point2=(1.0, 0.0, 0.0))
mdb.models['Model-1'].parts['CF'].CompositeLayup(description='', elementType=
    SOLID, name='CompositeLayup', symmetric=False, thicknessAssignment=
    FROM_SECTION)
mdb.models['Model-1'].parts['CF'].compositeLayups['CompositeLayup'].ReferenceOrientation(
    additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
    , axis=AXIS_3, fieldName='', localCsys=
    mdb.models['Model-1'].parts['CF'].datums[3], orientationType=SYSTEM, 
    stackDirection=STACK_3)
mdb.models['Model-1'].parts['CF'].compositeLayups['CompositeLayup'].CompositePly(
    additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
    , axis=AXIS_3, material='CF', numIntPoints=1, orientationType=
    SPECIFY_ORIENT, orientationValue=0.0, plyName='Ply-1', region=
    mdb.models['Model-1'].parts['CF'].sets['CFset'], suppressed=False, 
    thickness=0.5, thicknessType=SPECIFY_THICKNESS)
mdb.models['Model-1'].parts['CF'].compositeLayups['CompositeLayup'].CompositePly(
    additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
    , axis=AXIS_3, material='CF', numIntPoints=1, orientationType=
    SPECIFY_ORIENT, orientationValue=90.0, plyName='Ply-2', region=
    mdb.models['Model-1'].parts['CF'].sets['CFset'], suppressed=False, 
    thickness=0.5, thicknessType=SPECIFY_THICKNESS)
mdb.models['Model-1'].parts['CF'].compositeLayups['CompositeLayup'].CompositePly(
    additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
    , axis=AXIS_3, material='CF', numIntPoints=1, orientationType=
    SPECIFY_ORIENT, orientationValue=90.0, plyName='Ply-3', region=
    mdb.models['Model-1'].parts['CF'].sets['CFset'], suppressed=False, 
    thickness=0.5, thicknessType=SPECIFY_THICKNESS)
mdb.models['Model-1'].parts['CF'].compositeLayups['CompositeLayup'].CompositePly(
    additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
    , axis=AXIS_3, material='CF', numIntPoints=1, orientationType=
    SPECIFY_ORIENT, orientationValue=0.0, plyName='Ply-4', region=
    mdb.models['Model-1'].parts['CF'].sets['CFset'], suppressed=False, 
    thickness=0.5, thicknessType=SPECIFY_THICKNESS)
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
mdb.models['Model-1'].Material(name='BatOrtho')
mdb.models['Model-1'].materials['BatOrtho'].Elastic(table=((1090.0, 109.0, 
    500.0, 0.15, 0.15, 0.15, 474.0, 474.0, 474.0), ), type=
    ENGINEERING_CONSTANTS)
mdb.models['Model-1'].parts['Battery'].Set(cells=
    mdb.models['Model-1'].parts['Battery'].cells.getSequenceFromMask(('[#1 ]', 
    ), ), name='Batset')	
mdb.models['Model-1'].HomogeneousSolidSection(material='BatOrtho', name=
    'BatOrtho', thickness=None)
mdb.models['Model-1'].parts['Battery'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Battery'].sets['Batset'], sectionName=
    'BatOrtho', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Battery'].MaterialOrientation(
    additionalRotationType=ROTATION_NONE, axis=AXIS_3, fieldName='', localCsys=
    None, orientationType=GLOBAL, region=
    mdb.models['Model-1'].parts['Battery'].sets['Batset'], stackDirection=
    STACK_3)	
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
    mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].surfaces['PolyBot']
    , name='PolyCF2', positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.instances['CF-2'].surfaces['CFtop'], 
    thickness=ON, tieRotations=ON)

mdb.models['Model-1'].ContactProperty('NormCont')
mdb.models['Model-1'].interactionProperties['NormCont'].NormalBehavior(
    allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
    pressureOverclosure=HARD)
mdb.models['Model-1'].interactionProperties['NormCont'].TangentialBehavior(
    dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
    formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
    pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
    table=((0.3, ), ), temperatureDependency=OFF)
mdb.models['Model-1'].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
    clearanceRegion=None, createStepName='Initial', datumAxis=None, 
    initialClearance=OMIT, interactionProperty='NormCont', master=
    mdb.models['Model-1'].rootAssembly.instances['CF-1'].surfaces['CFbot'], 
    name='CF1Bat', slave=
    mdb.models['Model-1'].rootAssembly.instances['Battery-1'].surfaces['BatTop']
    , sliding=FINITE, thickness=ON)
mdb.models['Model-1'].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
    clearanceRegion=None, createStepName='Initial', datumAxis=None, 
    initialClearance=OMIT, interactionProperty='NormCont', master=
    mdb.models['Model-1'].rootAssembly.instances['Battery-1'].surfaces['BatBot']
    , name='CF2Bat', slave=
    mdb.models['Model-1'].rootAssembly.instances['CF-2'].surfaces['CFtop'], 
    sliding=FINITE, thickness=ON)	

# Create BCs and Load Condition	
	
mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['CF-2'].edges.getSequenceFromMask(
    ('[#22000 ]', ), ), name='BCedges')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='Pin', region=
    mdb.models['Model-1'].rootAssembly.sets['BCedges'], u1=UNSET, u2=UNSET, u3=0, 
    ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].StaticStep(name='Loading', previous='Initial')
mdb.models['Model-1'].rootAssembly.Surface(name='LoadSurf', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['CF-1'].faces.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Loading', 
    distributionType=TOTAL_FORCE, field='', magnitude=F, name='Pressure', 
    region=mdb.models['Model-1'].rootAssembly.surfaces['LoadSurf'])
mdb.models['Model-1'].rootAssembly.ReferencePoint(point=(cellW/2, cellW/2, t_FS))
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
    , numCpus=3, numDomains=90, parallelizationMethodExplicit=DOMAIN, numGPUs=0,
    queue=None, scratch='', type=ANALYSIS, 
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
loadnode = odb.rootAssembly.nodeSets['LOADSET']
loadnodeDisp = displacement.getSubset(region=loadnode)
for v in loadnodeDisp.values:
	myoutfile.write(str(v.data[0]))
	myoutfile.write(' ')
	myoutfile.write(str(v.data[1]))
	myoutfile.write(' ')
	myoutfile.write(str(v.data[2]))
	myoutfile.write("\n")
myoutfile.close()
odb.close()
#