import matplotlib.pyplot as plt
import numpy as np
import sys, os
sys.path.append(os.path.abspath(__file__)[:-19])
#sys.path.append('C:/Users/tusnin/Documents/Physics/PhD/epfl/PyCORe')
import PyCORe_main as pcm

import time

start_time = time.time()

Num_of_modes = 2**10
N_crow = 8

D2 = 1e6#-1*beta2*L/Tr*D1**2 ## From beta2 to D2
#old D2 = 4.1e6
D3 = 0
mu = np.arange(-Num_of_modes/2,Num_of_modes/2)
Dint_single = 2*np.pi*(mu**2*D2/2 + mu**3*D3/6)
Dint = np.zeros([mu.size,N_crow])
Dint = (Dint_single*np.ones([mu.size,N_crow]).T).T#Making matrix of dispersion with dispersion profile of j-th resonator on the j-th column
#dNu_ini = 8e9
#dNu_end = 10e9
dNu_ini = -15e9
dNu_end = 15e9
#dNu_ini = -1e9
#dNu_end = 1e9
#dNu_ini = -10e9
#dNu_end = -7e9
nn = 4000
ramp_stop = 0.99
dOm = 2*np.pi*np.concatenate([np.linspace(dNu_ini,dNu_end, int(nn*ramp_stop)),dNu_end*np.ones(int(np.round((1-ramp_stop)*nn)))])


J = 3e9*2*np.pi*np.ones([mu.size,(N_crow-1)])
J_EO = -3e9*2*np.pi*np.ones([mu.size,(N_crow)])
phase_EO = np.zeros([mu.size,(N_crow)])
for ii in range(1,N_crow):
    phase_EO[:,ii] = phase_EO[:,ii-1]+ np.pi/2

#delta = 0.1e9*2*np.pi
kappa_ex_ampl = 50e6*2*np.pi
kappa_ex = np.zeros([Num_of_modes,N_crow])

kappa_ex[:,0] = 1*kappa_ex_ampl*np.ones([Num_of_modes])
kappa_ex[:,-1] = 1*kappa_ex_ampl*np.ones([Num_of_modes])

Delta = np.zeros([mu.size,(N_crow)])



PhysicalParameters = {'Inter-resonator_coupling': J,
                      'Electro-optical coupling':J_EO,
                      'Electro-optical phase' : phase_EO,
                      'Resonator detunings' : Delta,
                      'n0' : 1.9,
                      'n2' : 2.4e-19,### m^2/W
                      'FSR' : 181.7e9 ,
                      'w0' : 2*np.pi*192e12,
                      'width' : 1.5e-6,
                      'height' : 0.85e-6,
                      'kappa_0' : 50e6*2*np.pi,
                      'kappa_ex' : kappa_ex,
                      'Dint' : Dint}

simulation_parameters = {'slow_time' : 10e-6,
                         'detuning_array' : dOm,
                         'noise_level' : 1e-6,
                         'output' : 'map',
                         'absolute_tolerance' : 1e-8,
                         'relative_tolerance' : 1e-8,
                         'max_internal_steps' : 2000}

P0 = 1.0### W
#P0 = 0.006### W
Pump = np.zeros([len(mu),N_crow],dtype='complex')
Pump[0,0] = np.sqrt(P0)


#%%
crow = pcm.Synthetic_CROW(PhysicalParameters)
#ev = crow.Linear_analysis()
#%%

map2d = crow.Propagate_SAMCLIB(simulation_parameters, Pump, BC='OPEN')
#map2d = crow.Propagate_SAMCLIB_PSEUD_SPECT(simulation_parameters, Pump)
#map2d = crow.Propagate_SAM(simulation_parameters, Pump)
#%%
plt.figure()
plt.plot(dOm/2/np.pi,np.mean(np.abs(map2d[:,:,0])**2,axis=1))
plt.plot(dOm/2/np.pi,np.mean(np.abs(map2d[:,:,1])**2,axis=1))

pcm.Plot_Map(np.fft.ifft(map2d[:,:,0],axis=1),np.arange(nn))
print("--- %s seconds ---" % (time.time() - start_time))
    