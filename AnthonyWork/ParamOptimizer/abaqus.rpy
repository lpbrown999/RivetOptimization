# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2019 replay file
# Internal Version: 2018_09_24-11.41.51 157541
# Run by lpbro on Mon May 27 14:30:08 2019
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=208.828109741211, 
    height=239.180541992188)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
execfile('codenew.py', __main__.__dict__)
#: The interaction property "NormCont" has been created.
#: The interaction "CF1Bat" has been created.
#: The interaction "CF2Bat" has been created.
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
    constraints=ON, connectors=ON, engineeringFeatures=ON, 
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
session.viewports['Viewport: 1'].view.setValues(nearPlane=254.558, 
    farPlane=386.671, width=98.3929, height=114.014, cameraPosition=(275.16, 
    103.63, 226.478), cameraUpVector=(-0.51438, 0.843016, -0.157283), 
    cameraTarget=(57.8824, 54.7951, -4.17747))
session.viewports['Viewport: 1'].view.setValues(nearPlane=248.96, 
    farPlane=396.021, width=96.2293, height=111.507, cameraPosition=(361.665, 
    63.2117, 98.0067), cameraUpVector=(-0.425134, 0.893537, 0.144404), 
    cameraTarget=(57.8813, 54.7956, -4.17585))
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, interactions=OFF, constraints=OFF, 
    engineeringFeatures=OFF)
