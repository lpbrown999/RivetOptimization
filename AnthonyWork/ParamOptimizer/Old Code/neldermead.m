function [simplex(imin,:)] = neldermead(x0) 
    %x0 needs to be a row vector
    x0=float(x0);
    count=0;
    simplex=x0;
    T1=T(x0);
    funsimplex=T1;
    c=c+1;
    step=20;
    maxsteps=100; %Don't forget to change this later

    for j=1:length(x0)
        xj=x0;
        xj(j)=x0(j)+step;
        simplex=[simplex;xj];
        funsimplex=[funsimplex,T(xj)];
        c=c+1;
    end

    for i=1:maxsteps
%Step 2: find min and max indices
        
        
        [min,imin]=min(funsimplex);
        [max,imax]=max(funsimplex);
        max2=min;
        imax2=imin;
        
        if max-min<=1e-6+1e-5*abs(min)
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
        
        if c < cmax
        fxr=T(xr);
        c=c+1;
        else
            break
        end
        
        if (min<=fxr)&&(fxr<max)
            simplex(imax,:)=xr;
            funsimplex(imax)=fxr;
%Step 4
        elseif fxr<min
            xe=xc+2*(xr-xc);
            
            if c < cmax
            fxe=T(xe);
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
            
            if c < cmax
            fxs=T(xs);
            c=c+1;
            else
                break
            end
            
            if fxs<max
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
    
        [min,imin]=min(funsimplex);
        [max,imax]=max(funsimplex);
        max2=min;
        imax2=imin;
    
        for k=1:length(funsimplex)
            if k~=imax
            if funsimplex(k)>=max2
                max2=funsimplex(k);
                imax2=k;
            end
            end
        end

