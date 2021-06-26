import PyDSTool as dst

# we must give a name
DSargs = dst.args(name='fmmodel')
# parameters
#変数{V,n,h,Ca_i,K_o,Na_i}
DSargs.pars = {
               'C':1.0,
               'g_Na':100.0,
               'g_K':40.0,
               'g_AHP':0.01,
               'g_KL':0.05,
               'g_NaL':0.0175,
               'g_ClL':0.05,
               'phi':3.0,
               'V_Cl':-81.93,
               'g_Ca':0.1,
               'V_Ca':120.0,
               'beta':7.0,
               'rho':1.25,
               'G_glia':66.0,
               'eps':1.2,
               'k_oinf':2.0,#(8.02で分岐点)(70.0~71.0に分岐点)
               'Cl_i':6.0,
               'Cl_o':130.0
                }
# auxiliary helper function(s) -- function name: ([func signature], definition)
DSargs.fnspecs  = {
                   'K_i':(['Na_i'],'140.0+(18.0-Na_i)'),
                   'Na_o':(['Na_i'],'144.0-beta*(Na_i-18.0)'),
                   'V_Na':(['Na_i'],'26.64*log(Na_o(Na_i)/Na_i)'),
                   'V_K':(['Na_i,K_o'],'26.64*log(K_o/K_i(Na_i))'),
                   #'V_Cl':(['Cl_i'],'26.64*log(Cl_i/Cl_o)'),
                   'alpha_m':(['V'],'0.1*(V+30.0)/(1.0-exp(-0.1*(V+30.0)))'),
                   'beta_m':(['V'],'4.0*exp(-(V+55.0)/18.0)'),
                   'm_inf':(['V'],'(alpha_m(V))/(alpha_m(V)+beta_m(V))'),
                   'alpha_n':(['V'],'(0.01*(V+34.0))/(1.0-exp(-0.1*(V+34.0)))'),
                   'beta_n':(['V'],'0.125*exp(-(V+44.0)/80.0)'),
                   'alpha_h':(['V'],'0.07*exp(-(V+44.0)/20.0)'),
                   'beta_h':(['V'],'1.0/(1.0+exp(-0.1*(V+4.0)))'),
                   'I_Na':(['V','h','Na_i'],'-1.0*g_Na*(m_inf(V)**(3.0))*h*(V-V_Na(Na_i))-g_NaL*(V-V_Na(Na_i))'),
                   'I_K':(['V','n','Ca_i','K_o','Na_i'],'-1.0*(g_K*(n**(4.0))+(g_AHP*Ca_i)/(1.0+Ca_i))*(V-V_K(Na_i,K_o))-g_KL*(V-V_K(Na_i,K_o))'),
                   'I_Cl':(['V'],'-1.0*g_ClL*(V-V_Cl)'),
                   'I_pump':(['Na_i','K_o'],'(rho/(1.0+exp((25.0-Na_i)/3.0)))*(1.0/(1.0+exp(5.5-K_o)))'),
                   'I_glia':(['K_o'],'G_glia/(1.0+exp((18.0-K_o)/2.5))'),#符号不明
                   'I_diff':(['K_o'],'eps*(K_o-k_oinf)'),
                 }

DSargs.varspecs = { 
                   'V':'(1.0/C)*(I_Na(V,h,Na_i)+I_K(V,n,Ca_i,K_o,Na_i)+I_Cl(V))',
                   'n':'phi*((alpha_n(V)*(1.0-n))-(beta_n(V)*n))',
                   'h':'phi*((alpha_h(V)*(1.0-h))-(beta_h(V)*h))',
                   'Ca_i':'((-0.002*g_Ca*(V-V_Ca))/(1.0+exp(-(V+25.0)/2.5)))-(Ca_i/80.0)',
                   'K_o':'-0.33*I_K(V,n,Ca_i,K_o,Na_i)-2.0*beta*I_pump(Na_i,K_o)-I_glia(K_o)-I_diff(K_o)',#符号不明
                   'Na_i':'0.33*(I_Na(V,h,Na_i)/beta)-3.0*I_pump(Na_i,K_o)'
                   }
# initial conditions
#nの初期値で計算が壊れるのでなにかがおかしい
DSargs.ics      = {'V':-62.0, 'n':0.6,'h':0.01,'Ca_i':20.0,'K_o':7.0,'Na_i':17.0}
DSargs.xdomain = {'V': [-1000.0,1000.0], 'n': [-1000.0,1000.0],'h':[-1000.0,1000.0],'Ca_i':[-1000.0,1000.0],'K_o':[-1000.0,1000.0],'Na_i':[-1000.0,1000.0]}
#Normal comdition G_glia=66,K_o=4.0,k_oinf=4.0,eps=1.2