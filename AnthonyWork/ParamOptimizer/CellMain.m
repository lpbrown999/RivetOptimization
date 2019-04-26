clc
clear all
close all

global cellW frameW n r F FS bat poly

% IMPORTANT: you must change the path folder location variable below to
% wherever you store these functions to run the parameterized cell code
PathToFolder='C:\Users\Bombik\Documents\School\GradSchool\AeroAstroMasters\SACL\ParamOptimizer\';

%Parameters for the geometry of the cell

r = 4.0;%range between 1 and 15
frameW = 10.0; %range between 5 and 20
n = 5.0; %range between 2 and 10



%Other cell parameters and material properties of the components

cellW = 110.0;
F = 150.0;
FS.t = .8;
FS.E11 = 30420;
FS.E22 = 4023;
FS.E33 = 4023;
FS.nu12 = .29;
FS.nu13 = .29;
FS.nu23 = .3928;
FS.G12 = 2081;
FS.G13 = 2081;
FS.G23 = 1440;
FS.mesh = 1.5;
bat.t = 3.0;
bat.E11 = 1090;
bat.E22 = 1090;
bat.E33 = 500;
bat.nu12 = .15;
bat.nu13 = .15;
bat.nu23 = .15;
bat.G12 = 474;
bat.G13 = 474;
bat.G23 = 474;
bat.mesh = 1.5;
poly.E=600.00;
poly.nu=0.30;

if 2*r >= (cellW-2*frameW)/(n+1)
    r=(cellW-2*frameW)/(2*(n+1))-1;
end

g=cellG([r*2,frameW,n],PathToFolder)
e=cellE([r*2,frameW,n],PathToFolder)