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
    point2=(500.0, 50.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=1.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].Material(name='FS')
mdb.models['Model-1'].materials['FS'].Elastic(table=((70000.0, 0.3), ))
mdb.models['Model-1'].parts['Part-1'].Set(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.getSequenceFromMask(('[#1 ]', 
    ), ), name='CFset')
mdb.models['Model-1'].HomogeneousSolidSection(material='FS', name='FSsec', 
    thickness=None)
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['CFset'], sectionName='FSsec', 
    thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=2.0)
mdb.models['Model-1'].parts['Part-1'].generateMesh()
mdb.models['Model-1'].parts['Part-1'].deleteMesh()
mdb.models['Model-1'].parts['Part-1'].deleteSeeds()
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=25.12, name='__profile__', 
    sheetSize=1004.98, transform=
    mdb.models['Model-1'].parts['Part-1'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces[4], 
    sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['Model-1'].parts['Part-1'].edges[7], 
    sketchOrientation=RIGHT, origin=(250.0, 25.0, 1.0)))
mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-1.0, -25.0), 
    point2=(1.0, 25.0))
mdb.models['Model-1'].parts['Part-1'].PartitionFaceBySketch(faces=
    mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(('[#10 ]', 
    ), ), sketch=mdb.models['Model-1'].sketches['__profile__'], sketchUpEdge=
    mdb.models['Model-1'].parts['Part-1'].edges[7])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=2.0)
mdb.models['Model-1'].parts['Part-1'].generateMesh()
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(500.0, 50.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Poly', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Poly'].BaseSolidExtrude(depth=10.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].Material(name='Poly')
mdb.models['Model-1'].materials['Poly'].Elastic(table=((500.0, 0.3), ))
mdb.models['Model-1'].parts['Poly'].Set(cells=
    mdb.models['Model-1'].parts['Poly'].cells.getSequenceFromMask(('[#1 ]', ), 
    ), name='Polyset')
mdb.models['Model-1'].HomogeneousSolidSection(material='Poly', name='Polysec', 
    thickness=None)
mdb.models['Model-1'].parts['Poly'].SectionAssignment(offset=0.0, offsetField=
    '', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Poly'].sets['Polyset'], sectionName='Polysec', 
    thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Poly'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=2.0)
mdb.models['Model-1'].parts['Poly'].generateMesh()
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Poly-1', part=
    mdb.models['Model-1'].parts['Poly'])
mdb.models['Model-1'].rootAssembly.instances['Poly-1'].translate(vector=(0, 
    0.0, -10.0))
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-2', 
    part=mdb.models['Model-1'].parts['Part-1'])
mdb.models['Model-1'].rootAssembly.instances['Part-1-2'].translate(vector=(0.0, 
    0.0, -11.0))
mdb.models['Model-1'].parts['Part-1'].Surface(name='FStop', side1Faces=
    mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(('[#43 ]', 
    ), ))
mdb.models['Model-1'].parts['Part-1'].Surface(name='FSbot', side1Faces=
    mdb.models['Model-1'].parts['Part-1'].faces.getSequenceFromMask(('[#80 ]', 
    ), ))
mdb.models['Model-1'].parts['Poly'].Surface(name='Polytop', side1Faces=
    mdb.models['Model-1'].parts['Poly'].faces.getSequenceFromMask(('[#10 ]', ), 
    ))
mdb.models['Model-1'].parts['Poly'].Surface(name='Polybot', side1Faces=
    mdb.models['Model-1'].parts['Poly'].faces.getSequenceFromMask(('[#20 ]', ), 
    ))
mdb.models['Model-1'].rootAssembly.regenerate()
mdb.models['Model-1'].Tie(adjust=ON, master=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].surfaces['FSbot'], 
    name='Top', positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.instances['Poly-1'].surfaces['Polytop'], 
    thickness=ON, tieRotations=ON)
mdb.models['Model-1'].Tie(adjust=ON, master=
    mdb.models['Model-1'].rootAssembly.instances['Poly-1'].surfaces['Polybot'], 
    name='Bot', positionToleranceMethod=COMPUTED, slave=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-2'].surfaces['FStop'], 
    thickness=ON, tieRotations=ON)
mdb.models['Model-1'].rootAssembly.ReferencePoint(point=(250.0, 25.0, 1.0))
mdb.models['Model-1'].rootAssembly.Surface(name='LoadSurf', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.getSequenceFromMask(
    ('[#2 ]', ), ), name='LoadSurf')
mdb.models['Model-1'].RigidBody(name='RigidLoad', refPointRegion=Region(
    referencePoints=(mdb.models['Model-1'].rootAssembly.referencePoints[8], )), 
    surfaceRegion=None, tieRegion=
    mdb.models['Model-1'].rootAssembly.sets['LoadSurf'])
mdb.models['Model-1'].StaticStep(name='Loading', previous='Initial')
mdb.models['Model-1'].rootAssembly.Surface(name='Load', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.getSequenceFromMask(
    ('[#2 ]', ), ))
mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Loading', 
    distributionType=TOTAL_FORCE, field='', magnitude=500.0, name='Press', 
    region=mdb.models['Model-1'].rootAssembly.surfaces['Load'])
mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-2'].edges.getSequenceFromMask(
    ('[#8100 ]', ), ), name='BC')
mdb.models['Model-1'].ZsymmBC(createStepName='Loading', localCsys=None, name=
    'BC', region=mdb.models['Model-1'].rootAssembly.sets['BC'])
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='c393test', nodalOutputPrecision=SINGLE, 
    numCpus=1, numGPUs=0, queue=None, scratch='', type=ANALYSIS, 
    userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['c393test'].submit(consistencyChecking=OFF)

myoutfile = open('C:/Users/Bombik/Documents/School/GradSchool/AeroAstroMasters/SACL/ParamOptimizer/Results/c393.txt','w+');

import odbAccess
odb = session.openOdb('c393test.odb')
timeFrame = odb.steps['Loading'].frames[1]
displacement = timeFrame.fieldOutputs['U']
loadnode = odb.rootAssembly.nodeSets['LOADSURF']
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
