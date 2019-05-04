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
    for i in range(1,num_rivets+1):
        # m.SurfaceToSurfaceContactStd(adjustMethod=NONE, 
        #     clearanceRegion=None, createStepName='Initial', datumAxis=None, 
        #     initialClearance=OMIT, interactionProperty='NormCont',
        #     name='BatPoly-'+str(i),
        #     master=a.instances['Polymer-1'].surfaces['Polymer-rivet-'+str(i)], 
        #     slave=a.instances['Battery-1'].surfaces['Battery-rivet-'+str(i)], 
        #     sliding=FINITE, thickness=ON)
        m.Tie(name='CF1Bat', positionToleranceMethod=SPECIFIED, positionTolerance=0.05, adjust=OFF, 
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

    for i in range(1,num_rivets+1):
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

def mesh_part(part_name, deviationFactor=0.1, minSizeFactor=0.1, size=1.50):
    #Generate mesh
    mdb.models['Model-1'].parts[part_name].seedPart(deviationFactor=deviationFactor, 
        minSizeFactor=minSizeFactor, size=size)
    mdb.models['Model-1'].parts[part_name].generateMesh()
    return True

def run_model(name='Job-1',description=''):
    #Create the job
    mdb.Job(name=name, model='Model-1', description=description, type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB)
    #Set our output requests
    mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('U', 'UT', 'UR'))
    mdb.jobs[name].submit(consistencyChecking=OFF)
    mdb.jobs[name].waitForCompletion()
    return True