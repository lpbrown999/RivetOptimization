function filename = WriteScript(mode,PathToFolder)
%mode tells whether to run bending or tension test
%mode=1 is bending and mode=2 is tension/compression depending on sign of F
global cellW frameW n r F FS bat poly

filename=['d',num2str(r*2),'f',num2str(frameW),'n',num2str(n),'.txt'];

if mode==1
    loc = 'Results/t=3mm/';
    code = 'codenew.txt';
else
    loc = 'TensionResults/t=3mm/';
    code = 'tensioncompression.txt';
end

% You can change the directory where the results files will be saved to here %
fileloc=[PathToFolder,loc,filename];


fid = fopen('parameters.txt','wt');

fprintf(fid,'cellW=%.2f;\n',cellW);
fprintf(fid,'frameW=%.2f;\n',frameW);

fprintf(fid,'n=%.2f;\n',n);
fprintf(fid,'r=%.2f;\n\n',r);

fprintf(fid,'F=%.2f;\n\n',F);

fprintf(fid,'t_FS=%.2f;\n',FS.t);
fprintf(fid,'E11_FS=%.2f;\n',FS.E11);
fprintf(fid,'E22_FS=%.2f;\n',FS.E22);
fprintf(fid,'E33_FS=%.2f;\n',FS.E33);
fprintf(fid,'nu12_FS=%.2f;\n',FS.nu12);
fprintf(fid,'nu13_FS=%.2f;\n',FS.nu13);
fprintf(fid,'nu23_FS=%.2f;\n',FS.nu23);
fprintf(fid,'G12_FS=%.2f;\n',FS.G12);
fprintf(fid,'G13_FS=%.2f;\n',FS.G13);
fprintf(fid,'G23_FS=%.2f;\n',FS.G23);
fprintf(fid,'t_rod=%.2f;\n',2.0);
fprintf(fid,'mesh_FS=%.2f;\n\n',FS.mesh);

fprintf(fid,'t_bat=%.2f;\n',bat.t);
fprintf(fid,'E11_bat=%.2f;\n',bat.E11);
fprintf(fid,'E22_bat=%.2f;\n',bat.E22);
fprintf(fid,'E33_bat=%.2f;\n',bat.E33);
fprintf(fid,'nu12_bat=%.2f;\n',bat.nu12);
fprintf(fid,'nu13_bat=%.2f;\n',bat.nu13);
fprintf(fid,'nu23_bat=%.2f;\n',bat.nu23);
fprintf(fid,'G12_bat=%.2f;\n',bat.G12);
fprintf(fid,'G13_bat=%.2f;\n',bat.G13);
fprintf(fid,'G23_bat=%.2f;\n',bat.G23);
fprintf(fid,'mesh_bat=%.2f;\n\n',bat.mesh);

fprintf(fid,'E_poly=%.2f;\n',poly.E);
fprintf(fid,'nu_poly=%.2f;\n',poly.nu);
if r>3
    mesh=1.5;
    fprintf(fid,'mesh_poly=%.2f;\n\n',mesh);
else
    fprintf(fid,'mesh_poly=r/2;\n\n');
end

fprintf(fid,'myoutfile = open(''%s''%f',fileloc);
fprintf(fid,',''%s'');\n\n','w+');

fclose(fid);
string=strcat('copy parameters.txt+',code,' final.py');
system(string);
end

