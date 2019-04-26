function g = g(xi)
global frame_min n_max n_min d_min d_max Emin cellW bat FS

Vpoly=bat.t*(xi(3)^2*xi(1)^2*pi/4+(xi(2)*(cellW-xi(2)))*4);

g1=(Emin-(210*(bat.t*cellW^2-Vpoly)*2.857e-6)/(Vpoly*(1e-6-2.857e-6)+bat.t*cellW^2*2.857e-6+2*FS.t*cellW^2*1.6e-6));
g2=(-xi(1)+d_min);
g3=(-xi(2)+frame_min);
g4=xi(1)*xi(3)+2*xi(2)-cellW;
g5=(-xi(3)+n_min);
g6=(xi(1)*(xi(3)+1)+2*xi(2)+xi(3)*xi(1)-cellW);
g7=xi(3)-n_max;
g8=xi(1)-d_max;

g=[g1,g2,g3,g4,g5,g6,g7,g8];
end

