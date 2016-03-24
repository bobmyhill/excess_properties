import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data = np.loadtxt(fname='Fort_Moore_xrhovphi.dat', unpack=True)


compound_masses = [[78.11,    'benzene'],
                   [84.16,    'cyclohexane'],
                   [98.95,    'ethylene-dichloride'],
                   [153.82,   'carbon-tetrachloride'],
                   [119.38,   'chloroform'],
                   [112.56,   'chlorbenzene'],
                   [78.13,    'dimethyl-sulphoxide'],
                   [41.05,    'acetonitrile'],
                   [88.11,    'dioxan'],
                   [58.08,    'acetone'],
                   [167.848,  's-tetrachlorethane'],
                   [128.5563, 'o-chlorphenol'],
                   [18.01528, 'water'],
                   [32.04,    'methanol'],
                   [60.05,    'acetic acid']]

names = [[compound_masses[int(data[0][i])][1], compound_masses[int(data[1][i])][1]] for i in xrange(len(data[0]))]
for i, datum in enumerate(data[0]):
    data[0][i] = compound_masses[int(data[0][i])][0]
    data[1][i] = compound_masses[int(data[1][i])][0]

V_data = []
V_not_fit = []
K_S_data = []
K_S_not_fit = []
for i, datum in enumerate(zip(*data)):
    Xi   = np.array([datum[2], datum[5], datum[8],  datum[11], datum[14], datum[17]])
    rho  = np.array([datum[3], datum[6], datum[9],  datum[12], datum[15], datum[18]])
    vphi = np.array([datum[4], datum[7], datum[10], datum[13], datum[16], datum[19]])
    mass = Xi*datum[0] + (1. - Xi)*datum[1]
    volume = mass/rho
    ideal_volume = Xi*volume[-1] + (1. - Xi)*volume[0]
    K_S = vphi*vphi*rho

    #K_S = V*dP/dV
    # dV/dP is linear across the solution
    ideal_dVdP = Xi*volume[-1]/K_S[-1] + (1. - Xi)*volume[0]/K_S[0]
    ideal_K_S = ideal_volume / ideal_dVdP
    #plt.plot(Xi, ideal_K_S, marker='o')
    #plt.show()
    
    ratio_volume = volume/ideal_volume
    ratio_K_S = K_S/ideal_K_S
    
    if i<40: #i != 10 and i != 11:
        K_S_data.extend(ratio_K_S)
        V_data.extend(ratio_volume)
        if i<5:
            plt.plot(ratio_volume, ratio_K_S, marker='o', linestyle='None', label=names[i][0]+'-'+names[i][1])
        elif i<10:
            plt.plot(ratio_volume, ratio_K_S, marker='.', linestyle='None', label=names[i][0]+'-'+names[i][1])
        else:
            plt.plot(ratio_volume, ratio_K_S, marker='d', linestyle='None', label=names[i][0]+'-'+names[i][1])
    else:
        K_S_not_fit.extend(ratio_K_S)
        V_not_fit.extend(ratio_volume)
    

def linear(x, a):
    return a*(x - 1.) + 1.
def power(x, a):
    return np.power(x, a)

volumes = np.linspace(0.96, 1.012, 101)

#popt, pcov = curve_fit(linear, V_data, K_S_data)
#print popt[0], '+/-', pcov[0][0]
#plt.plot(volumes, linear(volumes, *popt), label='linear model, a='+str(popt[0])+'+/-'+str(pcov[0][0]))

#popt, pcov = curve_fit(power, V_data, K_S_data)
#print popt[0], '+/-', pcov[0][0]
#plt.plot(volumes, power(volumes, *popt), label='power law model, a='+str(popt[0])+'+/-'+str(pcov[0][0]))

plt.plot(volumes, power(volumes, -15.), label='power law model, a=-15')
plt.plot(volumes, power(volumes, -10.), label='power law model, a=-10')
plt.plot(volumes, power(volumes, -5.), label='power law model, a=-5')
plt.plot(volumes, power(volumes, -7./3.), label='power law model, a=-7/3')

#plt.plot(V_data, K_S_data, marker='o', linestyle='None', label='Fort and Moore (1965)')
#plt.plot(V_not_fit, K_S_not_fit, marker='x', linestyle='None', label='Fort and Moore (1965), involving water (not fit)')


xjdae = np.array([1., 0.74, 0.35, 0.])
Vjdae = np.array([402.21, 408.43, 418.54, 429.25])
Videaljdae = xjdae*402.21 + (1. - xjdae)*429.25
Kjdae = np.array([134.0, 130.4, 124.4, 116.1])
dVdPideal = xjdae*Vjdae[0]/Kjdae[0] + (1. - xjdae)*Vjdae[-1]/Kjdae[-1]
Kidealjdae = Videaljdae/dVdPideal
plt.plot(Vjdae/Videaljdae, Kjdae/Kidealjdae, marker='s', linestyle='None', label='Nestola et al., 2006 (jd-aeg)')


xjdhd = np.array([1., 0.53, 0.24, 0.])
Vjdhd = np.array([402.26, 424.90, 439.46, 450.84])
Videaljdhd = xjdhd*402.26 + (1. - xjdhd)*450.84
Kjdhd = np.array([134.0, 120.7, 113.5, 108.8])
dVdPideal = xjdhd*Vjdhd[0]/Kjdhd[0] + (1. - xjdhd)*Vjdhd[-1]/Kjdhd[-1]
Kidealjdhd = Videaljdhd/dVdPideal
plt.plot(Vjdhd/Videaljdhd, Kjdhd/Kidealjdhd, marker='s', linestyle='None', label='Nestola et al., 2007 (jd-hed)')


plt.xlim(0.97, 1.03)
plt.ylim(0.9, 1.2)
plt.legend(loc='upper right')
plt.show()


