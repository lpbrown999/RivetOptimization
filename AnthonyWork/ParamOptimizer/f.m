function [avg_y] = f(x)
global cellW frameW n r F FS bat poly

r=x(1)/2;
frameW=x(2);
n=x(3);

warning('off')
rmpath('filenotfound')
%delete('C:\Users\Bombik\Documents\School\GradSchool\AeroAstroMasters\SACL\ParamOptimizer\3PointBend.*')
%delete('C:\Users\Bombik\Documents\School\GradSchool\AeroAstroMasters\SACL\ParamOptimizer\*.rpy.*')
%delete('C:\Users\Bombik\Documents\School\GradSchool\AeroAstroMasters\SACL\ParamOptimizer\*.rec')
%delete('C:\Users\Bombik\Documents\School\GradSchool\AeroAstroMasters\SACL\ParamOptimizer\result.txt')
delete('3PointBend.*')
delete('Tension.*')
delete('*.rpy.*')
delete('*.rec')

fi = WriteScript(1);

% change the location of the results file. make sure it aligns with the
% folder location in "WriteScript.m"
filename =['C:\Users\Bombik\Documents\School\GradSchool\AeroAstroMasters\SACL\ParamOptimizer\Results\t=3mm\',fi];

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
    x = A(i,1);
    y = A(i,2);
    z = A(i,3);
    
    %amplitude(i) = sqrt(x^2+y^2+z^2);
    ys(i) = abs(y);
    zs(i) = abs(z);
end

%max_amplitude = max(amplitude);
avg_y = mean(ys);
avg_z = mean(zs);

% cell.L = cellW/1e3; % overall length
% cell.b = cellW/1e3; % overall width
% cell.c = bat.t/1e3; % thickness of core
% cell.t_FS = FS.t/1e3; % thickness of facesheet
% cell.t = cell.c + 2 * cell.t_FS; % overall thickness
% cell.d = cell.t_FS+cell.c;
% 
% cell.E_FS = (FS.E11+FS.E22)/2 *1e6; % N/m^2
% cell.E_core = poly.E *1e6; % N/m^2
% 
% P=F; %N
% 
% D = cell.E_FS * cell.b*cell.t_FS^3/6 + ...
%     cell.E_FS * (cell.b*cell.t_FS*cell.d^2)/2 + ...
%     cell.E_core * cell.b*cell.c^3/12;
% 
% syms G
% 
% theta =simplify( cell.L/cell.c * ( G/2/cell.E_FS*cell.c/cell.t_FS*...
%     (1+3*cell.d^2/cell.t_FS^2)).^(0.5));
% psi = 1- tanh(theta)./theta;
% A = cell.b*cell.d^2/cell.c;
% I_f =1/12*cell.b*cell.t_FS^3; 
% I = (I_f+1/4*(cell.b*cell.t_FS)*cell.d^2);
% delta = P*cell.L^3/48/D + P*cell.L./4./G./A * (1-I_f/I)^2*psi;
% 
% 
% warning('off')
% rmpath('cannotsolvesymbolically')
% Gg = -double(solve(delta==avg_z*1e-3,G)*1e-6);
end
