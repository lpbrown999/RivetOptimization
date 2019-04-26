function [TENSOR, IDs, nodalListing, elementListing] = getRPT(FILENAME)
%GETRPT Gets the field output variable items from an Abaqus/CAE RPT file.
%   [TENSOR, IDs] = GETRPT(FILENAME) returns the tensor components of an FE model
%   exported from the Abaqus visualisation module.
%
%   FILENAME is the name of the RPT file generated by Abaqus/CAE.
%
%   TENSOR is an Nx6 array of stresses.
%
%   IDS is a 1x2 array. IDS(1) is the number of elements in the FE model if
%   the field variable data was specified as elemental-nodal, otherwise it
%   is assigned a default value of -9999. IDS(2) is the number of nodes in the FE
%   model.
%
%   Data must be the stress components [S11 S22 S33 S12 S23 S13]. In the
%   event of an error in reading the stresses, IDS is assigned the value
%   [-1, -1]
%
%   To generate an RPT field variable file, do the following in ABAQUS/CAE:
%   1. In the Visualizaiton Module, go to "Report -> Field Output...".
%   2. In the "Variable" tab, choose "Unique Nodal" or "Element Nodal" as 
%   the position type.
%   3. Expand the "S: Stress components" tree and check the last 6 options
%   (the Cauchy stress tensor). Make sure that these are the only boxes
%   checked.
%   4. In the "Setup" tab under "Output Format", make sure the layout style
%   is set to "Single table for all field output variables".
%   5. Under "Data", uncheck "Column totals" and "Column
%   min/max" as these are not required. GETITEMS has not been validated
%   for RPT files with this information included.
%
%   For a list of functions related to scanning data from files with
%   headers, refer to the following:
%   
%   See also fopen, fclose, importdata, dlmread, textscan, fscanf, fread.

%   Copyright 2014 Louis Vallance, Safe Technlogy Limited
%   Last modified 07-Oct-2014 11:30:14

%% Open the .rpt file:

fid = fopen(FILENAME, 'r');

%% Check if there is a header:

try
    cellData = textscan(fid, '%f %f %f %f %f %f %f %f');
catch
    IDs = [-999.0, -999.0];
    TENSOR = [];
    nodalListing = -999.0;
    return
end

if isempty(cellData{1.0})
    hasHeader = true; % There is a header in the file
else
    hasHeader = false; % There might be no header in the file
end

if ~hasHeader
    for i = 1.0:length(cellData)
        if isempty(cellData{i})
            hasHeader = true;
            break
        end
    end
end

%% Scan the file:

if hasHeader
    while ~feof(fid)
        fgetl(fid);
        cellData = textscan(fid, '%f %f %f %f %f %f %f %f');
    end
end

%% Remove unused columns if required:

remove = 0.0;
if length(cellData{8.0}) ~= length(cellData{1.0})
    cellData{8.0} = zeros(length(cellData{1.0}), 1.0, 'double');
    remove = 1.0;
end

if length(cellData{7.0}) ~= length(cellData{1.0})
    cellData{7.0} = zeros(length(cellData{1.0}), 1.0, 'double');
    remove = 2.0;
end

%% Check for concatenation errors:

try
    fieldData = cell2mat(cellData);
catch
    IDs = [-999.0, -999.0];
    TENSOR = [];
    nodalListing = -999.0;
    return
end

if isempty(fieldData)
    IDs = [-999.0, -999.0];
    TENSOR = [];
    nodalListing = -999.0;
    return
end

if remove == 2.0
    fieldData(:, 7.0:8.0) = [];
elseif remove == 1.0
    fieldData(:, 8.0) = [];
end

%% Interpret columns:

%{
    NODETYPE: Format of nodal information
    0: No listing. Take nodal information from row number
    1: Nodal listing
    2: Element-nodal listing
    -1: Error
%}

[R, C] = size(fieldData);
switch C
    case 8.0
        nodeType = 2.0;
        elementListing = fieldData(:, 1.0);
        nodalListing = fieldData(:, 2.0);
        X = 3.0;
    case 7.0
        nodeType = 1.0;
        IDs = [-999.0, R];
        nodalListing = fieldData(:, 1.0);
        elementListing = -999.0;
        X = 2.0;
    case 6.0
        nodeType = 0.0;
        IDs = [-999.0, R];
        nodalListing = linspace(1.0, R, R);
        elementListing = -999.0;
        X = 1.0;
    otherwise
        IDs = [-999.0, -999.0];
        nodalListing = -999.0;
        elementListing = -999.0;
        return
end

%%  Check for erroneous data:

% check = false;
% while ~check
%     if nodeType >= 1.0
%         if fieldData(1.0,1.0) ~= 1.0
%             fieldData(1.0, :) = [];
%         else
%             check = true;
%         end
%     else
%         check = true;
%     end
% end

%% Get tensor components:

Sxx = fieldData(:, X)';
Syy = fieldData(:, (X+1.0))';
Szz = fieldData(:, (X+2.0))';
Txy = fieldData(:, (X+3.0))';
Tyz = fieldData(:, (X+4.0))';
Txz = fieldData(:, (X+5.0))';

TENSOR = [Sxx; Syy; Szz; Txy; Tyz; Txz]';

fclose(fid);

%% Get element-nodal listing if required:

if nodeType == 2.0
    items = fieldData(:, 1.0)';
    
    if length(items) == 1
        IDs = [1.0, 1.0];
        nodalListing = -999.0;
        return
    end
    
    for i = 2.0:length(items)
        if items(i) ~= items(i-1.0)
            subIDs = i-1.0;
            break
        elseif i == length(items)
            subIDs = i;
            break
        end
    end
    
    mainIDs = floor(length(items)/subIDs);
    
    IDs = [mainIDs, subIDs];
end
end