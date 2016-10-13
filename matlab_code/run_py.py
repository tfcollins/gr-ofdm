import scipy.io as sio
import numpy as np

def ind2sub(array_shape, ind):
    rows = (ind.astype('int') / array_shape[1])
    cols = (ind.astype('int') % array_shape[1]) # or numpy.mod(ind.astype('int'), array_shape[1])
    return (rows, cols)

def convert2angles(FFT_ang,  ind_elev, ind_azim):
    azim_vec = np.linspace(-180, 180-360/FFT_ang, num=FFT_ang)
    elev_vec = np.linspace(0, 360-360/FFT_ang, num=FFT_ang)

    est_azim = azim_vec[ind_azim]
    est_elev = elev_vec[ind_elev]

    if est_elev > 180:
        est_elev = 360 - est_elev
        est_azim = est_azim + 180

        if est_azim > 180:
            est_azim = est_azim - 360
        elif est_azim < -180:
            est_azim = est_azim + 360

    if est_azim > 90:
        est_azim = 180 - est_azim
    elif est_azim < -90:
        est_azim = 180 + est_azim

    return (est_azim, est_elev)

#### OFFLINE
# Read data from MATLAB
m = sio.loadmat('acal_theoretical_monopole.mat')
antennaCal = m['antennaCal']
EPhi = antennaCal['EPhi'][0][0]
dimensions = EPhi.shape

Glk_H = np.mat(antennaCal['Glk_H'][0][0]).conj()
Glk_V = np.mat(antennaCal['Glk_V'][0][0]).conj()

Mf = antennaCal['Mf'][0][0][0][0]
Me = antennaCal['Me'][0][0][0][0]
Ma = antennaCal['Ma'][0][0][0][0]

Hlk = np.mat(np.array([1,1,1,1], ndmin=2, dtype=complex))

FFT_freq = 1
FFT_ang = 2**10


### Online
# Compute Estimates
conv_H = Hlk*Glk_H
conv_V = Hlk*Glk_V

AH = conv_H.reshape(Mf, Me, Ma)
AV = conv_V.reshape(Mf, Me, Ma)

BH = np.abs( np.fft.fftn(AH, s=(FFT_ang, FFT_ang)) )**2
BV = np.abs( np.fft.fftn(AV, s=(FFT_ang, FFT_ang)) )**2

tot_mat = BH + BV
print tot_mat[0,0]
print tot_mat[0,1]
print tot_mat[0,2]
max_ind = np.argmax(np.abs(tot_mat))

print max_ind
(ind_azim, ind_elev) = ind2sub(tot_mat.shape, (max_ind))

print convert2angles(FFT_ang,  ind_elev, ind_azim)

# BH = abs(fftn(AH, [FFT_freq, FFT_ang, FFT_ang])).^2;
# BV = abs(fftn(AV, [FFT_freq, FFT_ang, FFT_ang])).^2;
