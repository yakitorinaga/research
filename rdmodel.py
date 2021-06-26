import PyDSTool as dst
import numpy as np

# we must give a name
DSargs = dst.args(name='rdmodel')
# parameters
#変数{V,n,h,Ca_i,K_o,Na_i}
DSargs.pars = {
               'beta':7.0,
               'rho':1.2,
               'G_glia':-66.0,
               'eps':1.2,
               'k_oinf':2.0,#(8.02で分岐点)(70.0~71.0に分岐点)
               'alpha_K':1.0,
               'alpha_Na':1.0,
               'A_1':0.75,
               'B_1':0.93,
               'mu_1':2.6,
               'lambda_2':7.41,
               'sigma_2':2.0,
               'mu_2':2.6,
               'sigma_3':35.7,
               'mu_3':1.94,
               'lambda_3':24.3,
               'sigma_4':0.88,
               'mu_4':1.48,
               'lambda_4':24.6,
               'g_1Na':1.5,
               'A_1K':2.6,
               'lambda_1K':32.5,
                }
# auxiliary helper function(s) -- function name: ([func signature], definition)
DSargs.fnspecs  = {
                   'K_i':(['Na_i'],'140.0+(18.0 - Na_i)'),
                   'Na_o':(['Na_i'],'144.0-beta*(Na_i-18.0)'),
                   'I_pump':(['Na_i','K_o'],'((rho)/(1.0+exp((25.0-Na_i)/3.0)))*(1.0/(1.0+exp(5.5-K_o)))'),#5.5or8.0
                   'I_glia':(['K_o'],'G_glia/(1.0+exp((18.0-K_o)/2.5))'),
                   'I_diff':(['K_o'],'eps*(K_o-(k_oinf))'),
                   'K_oi':(['Na_i','K_o'],'K_o/K_i(Na_i)'),
                   'Na_io':(['Na_i'],'Na_i/Na_o(Na_i)'),
                   'g_1':(['Na_i'],'420.0*(1.0-A_1*(1.0-B_1*exp(-mu_1*Na_io(Na_i)))**(1.0/3.0))'),
                   'g_2':(['Na_i','K_o'],'exp(sigma_2*(1.0-lambda_2*K_oi(Na_i,K_o))/(1.0+exp(-mu_2*Na_io(Na_i))))'),
                   'g_3':(['Na_i','K_o'],'(1.0/((1.0+exp(sigma_3*(1.0+mu_3*Na_io(Na_i)-lambda_3*K_oi(Na_i,K_o))))**(5.0)))'),
                   'g_4':(['Na_i','K_o'],'(1.0/((1.0+exp(sigma_3*(1.0+mu_3*Na_io(Na_i)-lambda_3*K_oi(Na_i,K_o))))**(5.0)))'),
                   'g_1K':(['Na_i','K_o'],'A_1K*exp(-lambda_1K*K_oi(Na_i,K_o))'),
                   'I_Kinf':(['Na_i','K_o'],'alpha_K*(g_1(Na_i)*g_2(Na_i,K_o)*g_3(Na_i,K_o)+g_1K(Na_i,K_o))'),
                   'I_Nainf':(['Na_i','K_o'],'alpha_Na*(g_1(Na_i)*g_2(Na_i,K_o)*g_4(Na_i,K_o)+g_1Na)'),
                 }
        

DSargs.varspecs = { 
                   'K_o':'(-0.33)*I_Kinf(Na_i,K_o)-2.0*beta*I_pump(Na_i,K_o)-I_glia(K_o)-I_diff(K_o)',
                   'Na_i':'0.33*(I_Nainf(Na_i,K_o)/beta)-3.0*I_pump(Na_i,K_o)',
                   }
# initial conditions
DSargs.ics      = {'K_o':7.0,'Na_i':17.0}
DSargs.xdomain = {'K_o':[-1000.0,1000.0],'Na_i':[-1000.0,1000.0]}
#Normal comdition G_glia=66,K_o=4.0,k_oinf=4.0,eps=1.2