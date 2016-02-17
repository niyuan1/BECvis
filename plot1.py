#Program plots various trajectories of BEC evolution

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

names = ['10', '11', '12', '13', '14', '15']
plot = 'HR'

ts = []
Teffs = []
Ls = []
Ycs = []
for name in names:
    #read data
    t, Tc, Yc, Lh, Lhe, M, sev, Teff, L, logpc, Lc, Lv, Mw, Tmax, pTmax, MrTmax = np.loadtxt(str(name)+'.plot1', dtype='string', unpack=True)

    #format data
    t = np.array([float(s.split('D')[0])*10**int(s.split('D')[1]) for s in t])
    Teff = np.array([float(T.split('D')[0])*10**int(T.split('D')[1]) for T in Teff])
    L = np.array([float(B.split('D')[0])*10**int(B.split('D')[1]) for B in L])
    Yc = np.array([float(H.split('D')[0])*10**int(H.split('D')[1]) for H in Yc[Yc!='4.000000000-100']])

    print name+': '+str(len(t))

    #convert to log
    Teff = np.log10(Teff)

    #append to list
    ts.append(t)
    Teffs.append(Teff)
    Ls.append(L)
    Ycs.append(Yc)

#plot data
if plot == 'Lt':
    plt.title("Dynamic Trajectory for " +str(names)+ " stars")
    for i in range(len(names)):
        plt.plot(ts[i], Ls[i], '.', label=name)
    plt.xlabel('time (yrs)')
    plt.ylabel('Luminotsity (log LS)')
elif plot == 'Tt':
    plt.title("Dynamic Trajectory for " +str(names)+ " stars")
    for i in range(len(names)):
        plt.plot(ts[i], Teffs[i], '.', label=name)
    plt.xlabel('time (yrs)')
    plt.ylabel('Temperature (log K)')
elif plot == 'HR':
    plt.title("HR Trajectory for " +str(names)+ " stars")
    for i in range(len(names)):
        plt.plot(Teffs[i], Ls[i], '.', label=name)
    plt.xlabel('Temperature (log K)')
    plt.ylabel('Luminotsity (log LS)')
    Trange = np.amax(Teff) - np.amin(Teff)
    plt.xlim(np.amax(Teff)+Trange/10,np.amin(Teff)-Trange/10)

plt.legend()
plt.show()
