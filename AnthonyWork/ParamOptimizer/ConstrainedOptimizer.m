clc
clear all
close all
global frame_min frame_max n_max n_min d_min d_max Emin cellW sens r c cmax frameW n F FS bat poly
frame_min=5;
frame_max=20;
n_max=10;
n_min=0;
d_min=1;
d_max=20;   
sens=1000;
c=0;

%battery parameters
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

%important parameters to change
cmax=1000;
Emin=160;    
x=[3,5,3]; %starting x value

load('CellData3.mat')
vars={'constant', 'x', 'y', 'z', 'x*y', 'x*z', 'y*z', 'x*y*z', 'x*x', 'y*y', 'z*z', 'z*x*x', 'y*z*x*x', 'x*y*y', 'z*y*y', 'x*z*y*y', 'x*z*z', 'y*z*z', 'x*y*z*z', 'z*z*x*x', 'y*z*z*x*x', 'x*x*x', 'z*x*x*x', 'z*z*x*x*x', 'y*y*y', 'z*z*z', 'x*z*z*z', 'x*x*z*z*z'};
p = polyfitn(a(:,1:3),a(:,4),vars);

for i=1:1
    if c<cmax-length(x)-1
%%%%%%%%%%%%%%%%%% beginning of nelder mead algorithm
    x0=x;
    x0=refineX(x0);
    count=0;
    simplex=x0;
    T1=T(p,x0);
    funsimplex=T1;
    c=c+1;
    step=20;
    maxsteps=cmax*14; %Don't forget to change this later

    for j=1:length(x0)
        xj=x0;
        xj(j)=x0(j)+step;
        xj=refineX(xj);
        simplex=[simplex;xj];
        funsimplex=[funsimplex,T(p,xj)];
        c=c+1;
    end

    for i=1:maxsteps
        
%Step 2: find min and max indices
       
        [mini,imin]=min(funsimplex);
        [maxi,imax]=max(funsimplex);
        max2=mini;
        imax2=imin;
        
        if maxi-mini<=1e-6+1e-5*abs(mini)
                    break
        end
        
        for k=1:length(funsimplex)
            if k~=imax
            if funsimplex(k)>=max2
                max2=funsimplex(k);
                imax2=k;
            end
            end
        end

%Step 3: find centroid of the simplex and determine reflection
        sum=0;
        for j=1:length(funsimplex)
            if j~=imax
                sum=sum+simplex(j,:);
            end
        end
        xc=sum/(length(funsimplex)-1);    
        xr=xc+(xc-simplex(imax,:));
        xr=refineX(xr);
        
        if c < cmax
        fxr=T(p,xr);
        c=c+1;
        else
            break
        end
        
        if (mini<=fxr)&&(fxr<maxi)
            simplex(imax,:)=xr;
            funsimplex(imax)=fxr;
%Step 4
        elseif fxr<mini
            xe=xc+2*(xr-xc);
            xe=refineX(xe);
            
            if c < cmax
            fxe=T(p,xe);
            c=c+1;
            else
                break
            end
            
            if fxe<fxr
                simplex(imax,:)=xe;
                funsimplex(imax)=fxe;
            else
                simplex(imax,:)=xr;
                funsimplex(imax)=fxr;
            end
        else
%Step 5
            xs=xc+.5*(simplex(imax,:)-xc);
            xs=refineX(xs);
            
            if c < cmax
            fxs=T(p,xs);
            c=c+1;
            else
                break
            end
            
            if fxs<maxi
                simplex(imax,:)=xs;
                funsimplex(imax)=fxs;
            else
%Step 6
                for k=1:length(funsimplex)
                    if k==imin
                    else
                    simplex(k,:)=simplex(imin,:)+.5*(simplex(k,:)-simplex(imin,:));
                    end
                end
            end
        end
    end  
    
        [mini,imin]=min(funsimplex);
        [maxi,imax]=max(funsimplex);
        max2=mini;
        imax2=imin;
    
        for k=1:length(funsimplex)
            if k~=imax
            if funsimplex(k)>=max2
                max2=funsimplex(k);
                imax2=k;
            end
            end
        end
    x=simplex(imin,:);
%%%%%%%%%%%%%% end of nelder mead algorithm        
    else
        break
    end
    sens=sens*10;
end
gee=g(x);
Eact=Emin-gee(1);
[x,-ff(p,x),c]
