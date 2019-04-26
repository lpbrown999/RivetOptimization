In order to run this code your computer needs to have Matlab and Abaqus.

1. Change the Matlab directory to this folder.

2. Change the directory of where to find Abaqus on your computer in the cellE.m and cellG.m files
   i.e. "system('C:\SIMULIA\Abaqus\6.12-1\code\bin\abq6121 cae NOGUI=final.py')"

3. Write the directory of this folder in the first line of "CellMain.m"
   i.e. "PathToFolder='C:\Users\Bombik\Documents\School\GradSchool\AeroAstroMasters\SACL\ParamOptimizer\';"

4. Change any of the material properties, applied load or geometry parameters in CellMain.m as desired.

5. Run the CellMain.m file.

The script returns the value for E and G for the homogenized isotropic simplification of the cell.

Author:
Anthony Bombik		ajbombik@stanford.edu