# Program plots HR diagram from plot1 file

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

#dt parameter
t = 41

#read pixel to wavelength data
t25, Tc25, Yc25, Lh25, Lhe25, M25, sev25, Teff25, L25, logpc25, Lc25, Lv25, Mw25, Tmax25, pTmax25, MrTmax25 = np.loadtxt('25.plot1', dtype='string', unpack=True)
t15, Tc15, Yc15, Lh15, Lhe15, M15, sev15, Teff15, L15, logpc15, Lc15, Lv15, Mw15, Tmax15, pTmax15, MrTmax15 = np.loadtxt('15.plot1', dtype='string', unpack=True)
t10, Tc10, Yc10, Lh10, Lhe10, M10, sev10, Teff10, L10, logpc10, Lc10, Lv10, Mw10, Tmax10, pTmax10, MrTmax10 = np.loadtxt(str(t)+'t.plot1', dtype='string', unpack=True)

#format data
Teff25 = np.array([float(T.split('D')[0])*10**int(T.split('D')[1]) for T in Teff25])
L25 = np.array([float(B.split('D')[0])*10**int(B.split('D')[1]) for B in L25])
Yc25 = np.array([float(H.split('D')[0])*10**int(H.split('D')[1]) for H in Yc25[Yc25!='4.000000000-100']])

Teff15 = np.array([float(T.split('D')[0])*10**int(T.split('D')[1]) for T in Teff15])
L15 = np.array([float(B.split('D')[0])*10**int(B.split('D')[1]) for B in L15])
Yc15 = np.array([float(H.split('D')[0])*10**int(H.split('D')[1]) for H in Yc15[Yc15!='4.000000000-100']])

Teff10 = np.array([float(T.split('D')[0])*10**int(T.split('D')[1]) for T in Teff10])
L10 = np.array([float(B.split('D')[0])*10**int(B.split('D')[1]) for B in L10])
Yc10 = np.array([float(H.split('D')[0])*10**int(H.split('D')[1]) for H in Yc10[Yc10!='4.000000000-100']])

#convert to log
Teff25 = np.log10(Teff25)
Teff15 = np.log10(Teff15)
Teff10 = np.log10(Teff10)

Teff = np.concatenate((Teff10, Teff15, Teff25), axis=0)
L = np.concatenate((L10, L15, L25), axis=0)

#find critical points
HE25 = np.argmax(Yc25)
HE15 = np.argmax(Yc15)
HE10 = np.argmax(Yc10)

HeE25 = np.argmin(Yc25)
HeE15 = np.argmin(Yc15)
HeE10 = np.argmin(Yc10)

#plot data
plt.title("HR Trajectory for 25M,15M,10M star")
plt.plot(Teff25, L25, 'b.', label='25M')
plt.plot(Teff15, L15, 'g.', label='15M')
plt.plot(Teff10, L10, 'r.', label='10M')
ax = plt.gca()
ax.set_ylabel('Luminosity (log Solar Units)')
ax.set_xlabel('Temperature (log K)')
plt.axis([max(Teff)+0.2, min(Teff)-0.2, min(L)-0.05, max(L)+0.05])
plt.text(Teff25[HE25], L25[HE25], "End of H", color='b')
plt.text(Teff15[HE15], L15[HE15], "End of H", color='g')
plt.text(Teff10[HE10], L10[HE10], "End of H", color='r')
plt.text(Teff25[HeE25], L25[HeE25], "End of He", color='b')
plt.text(Teff15[HeE15], L15[HeE15], "End of He", color='g')
plt.text(Teff10[HeE10], L10[HeE10], "End of He", color='r')
plt.text(Teff25[-1], L25[-1], "End", color='b')
plt.text(Teff15[-1], L15[-1], "End", color='g')
plt.text(Teff10[-1], L10[-1], "End", color='r')
plt.legend(bbox_to_anchor=(0.2, 0.2))
plt.show()
