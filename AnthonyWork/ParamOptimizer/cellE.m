function Ee = cellE(x,PathToFolder)
global cellW frameW n r F FS bat poly

r=x(1)/2;
frameW=x(2);
n=x(3);

warning('off')
rmpath('filenotfound')
delete('3PointBend.*')
delete('Tension.*')
delete('*.rpy.*')
delete('*.rec')

fi = WriteScript(2,PathToFolder);

% change the location of the results file. make sure it aligns with the
% folder location in "WriteScript.m"
filename =[PathToFolder,'TensionResults\t=3mm\',fi];

if exist(filename,'file') ~= 2
    % this needs to be the directory for your abaqus executable dont change
    % the "cae NOGUI=final.py" part
    system('C:\SIMULIA\Abaqus\6.12-1\code\bin\abq6121 cae NOGUI=final.py');
end

delimiter = ' ';
header = 1;

A = importdata(filename, delimiter);
a = length(A);

for i = 1 : a
    y = A(i,2);
    ys(i) = abs(y);
end

avg_y = mean(ys);


cell.L = cellW*1e-3; % overall length
cell.b = cellW*1e-3; % overall width
cell.c = bat.t*1e-3; % thickness of core
cell.t_FS = FS.t*1e-3; % thickness of facesheet
cell.t = cell.c + 2 * cell.t_FS; % overall thickness
cell.d = cell.t_FS+cell.c;

cell.E_FS = (FS.E11+FS.E22)/2 *1e6; % N/m^2
cell.E_core = poly.E *1e6; % N/m^2

Ee=(F*cell.L/(avg_y*1e-3)-2*cell.E_FS*cell.b*cell.t_FS)/(cell.b*cell.c);
end

