import sys
sys.path.append('/Users/nagatomoyuuya/Documents/修論研究/fullmodel/')
import fmmodel as fm

import PyDSTool as dst
import numpy as np
from matplotlib import pyplot as plt
from PyDSTool.Toolbox import phaseplane as pp

#bar(k_oinf)=2.0=>70.0
#
fm.DSargs.tdomain = [0,100]                    
ode  = dst.Generator.Vode_ODEsystem(fm.DSargs)
ode.set(pars = {'k_oinf':40.0})
for i, eps0 in enumerate(np.linspace(0.7,0.8,30)):
    for j, G_glia0 in enumerate(np.linspace(23,24,20)):
        fig=plt.figure()
        ode.set(pars = {'G_glia':G_glia0})
        ode.set(pars = {'eps':eps0})
        traj = ode.compute('polarization')
        pts  = traj.sample(dt=0.00001)
        #fp_coord = pp.find_fixedpoints(ode, n=4, eps=1e-8)[0]
        # #nulls_x, nulls_y = pp.find_nullclines(ode, 'v', 'w', n=3, eps=1e-8, max_step=0.01,fps=[fp_coord])
        plt.xlabel('t')
        plt.ylabel('V')
        plt.ylim([-100.0,100.0])
        plt.grid()
        plt.title(ode.name+'k_oinf=40.0_G_glia=%f,eps=%f'%(G_glia0,eps0))
        #plt.plot(nulls_x[:,0], nulls_x[:,1],linestyle="dashed")
        #plt.plot(nulls_y[:,0], nulls_y[:,1],linestyle="dashed")
        plt.plot(pts['t'],pts['V'])
        fig.savefig("test/figure_V_%d,%d"%(i,j))
        plt.close()