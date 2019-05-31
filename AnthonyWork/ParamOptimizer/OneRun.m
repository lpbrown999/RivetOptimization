clc
clear all
close all

global cellW frameW n r F FS bat poly
iterations=0;
A=9*9*pi*1^2+(110-10)*4*10;

r = 4.0;%range between 1 and 15
frameW = 10.0; %range between 5 and 20
n = 4.0; %range between 2 and 10

cellW = 110.0;
F = 500.0;
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

for n=3:3
    for frameW=8:1:8
        for r=4:1:4
            iterations = iterations + 1
            
            %Change these three parameters only.
            %r = sqrt((A-(cellW-frameW)*4*frameW)/(n^2*pi));
            
            if 2*r >= (cellW-2*frameW)/(n+1)
                val(iterations,:)=[2*r,frameW,n,0,F];
            else
                val(iterations,:)=[2*r,frameW,n,f([r*2,frameW,n]),F];
            end
        end
    end
end
val=double(val);
xlswrite('threepointbend.xlsx',val)