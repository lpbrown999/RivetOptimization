#Idea;
#Write the locations etc in the optimization program to a database file like a .txt or CSV
#Read them in using the script that gets called
#Consider re-rewiting, using shells instead of solids -> done

#Todo:
#Extract values from OBD
#Optimization
#Formatting?

#Notes
#Anthony ties together the: CF, polymer
#Lets contact do work for: BAT/CF, BAT/POLY

#session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)


# # Output Displacement

# import odbAccess
odb = session.openOdb('Tension.odb')
timeFrame = odb.steps['Loading'].frames[1]
displacement = timeFrame.fieldOutputs['U']
loadnode = odb.rootAssembly.nodeSets['CONTINUITY']
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
#