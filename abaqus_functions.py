import numpy as np 

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
from odbAccess import *

#About:
#Helper functions for abaqus that generate parts,
#Apply BC, Apply loads, etc.


##GENERATE PARTS
def generate_facesheet(cellW=110.00, cellL=110.00, loadW=5.00, layup=[0,90,0], t_ply=0.1):
    ##INPUTS

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
    s1.rectangle(point1=(0,0), point2=(cellL, cellW))
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

    #Create surface for applying load
    p = m.parts['CF']
    f, e, d = p.faces, p.edges, p.datums
    s = m.ConstrainedSketch(name='__profile__', sheetSize=200.00)
    s.rectangle(point1=(cellL/2 - loadW/2, 0), point2=(cellL/2 + loadW/2, cellW))
    p.PartitionFaceBySketch(sketchUpEdge=e.findAt(coordinates=(cellL, cellW/2, 0.0)), 
        faces=f.findAt(((0.0, 0.0, 0.0), )), sketch=s)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

    #Assign material orientation
    region = Region(faces=f.findAt(((0.0, 0.0, 0.0), ), ((cellL/2, 0.0, 0.0), ), ((cellL, 0.0, 0.0), )))
    p.MaterialOrientation(region=region, 
        orientationType=GLOBAL, axis=AXIS_3, 
        additionalRotationType=ROTATION_NONE, localCsys=None, fieldName='')

    return True 

def generate_battery(cellL= 110.00, cellW=110.00, frameW=10.00, t_bat=3.00):

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
    m.sketches['__profile__'].rectangle(point1=(0.0, 0.0), point2=(cellL-2*frameW, cellW-2*frameW))
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

def generate_polymer(cellL=110.00, cellW=110.00, frameW=10.00, t_bat=3.00):

    E_poly=600.00;
    nu_poly=0.30;

    m =  mdb.models['Model-1']

    m.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    m.sketches['__profile__'].rectangle(point1=(0.0, 0.0), point2=(cellL, cellW))
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
    s1.rectangle(point1=(frameW, frameW), point2=(cellL-frameW, cellW-frameW))
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

##ASSEMBLY STUFF
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

def define_contact(num_rivets):
    m = mdb.models['Model-1']
    a = m.rootAssembly

    #Define contact property
    contact_prop = m.ContactProperty('NormCont')
    contact_prop.NormalBehavior( allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
        pressureOverclosure=HARD)
    contact_prop.TangentialBehavior(
        dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
        formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
        pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
        table=((0.3, ), ), temperatureDependency=OFF)

    # #Apply contact property to top CF, battery and bot CF, battery
    # m.SurfaceToSurfaceContactStd(adjustMethod=NONE, 
    #     clearanceRegion=None, createStepName='Initial', datumAxis=None, 
    #     initialClearance=OMIT, interactionProperty='NormCont', 
    #     name='CF2Bat',
    #     master=a.instances['CF-2'].surfaces['CFbot'],
    #     slave= a.instances['Battery-1'].surfaces['BatTop'], 
    #     sliding=FINITE, thickness=ON)
    m.Tie(name='CF2Bat', positionToleranceMethod=SPECIFIED, positionTolerance=0.05, adjust=OFF, 
        master= a.instances['CF-2'].surfaces['CFbot'], 
        slave = a.instances['Battery-1'].surfaces['BatTop'], 
        thickness=ON, tieRotations=ON)

    # m.SurfaceToSurfaceContactStd(adjustMethod=NONE, 
    #     clearanceRegion=None, createStepName='Initial', datumAxis=None, 
    #     initialClearance=OMIT, interactionProperty='NormCont', 
    #     name='CF1Bat',
    #     master=a.instances['CF-1'].surfaces['CFtop'],
    #     slave= a.instances['Battery-1'].surfaces['BatBot'], 
    #     sliding=FINITE, thickness=ON)
    m.Tie(name='CF1Bat', positionToleranceMethod=SPECIFIED, positionTolerance=0.05, adjust=OFF, 
        master= a.instances['CF-1'].surfaces['CFtop'], 
        slave = a.instances['Battery-1'].surfaces['BatBot'], 
        thickness=ON, tieRotations=ON)

    #Apply contact property between battery and polymer holes
    for i in range(0,num_rivets):
        # m.SurfaceToSurfaceContactStd(adjustMethod=NONE, 
        #     clearanceRegion=None, createStepName='Initial', datumAxis=None, 
        #     initialClearance=OMIT, interactionProperty='NormCont',
        #     name='BatPoly-'+str(i),
        #     master=a.instances['Polymer-1'].surfaces['Polymer-rivet-'+str(i)], 
        #     slave=a.instances['Battery-1'].surfaces['Battery-rivet-'+str(i)], 
        #     sliding=FINITE, thickness=ON)
        m.Tie(name='BatPoly-'+str(i), positionToleranceMethod=SPECIFIED, positionTolerance=0.05, adjust=OFF, 
            master= a.instances['Polymer-1'].surfaces['Polymer-rivet-'+str(i)], 
            slave = a.instances['Battery-1'].surfaces['Battery-rivet-'+str(i)], 
            thickness=ON, tieRotations=ON)


    #Tie the polymer to the face sheet. Rivets + frame.
    m.Tie(name='CF1Poly',  positionToleranceMethod=SPECIFIED, positionTolerance=0.05, adjust=OFF, 
        master= a.instances['CF-1'].surfaces['CFtop'], 
        slave = a.instances['Polymer-1'].surfaces['PolyBot'], 
        thickness=ON, tieRotations=ON)
    m.Tie(name='CF2Poly',  positionToleranceMethod=SPECIFIED, positionTolerance=0.05, adjust=OFF,
        master= a.instances['CF-2'].surfaces['CFbot'], 
        slave = a.instances['Polymer-1'].surfaces['PolyTop'], 
        thickness=ON, tieRotations=ON)

    for i in range(0,num_rivets):
        print i
        m.Tie(name='CF1Poly-Rivet-'+str(i),  positionToleranceMethod=SPECIFIED, positionTolerance=0.05, adjust=OFF,
            master= a.instances['CF-1'].surfaces['CFtop'], 
            slave = a.instances['Polymer-1'].surfaces['Polymer-rivet-bot-'+str(i)], 
            thickness=ON, tieRotations=ON)
        m.Tie(name='CF2Poly-Rivet-'+str(i),  positionToleranceMethod=SPECIFIED, positionTolerance=0.05, adjust=OFF,
            master= a.instances['CF-2'].surfaces['CFbot'], 
            slave = a.instances['Polymer-1'].surfaces['Polymer-rivet-top-'+str(i)], 
            thickness=ON, tieRotations=ON)
    
    return True

def constrain_assembly(cellL=110.00,cellW=110.00,t_FS=1.0):
    
    #Define a loadstep
    m = mdb.models['Model-1']
    a = m.rootAssembly
    m.StaticStep(name='Loading', previous='Initial')

    ##Sets up 3 point bending constraints
    #Vertical supports
    e = a.instances['CF-1'].edges
    edges = e.findAt(( (0.0, cellW/2, -t_FS/2), ), ((cellL, cellW/2, -t_FS/2), ))
    region = a.Set(edges=edges,name="VerticalSupport")
    m.DisplacementBC(name='VerticalSupport', createStepName='Loading', region=region, 
        u1=UNSET, u2=UNSET, u3=0.0, ur1=UNSET, ur2=UNSET, 
        ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, 
        fieldName='', localCsys=None)

    #Inplane support
    v = a.instances['CF-1'].vertices
    vertices = v.findAt(( (0.0, 0.0, -t_FS/2), ), ( (0.0, cellW, -t_FS/2), ))
    region = a.Set(vertices=vertices, name="XDirSupport")
    m.DisplacementBC(name='XDirSupport', createStepName='Loading', region=region, 
        u1=0.0, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, 
        ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, 
        fieldName='', localCsys=None)

    vertices = v.findAt( ((cellL,0.0,-t_FS/2),) )
    region = a.Set(vertices=vertices, name="YDirSupport")
    m.DisplacementBC(name='YDirSupport', createStepName='Loading', region=region, 
        u1=UNSET, u2=0.0, u3=UNSET, ur1=UNSET, ur2=UNSET, 
        ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, 
        fieldName='', localCsys=None)

    return True

def load_part(cellL=110.00,cellW=110.00,t_bat=3.0, t_FS=1.0, load=100):
    m = mdb.models['Model-1']
    a = m.rootAssembly
    a.regenerate()

    #Apply load
    f = a.instances['CF-2'].faces
    region = Region(side1Faces=f.findAt(((cellL/2, cellW/2, t_bat+t_FS/2),),))
    m.Pressure(name='Load-1', createStepName='Loading', 
        region=region, distributionType=TOTAL_FORCE, field='', magnitude=load, 
        amplitude=UNSET)

    return True

##JOB STUFF
def mesh_part(part_name, deviationFactor=0.1, minSizeFactor=0.1, size=1.50):
    #Generate mesh
    mdb.models['Model-1'].parts[part_name].seedPart(deviationFactor=deviationFactor, 
        minSizeFactor=minSizeFactor, size=size)
    mdb.models['Model-1'].parts[part_name].generateMesh()
    return True

def create_job(name='Job-1', description='',variables=('U','UT','UR')):
    mdb.Job(name=name, model='Model-1', description=description, type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB)
    mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('U', 'UT', 'UR'))
    return True

def write_inp(name='Job-1'):
    mdb.jobs[name].writeInput(consistencyChecking=OFF)
    return True

def run_model(name='Job-1',description=''):
    mdb.jobs[name].submit(consistencyChecking=OFF)
    mdb.jobs[name].waitForCompletion()
    return True

def get_max_min_disp(name='Job-1'):
	odb = openOdb(name+'.odb')
	lastFrame = odb.steps['Loading'].frames[-1]
	dispFieldOutput = lastFrame.fieldOutputs['U']
	dispVals = dispFieldOutput.values
	u3vals = np.zeros((len(dispVals),1))
	for i,d in enumerate(dispVals):
		u3vals[i] = d.data[-1]

	maxu3 = max(u3vals)[0]
	minu3 = min(u3vals)[0]
	return maxu3,minu3