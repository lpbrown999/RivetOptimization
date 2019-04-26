global Emin cellW sens
sens=1000;
Emin=140;
cellW=110;

nlcon=@nlc;
fun=@T;

gen_options=gaoptimset('PopulationSize',1000,'EliteCount',20,'CrossoverFraction',0.6,...
    'Generations',100,'StallGenLimit',50,'StallTimeLimit',1800,'TolFun',1e-14, 'TolCon',1e-14, 'display', 'iter',...
    'FitnessScalingFcn',@fitscalingprop, 'PlotFcns',@gaplotbestindiv, 'vectorized', 'on');
%[GAVar, fval, exitflag, output] = ga(@(x)ff(x),3,[],[],[],[],[0 5 0],[15 20 10],nlcon,[3],gen_options)

xmin = fmincon(fun,[0,5,10],[],[],[],[],[0,0,0],[15,20,10])
nlc(xmin)
-ff(xmin)