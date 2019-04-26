function [nlc,nlceq] = nlc(xi)
global Emin cellW

Vpoly=3*(xi(3)^2*xi(1)^2*pi/4+(xi(2)*(cellW-xi(2)))*4);

nlc1=(Emin-(210*(3*cellW^2-Vpoly)*2.857e-6)/(Vpoly*(1e-6-2.857e-6)+3*cellW^2*2.857e-6+2*cellW^2*1.6e-6));
nlc2=xi(1)*xi(3)+2*xi(2)-cellW;
nlc3=(xi(1)*(xi(3)+1)+2*xi(2)+xi(3)*xi(1)-cellW);

nlc=[nlc1,nlc2,nlc3];
nlceq=[];
end