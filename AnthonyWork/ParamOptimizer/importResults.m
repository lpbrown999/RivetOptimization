clear all
clc

%% Variable Input

cellW = 110.0;
F = 500.0;
FS.t = 1;
FS.E = 69000.0;
FS.nu = .3;
FS.mesh = 1.0;
bat.t=3.0;
bat.E=10.0;
bat.nu=0.3;
bat.mesh=1.0;
poly.E=500.00;
poly.nu=0.30;

cell.L = cellW/1e3; % overall length
cell.b = cellW/1e3; % overall width
cell.c = bat.t/1e3; % thickness of core
cell.t_FS = FS.t/1e3; % thickness of facesheet
cell.t = cell.c + 2 * cell.t_FS; % overall thickness
cell.d = cell.t_FS+cell.c;

cell.E_FS = FS.E *1e6; % N/m^2
cell.E_core = poly.E *1e6; % N/m^2

P=F; %N

D = cell.E_FS * cell.b*cell.t_FS^3/6 + ...
    cell.E_FS * (cell.b*cell.t_FS*cell.d^2)/2 + ...
    cell.E_core * cell.b*cell.c^3/12;

%% Beginning of Loop
index = 0;
for n=2:10
    for frameW=5:2.5:20
        for r=1:2:15
            index=index+1
            
            syms G
            
            theta =simplify( cell.L/cell.c * ( G/2/cell.E_FS*cell.c/cell.t_FS*...
                (1+3*cell.d^2/cell.t_FS^2)).^(0.5));
            psi = 1- tanh(theta)./theta;
            A = cell.b*cell.d^2/cell.c;
            I_f =1/12*cell.b*cell.t_FS^3;
            I = (I_f+1/4*(cell.b*cell.t_FS)*cell.d^2);
            delta = P*cell.L^3/48/D + P*cell.L./4./G./A * (1-I_f/I)^2*psi;
            
            if 2*r >= (cellW-2*frameW)/(n+1)
                val(index,:)=[2*r,frameW,n,0];
            else
                filename=['d',num2str(r*2),'f',num2str(frameW),'n',num2str(n),'.txt'];
                fileloc=['C:/Users/Bombik/Documents/School/GradSchool/AeroAstroMasters/SACL/ParamOptimizer/Results/',filename];
                
                delimiter = ' ';
                header = 1;
                
                A = importdata(fileloc, delimiter);
                a = length(A);
                
                for i = 1 : a
                    x = A(i,1);
                    y = A(i,2);
                    z = A(i,3);
                    
                    amplitude(i) = sqrt(x^2+y^2+z^2);
                    zs(i) = abs(z);
                end
                
                max_amplitude = max(amplitude);
                max_z = max(zs);
                
                warning('off')
                rmpath('cannotsolvesymbolically')
                Gg = double(solve(delta==.001*max_z,G))*1e-6;
                val(index,:)=[2*r,frameW,n,Gg];
            end
        end
    end
end