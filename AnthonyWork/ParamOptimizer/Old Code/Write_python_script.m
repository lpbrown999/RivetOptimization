
fid = fopen('parameters.txt','wt');

fprintf(fid,'cellW=%.2f;\n',110.0);
fprintf(fid,'frameW=%.2f;\n',10.0);

fprintf(fid,'n=%.2f;\n',4.0);
fprintf(fid,'r=%.2f;\n\n',2.0);

fprintf(fid,'F=%.2f;\n\n',500.0);

fprintf(fid,'t_FS=%.2f;\n',1.0);
fprintf(fid,'E_FS=%.2f;\n',69000.0);
fprintf(fid,'nu_FS=%.2f;\n',.3);
fprintf(fid,'t_rod=%.2f;\n',2.0);
fprintf(fid,'mesh_FS=%.2f;\n\n',2.0);

fprintf(fid,'t_bat=%.2f;\n',3.0);
fprintf(fid,'E_bat=%.2f;\n',10.0);
fprintf(fid,'nu_bat=%.2f;\n',.3);
fprintf(fid,'mesh_bat=%.2f;\n\n',2.0);

fprintf(fid,'E_poly=%.2f;\n',500.0);
fprintf(fid,'nu_poly=%.2f;\n',.3);
fprintf(fid,'mesh_poly=r/2;\n\n');

fclose(fid);

system('copy parameters.txt+code.txt final.py');