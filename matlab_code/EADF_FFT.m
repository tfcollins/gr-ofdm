function [ G ] = EADF_FFT(array_resp, Maz, Mel)
%EADF_FFT Calculates the EADF through a simple FFT processing
%
%   INPUTS:
%   array_resp  = predefined antenna array beam patterns
%   Maz         = number of azimuth levels to be used in processing
%   Mel         = number of elevation levels to be used in processing
%
%   OUTPUT:
%   G           = EADF for all antenna elements, dimensions N x Maz*Mel


%% --------------------------------------------------
% Aki Hakkarainen & Mike Koivisto
% Tampere University of Technology, Finland
% 2016
% aki.hakkarainen@tut.fi, mike.koivisto@tut.fi
% ---------------------------------------------------


%% Code

% Importing measurement parameters
[N, NumEl, NumAz] = size(array_resp);

% Parameters for truncating the FFT
HigherModeEl = (Mel-1)/2;
HigherModeAz = (Maz-1)/2;

% Indeces for the middle entries
middleAz = round(NumAz/2);
middleEl = round(NumEl-1);

% Init
G = complex(zeros(N, Maz*Mel));

% Loop over antenna elements
for nn = 1:N
    
    % Beam pattern of the nn^th antenna
    B_sensor = squeeze(array_resp(nn,:,:));
    
    % Build the periodic beam pattern
    % NOTE: This is necessary to make also elevation dimesion periodic
    B_r = circshift(B_sensor,[0 NumAz/2]);
    B_r = flip(B_r,1);
    B_r = B_r(2:end-1,:);
    B_p = [B_sensor; -B_r];
    
    % 2D FFT
    G_aux = fftshift(fft2(B_p));
    
    % Pick up only the most significant frequency components
    G_aux = G_aux(middleEl-HigherModeEl+1:middleEl+HigherModeEl+1,...
        middleAz-HigherModeAz+1:middleAz+HigherModeAz+1);
    
    % Reshaping the results
    G(nn,:) = reshape(G_aux, 1, Maz*Mel);
    
end;

end

