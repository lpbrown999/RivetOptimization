#Idea;
#Write the locations etc in the optimization program to a database file like a .txt or CSV
#Read them in using the script that gets called
#Consider re-rewiting, using shells instead of solids -> done

## todo:
# material orientation for composite
# tying all together
# loading

#session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

# F=150.00;

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


def generate_facesheet(layup=[0,90,0], t_ply=0.1, cellW=110.00):
    ##INPUTS
    #cellW: Width of cell
    #frameW: width of frame
    #t_rod: Thickness of rod that applies 3 point bending load

    E11_FS=30420.00;
    E22_FS=4023.00;
    nu12_FS=0.29;

    G12_FS=2081.00;
    G13_FS=2081.00;
    G23_FS=1440.00;
    
    m = mdb.models['Model-1']

    #Define composite material
    m.Material(name='CF_material')
    m.materials['CF_material'].Elastic(type=LAMINA, table=((E11_FS, E22_FS, nu12_FS, G12_FS, G13_FS, G23_FS), ))

    ply_angles = ()
    for i, angle in enumerate(layup):
        ply_angles = ply_angles + (SectionLayer(material='CF_material', thickness=t_ply, orientAngle=angle,  numIntPts=3),)

    m.CompositeShellSection(name='CF_sec', preIntegrate=OFF, 
        idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM, 
        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
        useDensity=OFF, integrationRule=SIMPSON, layup=ply_angles)

    #Sketch, create shell part
    s1 = m.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    s1.rectangle(point1=(0,0), point2=(cellW, cellW))
    p = m.Part(name='CF', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p.BaseShell(sketch=s1)
    del m.sketches['__profile__']

    #Create set, assign section, surface
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]',),)
    p.Set(faces=faces, name='CF_set')
    p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=
        p.sets['CF_set'], sectionName='CF_sec', thicknessAssignment=FROM_SECTION)

    p.Surface(side1Faces=f.getSequenceFromMask(mask=('[#1 ]', ), ), name='CFtop')
    p.Surface(side2Faces=f.getSequenceFromMask(mask=('[#1 ]', ), ), name='CFbot')

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

    m = mdb.models['Model-1']

    #Sketch batttery
    m.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    m.sketches['__profile__'].rectangle(point1=(0.0, 0.0), point2=(cellW-2*frameW, cellW-2*frameW))
    p = m.Part(dimensionality=THREE_D, name='Battery', type=DEFORMABLE_BODY)

    #Extrude, make surfaces
    p.BaseSolidExtrude(depth=t_bat, sketch= m.sketches['__profile__'])
    p.Surface(name='BatTop', side1Faces= p.faces.getSequenceFromMask(('[#10 ]',), ))
    p.Surface(name='BatBot', side1Faces= p.faces.getSequenceFromMask(('[#20 ]',), ))

    #Define battery materials, assign section
    m.Material(name='BatOrtho')
    m.materials['BatOrtho'].Elastic(table=((E11_bat, E22_bat, 
        E33_bat, nu12_bat, nu13_bat, nu23_bat, G12_bat, G13_bat, G23_bat), ), type=
        ENGINEERING_CONSTANTS)
    p.Set(cells= p.cells.getSequenceFromMask(('[#1 ]',),), name='Batset')    
    m.HomogeneousSolidSection(material='BatOrtho', name='BatOrtho', thickness=None)
    p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=p.sets['Batset'], 
        sectionName='BatOrtho', thicknessAssignment=FROM_SECTION)
    p.MaterialOrientation(additionalRotationType=ROTATION_NONE, axis=AXIS_3, fieldName='', localCsys=None, 
        orientationType=GLOBAL, region=p.sets['Batset'], stackDirection=STACK_3)    

    #Create datum plane, axis for later cutting holes
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)
    p.DatumAxisByThruEdge(edge=p.edges[7])

    return True

def generate_polymer(cellW=110.00, frameW=10.00, t_bat=3.00):

    E_poly=600.00;
    nu_poly=0.30;

    m =  mdb.models['Model-1']

    m.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    m.sketches['__profile__'].rectangle(point1=(0.0, 0.0), point2=(cellW, cellW))
    m.Part(dimensionality=THREE_D, name='Polymer', type= DEFORMABLE_BODY)
    m.parts['Polymer'].BaseSolidExtrude(depth=t_bat, sketch= m.sketches['__profile__'])
    del m.sketches['__profile__']
    p = m.parts['Polymer']


    #Define polymer material
    m.Material(name='Polymer')
    m.materials['Polymer'].Elastic(table=((E_poly, nu_poly), ))
    m.HomogeneousSolidSection(material='Polymer', name=
        'PolySec', thickness=None)
    p.Set(cells=p.cells.getSequenceFromMask(('[#1 ]', ), ), name='PolySet')
    p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=
        p.sets['PolySet'], sectionName='PolySec', thicknessAssignment=FROM_SECTION)

    #Create reference surfaces
    p.Surface(name='PolyTop', side1Faces=mdb.models['Model-1'].parts['Polymer'].faces.getSequenceFromMask(('[#10 ]',),))
    p.Surface(name='PolyBot', side1Faces=mdb.models['Model-1'].parts['Polymer'].faces.getSequenceFromMask(('[#20 ]',),))

    #Datums
    p = mdb.models['Model-1'].parts['Polymer']
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)
    p.DatumAxisByThruEdge(edge=p.edges[7])

    #Cut out the inner rectangle
    s1 = m.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    s1.rectangle(point1=(frameW, frameW), point2=(cellW-frameW, cellW-frameW))
    p.CutExtrude(sketchPlane=p.datums[5], sketchUpEdge=p.datums[6], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=ON)
    del m.sketches['__profile__']

    return True

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

    #Then we add a surface for this rivet to the battery and the polymer
    m = mdb.models['Model-1']
    p = m.parts['Battery']
    p.Surface(side1Faces=p.faces.findAt(((x+r-frameW, y-frameW, t_bat/2), ),), name='Battery-rivet-'+str(rivet_num))

    p = m.parts['Polymer']
    p.Surface(side1Faces=p.faces.findAt(((x+r, y, t_bat/2), ),), name='Polymer-rivet-'+str(rivet_num))

    return True

def mesh_part(part_name, deviationFactor=0.1, minSizeFactor=0.1, size=1.50):
    #Generate mesh
    mdb.models['Model-1'].parts[part_name].seedPart(deviationFactor=deviationFactor, 
        minSizeFactor=minSizeFactor, size=size)
    mdb.models['Model-1'].parts[part_name].generateMesh()
    return True

def assemble(t_FS=1.0, frameW=10.00, t_bat=3.00):
    # session.viewports['Viewport: 1'].assemblyDisplay.setValues(renderShellThickness=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.geometryOptions.setValues(
        datumAxes=OFF, datumPlanes=OFF)

    m = mdb.models['Model-1']
    a = m.rootAssembly

    #Insert polymer
    p = m.parts['Polymer']
    a.Instance(name='Polymer-1', part=p, dependent=ON)

    #Insert battery, translate it to proper location
    p = m.parts['Battery']
    a.Instance(name='Battery-1', part=p, dependent=ON)
    a.translate(instanceList=('Battery-1', ), vector=(frameW, frameW, 0.0))

    #Insert CF facesheet
    #First one goes down by half the FS thickness
    #Second one up by battery thickness + half the FS thickness
    p = m.parts['CF']
    a.Instance(name='CF-1', part=p, dependent=ON)
    a.Instance(name='CF-2', part=p, dependent=ON)
    a.translate(instanceList=('CF-1', ), vector=(0, 0, -t_FS/2))
    a.translate(instanceList=('CF-2', ), vector=(0, 0, t_bat+t_FS/2))

    return True

def constrain():

    ### Define contact property -> TENATIVELY NEED
    contact_prop = m.ContactProperty('NormCont')
    contact_prop.NormalBehavior( allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
        pressureOverclosure=HARD)
    contact_prop.TangentialBehavior(
        dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
        formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
        pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
        table=((0.3, ), ), temperatureDependency=OFF)

    #Apply contact property to top CF, battery. then bot Cf, battery
    m.SurfaceToSurfaceContactStd(adjustMethod=NONE, 
        clearanceRegion=None, createStepName='Initial', datumAxis=None, 
        initialClearance=OMIT, interactionProperty='NormCont', 
        name='CF1Bat',
        master=a.instances['CF-2'].surfaces['CFbot'],
        slave= a.instances['Battery-1'].surfaces['BatTop'], 
        sliding=FINITE, thickness=ON)

    m.SurfaceToSurfaceContactStd(adjustMethod=NONE, 
        clearanceRegion=None, createStepName='Initial', datumAxis=None, 
        initialClearance=OMIT, interactionProperty='NormCont', 
        name='CF1Bat',
        master=a.instances['CF-1'].surfaces['CFtop'],
        slave= a.instances['Battery-1'].surfaces['BatTop'], 
        sliding=FINITE, thickness=ON)

    # #Apply contact property to battery and polymer
    # m.SurfaceToSurfaceContactStd(adjustMethod=NONE, 
    #     clearanceRegion=None, createStepName='Initial', datumAxis=None, 
    #     initialClearance=OMIT, interactionProperty='NormCont',
    #     name='BatPoly',
    #     master=a.instances['Polymer-1'].surfaces['Inner'], 
    #     slave=a.instances['Battery-1'].surfaces['Inner'], 
    #     sliding=FINITE, thickness=ON)
    


    return True
    ### Tie assembly together

cellW = 110.00
frameW = 10.00
t_bat = 3.00

face_layup = [0,90,0]
t_ply = 0.01
t_FS = len(face_layup)*t_ply

generate_facesheet(layup=face_layup, t_ply=t_ply, cellW=cellW)
generate_battery(cellW=cellW, frameW=frameW, t_bat=t_bat)
generate_polymer(cellW=cellW, frameW=frameW, t_bat=t_bat)

#Add the rivets, then add a corresponding surface
add_rivet(x=50,y=50,r=3,rivet_num=1)
add_rivet(x=60,y=30,r=3,rivet_num=2)

# make_rivet_surfaces(2)
#Needs to be done after we make all the rivet holes

mesh_part('CF')
mesh_part('Battery')
mesh_part('Polymer')
assemble(frameW=frameW, t_bat=t_bat, t_FS=t_FS)


# # Tie the assembly together   
#Tie the CF to polymer
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
#Tie the polymer and battery
# #mdb.models['Model-1'].Tie(adjust=ON, master=
# #    mdb.models['Model-1'].rootAssembly.instances['Polymer-1'].surfaces['Inner']
# #    , name='PolyBat', positionToleranceMethod=COMPUTED, slave=
# #    mdb.models['Model-1'].rootAssembly.instances['Battery-1'].surfaces['Inner']
# #    , thickness=ON, tieRotations=ON)


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
#   queue=None, scratch='', type=ANALYSIS, 
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
#   myoutfile.write(str(v.data[0]))
#   myoutfile.write(' ')
#   myoutfile.write(str(v.data[1]))
#   myoutfile.write(' ')
#   myoutfile.write(str(v.data[2]))
#   myoutfile.write("\n")
# myoutfile.close()
# odb.close()
# #