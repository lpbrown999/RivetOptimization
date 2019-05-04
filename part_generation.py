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