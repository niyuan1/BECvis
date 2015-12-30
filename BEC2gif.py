# program animates BEC evolution model as gif
# visualizes time, radius, luminosity, and temperature
# program depends on modules:
#   PIL
#   Pillow (for ImageOps module)
#   Figtodat
#   images2gif

from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw
import matplotlib.pyplot as plt
import ImageOps
import numpy as np
import Figtodat
from images2gif import writeGif

#parameters
m = 10      #mass of star (MS)
O = 100     #number of output images
N = 59      #number of base gif images
step = 0.1  #animation time step (s)
pause = 1.0 #animation ending pause (s)

#import evolution data
t, Tc, Yc, Lh, Lhe, M, sev, Teff, logL, logpc, Lc, Lv, Mw, Tmax, pTmax, MrTmax = np.loadtxt(str(m)+'.plot1', dtype='string', unpack=True)    

#format data
Teff = np.array([float(T.split('D')[0])*10**int(T.split('D')[1]) for T in Teff])
logL = np.array([float(B.split('D')[0])*10**int(B.split('D')[1]) for B in logL])
t = np.array([float(H.split('D')[0])*10**int(H.split('D')[1]) for H in t])

#import black body colors
black_file = open('black.txt', 'r')
lines = black_file.read().split('\n')
Tb = np.array([float(line.split(' ')[0]) for line in lines])
cb = [line.split(' ')[1] for line in lines]

#get relevant arrays
t = t               #time
L = np.exp(logL)    #luminosity

#calculate radius information
Tsun = 5777.0
Tr = Teff/Tsun
R = np.sqrt(L/np.power(Tr,4))
R = R/max(R)

#map temperature to hex rgb color
cols = []
for T in Teff:
    color = cb[np.argmin(np.square(Tb-T))]
    cols.append(color)
cols = np.array(cols)

#open base star images
im = []
for i in range(N):
    image = Image.open("star/star-"+str(i)+".png")
    print "Image "+str(i)+":\t"+image.format+', '+str(image.size)+', '+image.mode
    im.append(image)

#generate list of evolution images
out = []
t0 = 0.0
fig = plt.figure(facecolor='black')
plt.rcParams.update({'font.size': 14})
sub = fig.add_subplot(111)
sub.hold(False)
for i in range(O):
    #current time
    print "time: " + ('%.2f' % t[int(i*len(t)/O)])
    dt = t[int(i*len(t)/O)] - t0
    t0 = t[int(i*len(t)/O)]
    #current star color
    color = cols[int(i*len(t)/O)]
    #take next gif image
    image = im[i % N]
    #get image size
    isize = image.size
    bsize = tuple((isize[0]*2,isize[1]))
    size = tuple([int(z * R[int(i*len(t)/O)]) for z in isize])
    
    #apply color transform to image
    image.load()
    r, g, b, alpha = image.split()
    gray = ImageOps.grayscale(image)
    img = ImageOps.colorize(gray, (0,0,0,0), color)
    img.putalpha(alpha)

    #resize transform to image
    img = img.resize(size)

    #apply filter to image
    #omage = omage.filter(ImageFilter.SMOOTH_MORE)

    #generate HR plot
    sub.plot(np.log10(Teff)[:int(i*len(t)/O)+1], logL[:int(i*len(t)/O)+1], 'b.', ms=4)
    sub.title.set_color('white')
    sub.yaxis.label.set_color('white')
    sub.xaxis.label.set_color('white')
    sub.tick_params(axis='x', colors='white')
    sub.tick_params(axis='y', colors='white')
    sub.tick_params(axis='both', direction='out')
    sub.get_xaxis().tick_bottom()
    sub.get_yaxis().tick_left()
    sub.set_title('HR Trajectory for '+str(m)+'M star')
    sub.set_ylabel('Luminosity (log LS)')
    sub.set_xlabel('Temperature (log K)')
    sub.set_ylim(min(logL)-0.05, max(logL)+0.05)
    sub.set_xlim(max(np.log10(Teff))+0.2, min(np.log10(Teff))-0.2)
    x0,x1 = sub.get_xlim()
    y0,y1 = sub.get_ylim()

    HR = Figtodat.fig2img(fig).resize(tuple(isize))
    HR = HR.filter(ImageFilter.EDGE_ENHANCE)

    #make blank image
    omage = Image.new("RGB", bsize)
    #inscribe text
    draw = ImageDraw.Draw(omage)
    draw.text((10,10),'BEC sim',(255,255,255))
    draw.text((10,30),'STAR '+str(m)+'M',(255,255,255))
    w, h = draw.textsize(('%.2f' % t[int(i*len(t)/O)])+'y')
    draw.text((isize[0]-w-10,10),('%.2f' % t[int(i*len(t)/O)])+'y',(255,255,255))
    w, h = draw.textsize('d'+('%.2f' % dt)+'y')
    draw.text((isize[0]-w-10,30),'d'+('%.2f' % dt)+'y',(255,255,255))
    draw = ImageDraw.Draw(omage)
    draw = ImageDraw.Draw(omage)
    #paste star image
    locate = ((isize[0]-size[0])/2, (isize[1]-size[1])/2+40)
    omage.paste(img, locate, img)
    #paste HR diagram
    omage.paste(HR, (isize[0],0))

    #append to out list
    out.append(omage.convert("P"))  

for i in range(int(pause/step)):
    out.append(omage.convert("P"))
    print "Pause "+str(pause)+"s"

#save output image list
#print str(len(out)) + " images"
#for i in range(O):
#    print "Saving out-"+str(i)+".png"
#    out[i].save('out-'+str(i)+".png")

#output as gif
print "Writing GIF"
#im = []
#for i in range(O):
#    image = Image.open("out-"+str(i)+".png")
#    print "Image "+str(i)+":\t"+image.format+', '+str(image.size)+', '+image.mode
#    im.append(image.convert("P"))
writeGif(str(m)+'.gif', out, duration=step, dither=0)
