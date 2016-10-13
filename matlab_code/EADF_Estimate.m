function [ est_azim, est_elev ] = EADF_Estimate( hlk )

assert(isa(hlk, 'double') && ~isreal(hlk) && all(size(hlk) == [4,1]))

%EADF_Estimate returns the indeces for the DoA and ToA parameters that
%correspond to DoA and ToA estimates
%
% INPUTS:
% hlk       = channel estimate
%
% LOADED:
% Glk_H     = EADF for horizontal polarization
% Glk_V     = EADF for vertical polarization
% Mf        = Number of frequency bins in the measured array response
% MAN       = Number of antenna elements
% Ma        = Number of azimuth points in the measured array response
% Me        = Number of elevation points in the measured array response
% FFT_freq  = Number of FFT points in the frequency dimension
% FFT_ang   = Number of FFT points in the angular dimensions
%
% OUTPUTS:
% ind_elev  = elevation index of the maximum entry
% ind_azim  = azimuth index of the maximum entry
% ind_freq  = frequency index of the maximum entry
persistent antennaCal Glk_H Glk_V MAN Me Ma
if isempty(antennaCal)
    vals = coder.load('acal_theoretical_monopole.mat');
    antennaCal = vals.antennaCal;
    
    % Importing measurement parameters
    [Mf, MAN, Me, Ma] = size(antennaCal.EPhi);
    
    % Get the horizontal and vertical components of the data
    % at the "middle" subcarrier
    mid_freq = round(Mf/2);
    Ephi   = squeeze(antennaCal.EPhi(mid_freq,:,:,:));
    Etheta = squeeze(antennaCal.ETheta(mid_freq,:,:,:));
    
    
    %% EADF GENERATION
    
    % Choose the number of modes for truncating the expansion
    % NOTE: numbers must be odd
    Ma = 179;
    Me = 179;
    
    % Calculate the EADF through the FFT approach
    Glk_H = EADF_FFT(Ephi, Ma, Me);
    Glk_V = EADF_FFT(Etheta, Ma, Me);

end


Mf = 1;

% Setting the number of estimation points
FFT_freq = 1;
FFT_ang = 2^10;

%% %%%%%%%%%%%%%%%%%%%%%%
% Reshaping the measured channel data
Hlk = reshape(hlk, [Mf, MAN]);

% Correlating the measured channel with the EADFs
AH = reshape(Hlk * conj(Glk_H), [Mf, Me, Ma]);
AV = reshape(Hlk * conj(Glk_V), [Mf, Me, Ma]);

% 3D FFTs
BH = abs(fftn(AH, [FFT_freq, FFT_ang, FFT_ang])).^2;
BV = abs(fftn(AV, [FFT_freq, FFT_ang, FFT_ang])).^2;

% Adding up both polarizations
tot_mat = BH + BV;

% Find the maximum entry
[~, max_ind] = max(abs(tot_mat(:)));

% Find the indeces of the maximum entry
[ind_freq, ind_elev, ind_azim] = ind2sub(size(tot_mat), max_ind);


%% Plotting the combined FFT (just for checking, can be removed)

% % X- and Y-axis
% azim_vec = linspace(-180, 180-360/FFT_ang, FFT_ang);
% elev_vec = linspace(0, 360-360/FFT_ang, FFT_ang);
% 
% % Limiting the least significant peaks in order to improve readibility
% plot_tot_mat = 10*log10(abs(tot_mat));
% min(min(min(plot_tot_mat)));  
% max(max(max(plot_tot_mat)));
% cut_point = (min(min(min(plot_tot_mat))) + ...
%              max(max(max(plot_tot_mat))))*0.7;
% plot_tot_mat(plot_tot_mat < cut_point) = cut_point;

% % 3D surf plot
% figure
% hh = surf(azim_vec.', elev_vec.', ...
%     reshape(plot_tot_mat(1,:,:), ...
%     length(elev_vec), length(azim_vec)));
% set(hh, 'LineStyle', 'none');
% xlabel('Azimuth'); ylabel('Elevation');

%% Convert to angles

% Vectors corresponding to the points in the 3D FFT processing
azim_vec = linspace(-180, 180-360/FFT_ang, FFT_ang);
% azim_vec = [0:0.5:180, -179.5:0.5:-0.5];
elev_vec = linspace(0, 360-360/FFT_ang, FFT_ang);

% DoA and ToA estimates
est_azim = azim_vec(ind_azim);
est_elev = elev_vec(ind_elev);
%est_freq = freq_vec(ind_freq) / 2*pi*f0;

% Correcting the possible overflows due to the elevation angle periodicity 
if est_elev > 180
    est_elev = 360 - est_elev;
    
    % NOTE: Based on eq. (4.18) in "Unified Array Manifold Decomposition 
    % Based on Spherical Harmonics and 2-D Fourier Basis". However, this 
    % is a slightly different correction since the azimuth is now
    % defined from -180 to +180deg. 
    est_azim = est_azim + 180;
    
    % Limit the results to -180...+180 degrees
    if est_azim > 180
        est_azim = est_azim - 360;
    elseif est_azim < -180
        est_azim = est_azim + 360;
    end
    
end

% Mapping the directions in case of ULA
if strcmp(antennaCal.arrayType, 'ULA')
    % Map the directions behind the ULA to the front of ULA
    % NOTE: ULA is not able to distinguish between directions in
    % front and back of it --> direction ambiguity
    if est_azim > 90
        est_azim = 180 - est_azim;
    elseif est_azim < -90
        est_azim = 180 + est_azim;
    end
end

% Display the estimates in the command window
fprintf('(est) Azimuth %3.3f | Elevation %3.3f\n',est_azim,est_elev);

end