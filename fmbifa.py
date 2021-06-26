import sys
sys.path.append('/Users/nagatomoyuuya/Documents/修論研究/fullmodel/')
import fmmodel as fm
import PyDSTool as dst
import numpy as np
from matplotlib import pyplot as plt
from PyDSTool.Toolbox import phaseplane as pp
from PyDSTool import PyCont


fm.DSargs.tdomain = [0,200]                         
testDS = dst.Generator.Dopri_ODEsystem(fm.DSargs) 
PC = dst.ContClass(testDS)            # Set up continuation class


PCargs = dst.args(name='EQ1', type='EP-C')
PCargs.freepars     = ['eps']          
PCargs.MaxNumPoints = 1000     # The following 3 parameters are set after trial-and-error
PCargs.MaxStepSize  = 1
PCargs.MinStepSize  = 1e-5
PCargs.StepSize     = 1e-2
PCargs.VarTol = 1e-16
PCargs.FuncTol = 1e-16
PCargs.TestTol = 1e-16
PCargs.LocBifPoints = 'all'                 # detect limit points / saddle-node bifurcations
PCargs.SaveEigen    = True                     # to tell unstable from stable branches
PC.newCurve(PCargs)
PC['EQ1'].forward()
PC['EQ1'].backward()

#PCargs = dst.args(name='LC1', type='LC-C')
#PCargs.initpoint = 'EQ1:H1'
#PCargs.MaxNumPoints = 100
#PCargs.MinStepSize = 1e-2				
#PCargs.StepSize = 4e-1		
#PCargs.LocBifPoints = 'all'
#PCargs.NumSPOut = 10;	
#PCargs.SolutionMeasures = 'all'
#PCargs.freepars = ['I']
#PC.newCurve(PCargs)
#PC['LC1'].forward()

PC.display(['eps','K_o'], stability=True, figure=1)

plt.show()