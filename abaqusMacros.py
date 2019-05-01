# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def cuthole():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    p = mdb.models['Model-1'].parts['Battery']
    f, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f[5], sketchUpEdge=e[9], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(44.858437, 
        45.212344, 3.0))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=254.55, gridSpacing=6.36, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['Battery']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.CircleByCenterPerimeter(center=(-30.21, 1.59), point1=(-22.26, 7.95))
    p = mdb.models['Model-1'].parts['Battery']
    f1, e1 = p.faces, p.edges
    p.CutExtrude(sketchPlane=f1[5], sketchUpEdge=e1[9], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=OFF)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']


def datumplane():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    p = mdb.models['Model-1'].parts['Battery']
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)



def datumaxis2():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    p = mdb.models['Model-1'].parts['Battery']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=222.598, 
        farPlane=353.692, width=122.396, height=99.3417, cameraPosition=(
        240.582, -10.9401, 205.605), cameraUpVector=(-0.37311, 0.918378, 
        0.131799))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=203.924, 
        farPlane=373.229, width=112.128, height=91.0083, cameraPosition=(
        207.481, -157.664, 127.263), cameraUpVector=(-0.0548293, 0.804929, 
        0.590833), cameraTarget=(47.5737, 44.8822, -0.947556))
    p = mdb.models['Model-1'].parts['Battery']
    e = p.edges
    p.DatumAxisByThruEdge(edge=e[7])


def Macro1():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=233.605, 
        farPlane=403.877, width=154.535, height=125.427, viewOffsetX=7.4312, 
        viewOffsetY=7.11193)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=205.804, 
        farPlane=413.938, width=136.143, height=110.5, cameraPosition=(
        -169.452, -150.084, 61.889), cameraUpVector=(0.70268, -0.0681519, 
        0.708235), cameraTarget=(59.7113, 66.2822, 5.99289), 
        viewOffsetX=6.5468, viewOffsetY=6.26553)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=208.53, 
        farPlane=411.211, width=137.947, height=111.964, cameraPosition=(
        -169.104, -151.409, 58.184), cameraUpVector=(0.549498, 0.124555, 
        0.826159), cameraTarget=(60.0588, 64.957, 2.28788), 
        viewOffsetX=6.63351, viewOffsetY=6.34852)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=242.947, 
        farPlane=385.829, width=160.715, height=130.443, cameraPosition=(
        -114.972, -35.8674, 249.897), cameraUpVector=(0.875107, 0.371346, 
        0.310305), cameraTarget=(56.3869, 59.1344, -3.21321), 
        viewOffsetX=7.72835, viewOffsetY=7.39632)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=239.385, 
        farPlane=389.39, width=158.359, height=128.531, cameraPosition=(
        -115.373, -41.532, 247.499), cameraUpVector=(0.63858, 0.716864, 
        0.279859), cameraTarget=(55.9857, 53.4698, -5.61094), 
        viewOffsetX=7.61504, viewOffsetY=7.28788)
    p = mdb.models['Model-1'].parts['Polymer']
    e = p.edges
    p.DatumAxisByThruEdge(edge=e[7])


