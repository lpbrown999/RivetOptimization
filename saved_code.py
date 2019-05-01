##This one I am no longer using because it uses a solid section not a shell
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