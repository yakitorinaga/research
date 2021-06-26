import sys
sys.path.append('/Users/nagatomoyuuya/Documents/修論研究/fullmodel/')
import fmmodel as fm

import PyDSTool as dst
import numpy as np
from matplotlib import pyplot as plt
from PyDSTool.Toolbox import phaseplane as pp

fm.DSargs.tdomain = [0,50]               
ode  = dst.Generator.Vode_ODEsystem(fm.DSargs)
ode.set(pars = {'k_oinf':9.0})
for i, k0 in enumerate(np.linspace(0.0,100.0,100)):
    fig=plt.figure()
    ode.set(pars = {'k_oinf':k0 })
    traj = ode.compute('polarization')
    pts  = traj.sample(dt=0.0001)
    #fp_coord = pp.find_fixedpoints(ode, n=4, eps=1e-8)[0]
    #nulls_x, nulls_y = pp.find_nullclines(ode, 'v', 'w', n=3, eps=1e-8, max_step=0.01,fps=[fp_coord])
    plt.xlabel('t')
    plt.ylabel('V')
    plt.ylim([-100.0,100.0])
    plt.grid()
    plt.title(ode.name+'_k_oinf=%f'%(k0))
    #plt.plot(nulls_x[:,0], nulls_x[:,1],linestyle="dashed")
    #plt.plot(nulls_y[:,0], nulls_y[:,1],linestyle="dashed")
    plt.plot(pts['t'],pts['V'])
    fig.savefig("k_oinf_anime/figure_V_%d"%(i))
    plt.close()
