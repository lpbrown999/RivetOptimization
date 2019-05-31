function x_new = refineX(x)
%Sometimes the x value will run an error in Abaqus, we must fix the values which are not allowed.
global frame_min frame_max n_max n_min d_min d_max cellW
%% If you are running Abaqus everytime
% if x(2)<frame_min
%     x(2)=frame_min;
% elseif x(2)>frame_max
%     x(2)=frame_max;
% end
% 
% x(3)=double(round(x(3)));
% if x(3)<n_min
%     x(3)=n_min;
% elseif x(3)>n_max
%     x(3)=n_max;
% end
% 
% if x(1)<d_min
%     x(1)=d_min;
% elseif x(1)*x(3)+2*x(2)>=cellW
%     x(1)=.8*(cellW-2*x(2))/x(3);
% end
% 
% if x(1)>d_max
%     x(1)=d_max;
% end
% 
% if x(3)==0
%     x(1)=0;
% end
%% If you just use an analytical function
x(3)=double(round(x(3)));
if x(3)==0
    x(1)=0;
end
%% Write the new x value and return
x_new=x;

end

