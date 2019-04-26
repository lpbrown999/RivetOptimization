% r=[1;3;5;7;9;11;13;15];
% f=[5;7.5;10;12.5;15;17.5;20];
% n=[3;4;5;6;7;8;9;10];
% 
% %assemble all data side by side to make 8*63 matrix
% %each row is a new radius size
% %each column is a new frame size
% %put the data for each n next to each other 2,3,4...etc
% 
% base=zeros(504,4);
% for j=1:length(n)
%     for i=1:length(f)
%         starti=56*(j-1)+8*(i-1)+1;
%         endi=starti+7;
%         base(starti:endi,1)=2*r;
%         base(starti:endi,2)=f(i);
%         base(starti:endi,4)=karen(1:8,(j-1)*7+i);
%     end
%     startj=56*(j-1)+1;
%     endj=56*j;
%     base(startj:endj,3)=n(j);
% end

a=zeros(223,4);
index=1;
for i=1:length(val)
    if val(i,4)~=0
        a(index,:)=val(i,:);
        index=index+1;
    end
end

p = polyfitn(a(:,1:3),a(:,4),'constant x y z x*y x*z y*z x*y*z x*x y*y z*z y*x*x z*x*x y*z*x*x x*y*y z*y*y x*z*y*y x*z*z y*z*z x*y*z*z y*y*x*x z*y*y*x*x z*z*x*x y*z*z*x*x y*y*z*z x*y*y*z*z x*x*y*y*z*z')