#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Travis F. Collins <travisfcollins@gmail.com>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np
import scipy.io as sio
from random import randint
import timeit

class my_graph(object):
    """
    docstring for block eadf_doa
    """
    def __init__(self, matfilename, num_ants):

        # Read data from MATLAB about the EADF function and FFT versions
        m = sio.loadmat(matfilename)
        antennaCal = m['antennaCal']
        EPhi = antennaCal['EPhi'][0][0]
        dimensions = EPhi.shape

        # Set Parameters
        self.Glk_H = np.mat(antennaCal['Glk_H'][0][0]).conj()
        self.Glk_V = np.mat(antennaCal['Glk_V'][0][0]).conj()

        self.Mf = antennaCal['Mf'][0][0][0][0]
        self.Me = antennaCal['Me'][0][0][0][0]
        self.Ma = antennaCal['Ma'][0][0][0][0]

        # FFT resolution
        self.FFT_freq = 1
        self.FFT_ang = 256 # Main performance problem

        # System parameters
        self.matfilename = matfilename
        self.num_ants = num_ants

    def ind2sub(self, array_shape, ind):
        rows = (ind.astype('int') / array_shape[1])
        cols = (ind.astype('int') % array_shape[1]) # or numpy.mod(ind.astype('int'), array_shape[1])
        return (rows, cols)

    def convert2angles(self, FFT_ang,  ind_elev, ind_azim):
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


    def doa_est(self, Hlk):

        # Convolve response
        conv_H = Hlk*self.Glk_H
        conv_V = Hlk*self.Glk_V

        AH = conv_H.reshape(self.Mf, self.Me, self.Ma)
        AV = conv_V.reshape(self.Mf, self.Me, self.Ma)

        # FFT (Truncate) and make real
        BH = np.abs( np.fft.fftn(AH, s=(self.FFT_ang, self.FFT_ang)) )**2
        BV = np.abs( np.fft.fftn(AV, s=(self.FFT_ang, self.FFT_ang)) )**2

        # Combine polarizations
        tot_mat = BH + BV

        # Search for most likely direction
        max_ind = np.argmax(np.abs(tot_mat))
        (ind_azim, ind_elev) = self.ind2sub(tot_mat.shape, (max_ind))
        print self.convert2angles(self.FFT_ang,  ind_elev, ind_azim)

    def process_msg(self, chan_est):
        # chan_est = pmt.to_python(msg)

        # Convert estimates to matrix
        Hlk = np.mat(np.array(np.ones((1,self.num_ants)), ndmin=2, dtype=complex))

        # Take middle subcarrier
        subcarrier = int(round(len(chan_est[0])/2))

        # Take one subcarrier from each antenna
        for i in range(self.num_ants):
            Hlk[0,i] = chan_est[i][subcarrier]

        # Estimate DoA
        self.doa_est(np.mat(Hlk))

filename = "/home/travis/Dropbox/PHD/WiFiUS/doa/gnuradio/gr-ofdm/matlab_code/acal_theoretical_monopole.mat"
num_ants = 4
eadf = my_graph(filename, num_ants)
subcarriers = 200
chan_est = []
for i in range(num_ants):
    chan_est.append([])
    for k in range(subcarriers):
        chan_est[i].append(randint(0,9))

runs = 100
import time
start = time.time()

for x in range(runs):
    eadf.process_msg(chan_est)

done = time.time()
elapsed = done - start
print str(runs/elapsed)+" Estimates/Second"
