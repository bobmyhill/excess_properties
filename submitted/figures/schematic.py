import os, sys, numpy as np, matplotlib.pyplot as plt

T = 298.

W12 = 10000.
W21 = 20000.

compositions=np.linspace(0.00000001, 0.99999999, 101)
TS_conf = np.empty_like(compositions)
Xs = np.empty_like(compositions)
G1 = np.empty_like(compositions)
G2 = np.empty_like(compositions)
G = np.empty_like(compositions)
for i, X in enumerate(compositions):
    TS_conf[i] = 8.3145*T*(X*np.log(X) + (1.-X)*np.log(1.-X))
    Xs[i] = X*(1.-X)*(W12*(1.-X) + W21*X)

    G[i] = Xs[i] - TS_conf[i]

    G1[i] = X*(1.-X)*W12 - TS_conf[i]
    G2[i] = X*(1.-X)*W21 - TS_conf[i]

    
plt.plot(compositions, TS_conf)
plt.plot(compositions, G1)
plt.plot(compositions, G2)
plt.plot(compositions, G)
plt.show()

filename = 'schematic.dat'
f = open(filename, 'w')

for i, c in enumerate(compositions):
    f.write(str(c)+' '+str(TS_conf[i])+' '+str(G1[i])+' '+str(G2[i])+' '+str(G[i])+'\n')
    
f.close()
