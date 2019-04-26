function pen = PenCalc(xi)
%The penalty function g needs to be defined in the function g Matlab file
pen=0;
a=g(xi);
eps=.001;
for k=1:length(a)
    pen=pen+max(0,a(k)+eps)^2;
end
end

