%% --------------------------------------------------
% Aki Hakkarainen & Mike Koivisto
% Tampere University of Technology, Finland
% 2016
% aki.hakkarainen@tut.fi, mike.koivisto@tut.fi
% ---------------------------------------------------


%% PARAMETERS

Mf  = 1;    % Number of frequencies 9
MAN = 4;    % Number of antenna elements
Ma  = 256;  % Number of azimuth points 180
Me  = 257;   % Number of elevation points 91

fc = 2.45e9;     % carrier frequency
f0 = 312.5e3;   % subcarrier spacing

% Choose the number of modes for truncating the expansion
% NOTE: numbers must be odd
Ma_glk = 179;
Me_glk = 179;

% Pilot frequencies (this can be set also manually based on measurements)
pilot_freqs = fc + f0*(-(Mf-1)/2:1:(Mf-1)/2);

% Select the array structure
array_structure = 1;    % 1 = ULA, 0 = URA (square)
if array_structure == 1
    array_type = 'ULA';
elseif array_structure == 0
    array_type = 'URA';
end

% Displaying the parameters for the user
disp_text = ...
    ('Generating array calibration data with monopoles and the following parameters:\n');
disp_text = [disp_text, 'Array type:                  ', ...
    array_type, '\n'];
disp_text = [disp_text, 'Number of antennas:          ', ...
    num2str(MAN), '\n'];
disp_text = [disp_text, 'Carrier frequency:           ', ...
    num2str(fc), ' Hz\n'];
disp_text = [disp_text, 'Subcarrier spacing:          ', ...
    num2str(f0), ' Hz\n'];
disp_text = [disp_text, 'Number of pilot frequencies: ', ...
    num2str(Mf), '\n'];
disp_text = [disp_text, 'Number of azimuth points:    ', ...
    num2str(Ma), '\n'];
disp_text = [disp_text, 'Number of elevation points:  ', ...
    num2str(Me), '\n'];
disp_text = sprintf(disp_text);
disp(disp_text)

%% ANGULAR GRID

% NOTE: azimuth directions are defined with respect to antenna broadside
% NOTE: Here elevation is defined -90...+90deg, e.g. from pole to pole 
% due to limitation of Phased toolbox. However, everywhere else pole to
% pole corresponds to 0...180deg. 
anglesPhiDeg   = linspace(-180, 180-360/Ma, Ma).'; % Azimuth
anglesThetaDeg = linspace(-90, 90, Me).'; % Elevation


%% DATA GENERATION

% Generate a single monopole antenna element (quarter-wave length)
% monopole_ant = monopole('Height', ...
%     physconst('LightSpeed')/(4*fc), ...
%     'GroundPlaneWidth', 0.05, 'GroundPlaneLength', 0.05);

monopole_ant = monopole('Height', ...
    physconst('LightSpeed')/(4*fc), ...
    'Width', 0.001,...
    'GroundPlaneWidth', 0.05, 'GroundPlaneLength', 0.05);


% Init
EPhi   = zeros(Mf, MAN, Me, Ma);
ETheta = zeros(Mf, MAN, Me, Ma);

% Element spacing is equal to lambda/2
element_spacing = physconst('LightSpeed')/(2*fc);

if array_structure == 1 % ULA

    % Generate a ULA with monopoles
    ant_array = phased.ULA('Element', monopole_ant, 'NumElements', MAN, ...
        'ElementSpacing', element_spacing);
    
    % Array type string for saving
    array_type = 'ULA';
    
elseif array_structure == 0 % URA (square)
    
    % Sanity check for MAN
    if (sqrt(MAN) - round(sqrt(MAN))) ~= 0
        error('Number of antennas must be quadratic')
    end
    
    % Generate a URA with monopoles
    ant_array = phased.URA('Element', monopole_ant, ...
        'Size', [sqrt(MAN), sqrt(MAN)], ...
        'ElementSpacing', [element_spacing, element_spacing], ...
        'ArrayNormal', 'z');
    
    % Array type string for saving
    array_type = 'URA';
    
end

% Set up the steering vector calculation
hsv = phased.SteeringVector('SensorArray',ant_array, ...
    'IncludeElementResponse', true, 'EnablePolarization', true);

for ff = 1:1:Mf % over all pilot frequencies
    for aa = 1:1:Ma % over all azimuth points
        for ee = 1:1:Me % over all elevation points
            
            % Calculate array response                      
            array_response = step(hsv, pilot_freqs(ff), ...
                [anglesPhiDeg(aa); anglesThetaDeg(ee)]);
            
            % Horizontal and vertical polarizations
            EPhi(ff,:,ee,aa) = array_response.H;
            ETheta(ff,:,ee,aa) = array_response.V;
        end
    end
end

%% Extra precompute
% Importing measurement parameters
% [Mf, MAN, ~, ~] = size(EPhi);

% Get the horizontal and vertical components of the data
% at the "middle" subcarrier
mid_freq = round(Mf/2);
Ephi_T   = squeeze(EPhi(mid_freq,:,:,:));
Etheta_T = squeeze(ETheta(mid_freq,:,:,:));


% EADF GENERATION



% Calculate the EADF through the FFT approach
Glk_H = EADF_FFT(Ephi_T, Ma_glk, Me_glk);
Glk_V = EADF_FFT(Etheta_T, Ma_glk, Me_glk);

%% SAVING THE DATA

% Generate a struct
antennaCal = struct('EPhi', EPhi, 'ETheta', ETheta, ...
    'anglesPhi', anglesPhiDeg/180*pi, ...
    'anglesTheta', anglesThetaDeg/180*pi, ...
    'numOfPhiSteps', Ma_glk, 'numOfThetaSteps', Me_glk, ...
    'arrayType', array_type, ...
    'Glk_H', Glk_H, ...
    'Glk_V', Glk_V, ...
    'MAN', MAN, 'fc', fc, 'f0', f0, 'Ma', Ma_glk, 'Me', Me_glk, 'Mf', Mf);

% Save the struct to a file
save('acal_theoretical_monopole.mat', 'antennaCal');

fprintf('Array data ready\n\n')
