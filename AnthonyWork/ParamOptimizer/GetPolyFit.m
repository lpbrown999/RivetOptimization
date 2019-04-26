%% Run this section to initialize the polynomial
load('CellData3.mat')
vars={'constant', 'x', 'y', 'z', 'x*y', 'x*z', 'y*z', 'x*y*z', 'x*x', 'y*y', 'z*z', 'y*x*x', 'z*x*x', 'y*z*x*x', 'x*y*y', 'z*y*y', 'x*z*y*y', 'x*z*z', 'y*z*z', 'x*y*z*z', 'y*y*x*x', 'z*y*y*x*x', 'z*z*x*x', 'y*z*z*x*x', 'y*y*z*z', 'x*y*y*z*z', 'x*x*y*y*z*z', 'x*x*x', 'y*x*x*x', 'z*x*x*x', 'y*z*x*x*x', 'y*y*x*x*x', 'z*z*x*x*x', 'y*y*z*x*x*x', 'y*z*z*x*x*x', 'y*y*z*z*x*x*x', 'y*y*y', 'x*y*y*y', 'z*y*y*y', 'x*z*y*y*y', 'x*x*y*y*y', 'z*z*y*y*y', 'x*x*z*y*y*y', 'z*z*x*y*y*y', 'z*z*x*x*y*y*y', 'z*z*z', 'x*z*z*z', 'y*z*z*z', 'x*y*z*z*z', 'x*x*z*z*z', 'y*y*z*z*z', 'x*y*y*z*z*z', 'y*x*x*z*z*z', 'x*x*y*y*z*z*z', 'x*x*x*y*y*y', 'x*x*x*y*y*y*z', 'x*x*x*y*y*y*z*z', 'x*x*x*z*z*z', 'x*x*x*z*z*z*y', 'x*x*x*z*z*z*y*y', 'y*y*y*z*z*z', 'y*y*y*z*z*z*x', 'y*y*y*z*z*z*x*x', 'y*y*y*z*z*z*x*x*x'};
p = polyfitn(a(:,1:3),a(:,4),vars)
[val,i]= min(abs(p.Coefficients));
%% Then continually run this section to whittle away terms that dont matter (length of 28 is best)
if i~=length(vars)
    vars=[vars(1:i-1),vars(i+1:end)];
else
    vars=vars(1:i-1);
end
p = polyfitn(a(:,1:3),a(:,4),vars) %vars length 28 is smallest good fit of data
[val,i]= min(abs(p.Coefficients));