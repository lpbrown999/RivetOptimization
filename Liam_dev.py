#Idea;
#Write the locations etc in the optimization program to a database file like a .txt or CSV
#Read them in using the script that gets called
#Consider re-rewiting, using shells instead of solids

# #Dimensioning
# cellW=110.00;
# frameW=10.00;


# F=150.00;


# E_poly=600.00;
# nu_poly=0.30;
# mesh_poly=1.50;


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

F=150.00;   

def generate_facesheet(cellW=110.00, frameW=10.00, t_rod=2.00):
    ##INPUTS
    #cellW: Width of cell
    #frameW: width of frame
    #t_rod: Thickness of rod that applies 3 point bending load

    #Face Sheet Properties
    t_FS=0.80;
    E11_FS=30420.00;
    E22_FS=4023.00;
    E33_FS=4023.00;
    nu12_FS=0.29;
    nu13_FS=0.29;
    nu23_FS=0.39;
    G12_FS=2081.00;
    G13_FS=2081.00;
    G23_FS=1440.00;

    #Begin sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(cellW, cellW))
    #Extrude Body
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='CF', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['CF'].BaseSolidExtrude(depth=t_FS, sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']

    #Define Material, Set
    mdb.models['Model-1'].Material(name='CF')
    mdb.models['Model-1'].materials['CF'].Elastic(table=((E11_FS, E22_FS, E33_FS, 
        nu12_FS, nu13_FS, nu23_FS, G12_FS, G13_FS, G23_FS), ), type=ENGINEERING_CONSTANTS)
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
    
    #Define layup
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

    #Other sketch not sure whats going on
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
    return True 

def generate_battery(cellW=110.00, frameW=10.00, t_bat=3.00):

    E11_bat=1090.00;
    E22_bat=1090.00;
    E33_bat=500.00;
    nu12_bat=0.15;
    nu13_bat=0.15;
    nu23_bat=0.15;
    G12_bat=474.00;
    G13_bat=474.00;
    G23_bat=474.00;

    #Sketch batttery
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(cellW-2*frameW, cellW-2*frameW))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Battery', type=
        DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Battery']

    #Extrude, make surfaces
    p.BaseSolidExtrude(depth=t_bat, sketch= mdb.models['Model-1'].sketches['__profile__'])
    p.Surface(name='BatTop', side1Faces= mdb.models['Model-1'].parts['Battery'].faces.getSequenceFromMask(('[#10 ]',), ))
    p.Surface(name='BatBot', side1Faces= mdb.models['Model-1'].parts['Battery'].faces.getSequenceFromMask(('[#20 ]',), ))
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=6.36, name='__profile__', 
        sheetSize=254.62, transform=
        mdb.models['Model-1'].parts['Battery'].MakeSketchTransform(
        sketchPlane=mdb.models['Model-1'].parts['Battery'].faces[4], 
        sketchPlaneSide=SIDE1, 
        sketchUpEdge=mdb.models['Model-1'].parts['Battery'].edges[7], 
        sketchOrientation=RIGHT, origin=((cellW-2*frameW)/2.0, (cellW-2*frameW)/2.0, t_bat)))

    #Define battery materials
    mdb.models['Model-1'].Material(name='BatOrtho')
    mdb.models['Model-1'].materials['BatOrtho'].Elastic(table=((E11_bat, E22_bat, 
        E33_bat, nu12_bat, nu13_bat, nu23_bat, G12_bat, G13_bat, G23_bat), ), type=
        ENGINEERING_CONSTANTS)
    p.Set(cells= mdb.models['Model-1'].parts['Battery'].cells.getSequenceFromMask(('[#1 ]',),), name='Batset')    
    mdb.models['Model-1'].HomogeneousSolidSection(material='BatOrtho', name=
        'BatOrtho', thickness=None)
    p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=p.sets['Batset'], 
        sectionName='BatOrtho', thicknessAssignment=FROM_SECTION)
    p.MaterialOrientation(additionalRotationType=ROTATION_NONE, axis=AXIS_3, fieldName='', localCsys=None, 
        orientationType=GLOBAL, region=p.sets['Batset'], stackDirection=STACK_3)    

    #Create datum plane, axis for later cutting holes
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)
    p.DatumAxisByThruEdge(edge=p.edges[7])

def polymer(cellW=110.00, frameW=10.00, t_bat=3.00):

    E_poly=600.00;
    nu_poly=0.30;

    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
        point2=(cellW, cellW))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Polymer', type=
        DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Polymer'].BaseSolidExtrude(depth=t_bat, sketch=
        mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']

    #Define polymer material
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

    #Surfaces
    mdb.models['Model-1'].parts['Polymer'].Surface(name='PolyTop', side1Faces=
        mdb.models['Model-1'].parts['Polymer'].faces.getSequenceFromMask(('[#10 ]', 
        ), ))
    mdb.models['Model-1'].parts['Polymer'].Surface(name='PolyBot', side1Faces=
        mdb.models['Model-1'].parts['Polymer'].faces.getSequenceFromMask(('[#20 ]', 
        ), ))

    #?
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

    #Datum stuff
    p = mdb.models['Model-1'].parts['Polymer']
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)
    p.DatumAxisByThruEdge(edge=p.edges[7])

    # #Cuts out the linear pattern of rivets
    # mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    #     -cellW/2+frameW+(cellW-2*frameW)/(n+1), -cellW/2+frameW+(cellW-2*frameW)/
    #     (n+1)), point1=(-cellW/2+frameW+(cellW-2*frameW)/(n+1)+r, -cellW/2+frameW+
    #     (cellW-2*frameW)/(n+1)))

    # mdb.models['Model-1'].sketches['__profile__'].linearPattern(angle1=0.0, angle2=
    #     90.0, geomList=(mdb.models['Model-1'].sketches['__profile__'].geometry[10], 
    #     ), number1=int(n), number2=int(n), spacing1=(cellW-2*frameW)/(n+1), spacing2=(cellW-2
    #     *frameW)/(n+1), vertexList=())
    # mdb.models['Model-1'].parts['Polymer'].CutExtrude(flipExtrudeDirection=OFF, 
    #     sketch=mdb.models['Model-1'].sketches['__profile__'], sketchOrientation=
    #     RIGHT, sketchPlane=mdb.models['Model-1'].parts['Polymer'].faces[4], 
    #     sketchPlaneSide=SIDE1, sketchUpEdge=
    #     mdb.models['Model-1'].parts['Polymer'].edges[7])

    # mdb.models['Model-1'].parts['Polymer'].Surface(name='Inner', side1Faces=
    #     mdb.models['Model-1'].parts['Polymer'].faces.getSequenceFromMask((
    #     '[#ffffffff:2 #ffffffff ]', ), ))
    # del mdb.models['Model-1'].sketches['__profile__']


def cut_rivet_hole(part_name,x,y,r):
    #Part
    p  = mdb.models['Model-1'].parts[part_name]

    #Sketch
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    s1.CircleByCenterPerimeter(center=(x,y), point1=(x+r,y))

    #Cut
    p.CutExtrude(sketchPlane=p.datums[5], sketchUpEdge=p.datums[6], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)


def mesh_part(part_name, deviationFactor=0.1, minSizeFactor=0.1, size=1.50):
    #Generate mesh
    mdb.models['Model-1'].parts[part_name].seedPart(deviationFactor=deviationFactor, 
        minSizeFactor=minSizeFactor, size=size)
    mdb.models['Model-1'].parts[part_name].generateMesh()
    return True



generate_facesheet()
generate_battery()
polymer()

cut_rivet_hole(part_name="Battery",x=10,y=10,r=3)
cut_rivet_hole(part_name="Battery",x=20,y=10,r=3)
cut_rivet_hole(part_name="Polymer",x=10,y=10,r=3)
cut_rivet_hole(part_name="Polymer",x=20,y=10,r=3)

mesh_part('CF')
mesh_part('Battery')
mesh_part('Polymer')


# # Making the Assembly	
	
# mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='CF-1', part=
#     mdb.models['Model-1'].parts['CF'])
# mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Battery-1', 
#     part=mdb.models['Model-1'].parts['Battery'])
# mdb.models['Model-1'].rootAssembly.instances['Battery-1'].translate(vector=(
#     frameW, frameW, -t_bat))
# mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Polymer-1', 
#     part=mdb.models['Model-1'].parts['Polymer'])
# mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].translate(vector=(
#     0.0, 0.0, -t_bat))
# mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='CF-2', part=
#     mdb.models['Model-1'].parts['CF'])
# mdb.models['Model-1'].rootAssembly.instances['CF-2'].translate(vector=(0.0, 
#     0.0, -(t_FS+t_bat)))
# mdb.models['Model-1'].parts['Polymer'].Surface(name='PolyInside', side1Faces=
#     mdb.models['Model-1'].parts['Polymer'].faces.getSequenceFromMask(('[#1 ]', 
#     ), ))

# # Tie the assembly together	
	
# mdb.models['Model-1'].Tie(adjust=ON, master=
#     mdb.models['Model-1'].rootAssembly.instances['CF-1'].surfaces['CFbot'], 
#     name='CF1Poly', positionToleranceMethod=COMPUTED, slave=
#     mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].surfaces['PolyTop']
#     , thickness=ON, tieRotations=ON)
# mdb.models['Model-1'].Tie(adjust=ON, master=
#     mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].surfaces['PolyBot']
#     , name='PolyCF2', positionToleranceMethod=COMPUTED, slave=
#     mdb.models['Model-1'].rootAssembly.instances['CF-2'].surfaces['CFtop'], 
#     thickness=ON, tieRotations=ON)
# #mdb.models['Model-1'].Tie(adjust=ON, master=
# #    mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].surfaces['Inner']
# #    , name='PolyBat', positionToleranceMethod=COMPUTED, slave=
# #    mdb.models['Model-1'].rootAssembly.instances['Battery-1'].surfaces['Inner']
# #    , thickness=ON, tieRotations=ON)

# mdb.models['Model-1'].ContactProperty('NormCont')
# mdb.models['Model-1'].interactionProperties['NormCont'].NormalBehavior(
#     allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
#     pressureOverclosure=HARD)
# mdb.models['Model-1'].interactionProperties['NormCont'].TangentialBehavior(
#     dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
#     formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
#     pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
#     table=((0.3, ), ), temperatureDependency=OFF)
# mdb.models['Model-1'].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
#     clearanceRegion=None, createStepName='Initial', datumAxis=None, 
#     initialClearance=OMIT, interactionProperty='NormCont', master=
#     mdb.models['Model-1'].rootAssembly.instances['CF-1'].surfaces['CFbot'], 
#     name='CF1Bat', slave=
#     mdb.models['Model-1'].rootAssembly.instances['Battery-1'].surfaces['BatTop']
#     , sliding=FINITE, thickness=ON)
# mdb.models['Model-1'].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
#     clearanceRegion=None, createStepName='Initial', datumAxis=None, 
#     initialClearance=OMIT, interactionProperty='NormCont', master=
#     mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].surfaces['Inner'], 
#     name='BatPoly', slave=
#     mdb.models['Model-1'].rootAssembly.instances['Battery-1'].surfaces['Inner']
#     , sliding=FINITE, thickness=ON)
# mdb.models['Model-1'].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
#     clearanceRegion=None, createStepName='Initial', datumAxis=None, 
#     initialClearance=OMIT, interactionProperty='NormCont', master=
#     mdb.models['Model-1'].rootAssembly.instances['Battery-1'].surfaces['BatBot']
#     , name='CF2Bat', slave=
#     mdb.models['Model-1'].rootAssembly.instances['CF-2'].surfaces['CFtop'], 
#     sliding=FINITE, thickness=ON)	

# # Create BCs and Load Condition	
	
# mdb.models['Model-1'].rootAssembly.Surface(name='TensionZone', side1Faces=
#     mdb.models['Model-1'].rootAssembly.instances['CF-2'].faces.getSequenceFromMask(
#     mask=('[#8 ]', ), )+\
#     mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].faces.getSequenceFromMask(
#     mask=('[#20 ]', ), )+\
#     mdb.models['Model-1'].rootAssembly.instances['CF-1'].faces.getSequenceFromMask(
#     mask=('[#8 ]', ), ))
# mdb.models['Model-1'].rootAssembly.Set(faces=
#     mdb.models['Model-1'].rootAssembly.instances['CF-1'].faces.getSequenceFromMask(
#     mask=('[#20 ]', ), )+\
#     mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].faces.getSequenceFromMask(
#     mask=('[#80 ]', ), )+\
#     mdb.models['Model-1'].rootAssembly.instances['CF-2'].faces.getSequenceFromMask(
#     mask=('[#20 ]', ), ), name='BC')
# mdb.models['Model-1'].rootAssembly.Set(faces=
#     mdb.models['Model-1'].rootAssembly.instances['CF-1'].faces.getSequenceFromMask(
#     mask=('[#8 ]', ), )+\
#     mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].faces.getSequenceFromMask(
#     mask=('[#20 ]', ), )+\
#     mdb.models['Model-1'].rootAssembly.instances['CF-2'].faces.getSequenceFromMask(
#     mask=('[#8 ]', ), ), name='continuity')
# mdb.models['Model-1'].rootAssembly.ReferencePoint(point=(cellW/2, cellW/2, t_FS))
# mdb.models['Model-1'].RigidBody(name='Constraint', refPointRegion=Region(
#     referencePoints=(mdb.models['Model-1'].rootAssembly.referencePoints[12], ))
#     , tieRegion=mdb.models['Model-1'].rootAssembly.sets['continuity'])
# mdb.models['Model-1'].StaticStep(name='Loading', previous='Initial')
# mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='Loading', 
#     distributionType=TOTAL_FORCE, field='', magnitude=-F, name='Tension', 
#     region=mdb.models['Model-1'].rootAssembly.surfaces['TensionZone'])
# mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Loading', 
#     distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
#     'Fixed', region=mdb.models['Model-1'].rootAssembly.sets['BC'], u1=0.0, u2=
#     0.0, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)
# mdb.models['Model-1'].steps['Loading'].setValues(adaptiveDampingRatio=0.05, 
#     continueDampingFactors=False, stabilizationMagnitude=0.0002, 
#     stabilizationMethod=DISSIPATED_ENERGY_FRACTION)
	
	
# # Create the Job	
	
# mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
#     explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
#     memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
#     multiprocessingMode=DEFAULT, name='Tension', nodalOutputPrecision=SINGLE, 
#     numCpus=3, numDomains=90, parallelizationMethodExplicit=DOMAIN, numGPUs=0, 
# 	queue=None, scratch='', type=ANALYSIS, 
#     userSubroutine='', waitHours=0, waitMinutes=0)
# mdb.models['Model-1'].rootAssembly.regenerate()
# mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
#     'U', 'UT', 'UR'))	
	
	
# # Run Job	

# mdb.jobs['Tension'].submit(consistencyChecking=OFF)
# mdb.jobs['Tension'].waitForCompletion()

# # Output Displacement

# import odbAccess
# odb = session.openOdb('Tension.odb')
# timeFrame = odb.steps['Loading'].frames[1]
# displacement = timeFrame.fieldOutputs['U']
# loadnode = odb.rootAssembly.nodeSets['CONTINUITY']
# loadnodeDisp = displacement.getSubset(region=loadnode)
# for v in loadnodeDisp.values:
# 	myoutfile.write(str(v.data[0]))
# 	myoutfile.write(' ')
# 	myoutfile.write(str(v.data[1]))
# 	myoutfile.write(' ')
# 	myoutfile.write(str(v.data[2]))
# 	myoutfile.write("\n")
# myoutfile.close()
# odb.close()
# #