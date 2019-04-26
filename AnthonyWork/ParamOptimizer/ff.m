function ef = ff(x)
load('CellData3.mat')
vars={'constant', 'x', 'y', 'z', 'x*y', 'x*z', 'y*z', 'x*y*z', 'x*x', 'y*y', 'z*z', 'z*x*x', 'y*z*x*x', 'x*y*y', 'z*y*y', 'x*z*y*y', 'x*z*z', 'y*z*z', 'x*y*z*z', 'z*z*x*x', 'y*z*z*x*x', 'x*x*x', 'z*x*x*x', 'z*z*x*x*x', 'y*y*y', 'z*z*z', 'x*z*z*z', 'x*x*z*z*z'};
p = polyfitn(a(:,1:3),a(:,4),vars);
ef=polyvaln(p,x);
ef=-ef;
end

