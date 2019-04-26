xz = [2 2; 6 2 ; 10 2 ; 14 2 ; 2 3 ; 6 3 ; 10 3 ; 14 3 ; 2 4 ; 6 4 ; 10 4 ; 14 4 ; 2 5 ; 6 5 ; 10 5 ; 14 5];
xy = [2 5; 2 7.5; 2 10; 2 12.5; 6 5; 6 7.5; 6 10; 6 12.5; 10 5; 10 7.5; 10 10; 10 12.5; 14 5; 14 7.5; 14 10; 14 12.5];
yz = [5 2; 7.5 2; 10 2; 12.5 2; 5 3; 7.5 3; 10 3; 12.5 3; 5 4; 7.5 4; 10 4; 12.5 4; 5 5; 7.5 5; 10 5; 12.5 5];

Gxz = [23.45097177 23.76469765 24.19950772 24.8456932 23.48081884 24.00729865 24.89476208 26.48290214 23.70636497 25.0266383 27.41071368 32.59379186 23.81632991 25.69901935 30.09190072 42.98078626].';
Gxy = [13.35393728 18.35412545 23.70636497 29.39962549 14.27545553 19.46536905 25.0266383 30.98621027 15.85222849 21.34651497 27.41071368 33.85849485 18.98766717 25.29673553 32.59379186 40.37368715].';
Gyz = [13.69021315 18.83635136 24.19950772 30.08597608 14.188762 19.42987741 24.89476208 30.96818341 15.85222849 21.34651497 27.41071368 33.85849485 17.33324673 23.42238004 30.09190072 37.44346447].';

fxz = fit( xz, Gxz, 'poly33');
fxy = fit( xy, Gxy, 'poly21');
fyz = fit( yz, Gyz, 'poly21');

subplot(1,3,1); plot(fxz, xz, Gxz); shading interp; box off; 
subplot(1,3,2); plot(fxy, xy, Gxy); shading interp; box off; 
subplot(1,3,3); plot(fyz, yz, Gyz); shading interp; box off;

%You need to use meshgrid to define the grid for the surface. 

[xz_x, xz_z] = meshgrid(2:4:14, 2:1:5);
[xy_x, xy_y] = meshgrid(2:4:14, 5:2.5:12.5);
[yz_y, yz_z] = meshgrid(5:2.5:12.5, 2:1:5);

%Then you evaluate the functions at the points of the grid:

Gxz = fxz(xz_x,xz_z); Gxy = fxy(xy_x,xy_y); Gyz = fyz(yz_y,yz_z); 

%Then you plot:

i = 9; ii = 10;

figure 
set(gcf,'papertype','a4','paperorientation','landscape','paperunits','centimeters', ...
    'paperposition',[0.63 0.63 28.41 19.72], 'Renderer', 'zbuffer');

subplot(1,3,1); surf(xz_x,xz_z,Gxz); shading interp; set(gca, 'fontsize', i, 'projection', 'perspective')
xlabel('Rivet Diameter (mm)', 'fontsize', ii); ylabel('Num of Rivets (n*n)', 'fontsize', ii); zlabel('Effective G (MPa)', 'fontsize', ii); 

subplot(1,3,2); surf(xy_x,xy_y,Gxy); shading interp; set(gca, 'fontsize', i, 'projection', 'perspective')
xlabel('Rivet Diameter (mm)', 'fontsize', ii); ylabel('Frame Width (mm)', 'fontsize', ii); zlabel('Effective G (MPa)', 'fontsize', ii); 

subplot(1,3,3); surf(yz_y,yz_z,Gyz); shading interp; set(gca, 'fontsize', i, 'projection', 'perspective')
xlabel('Frame Width (mm)', 'fontsize', ii); ylabel('Num of Rivets (n*n)', 'fontsize', ii); zlabel('Effective G (MPa)', 'fontsize', ii); 
