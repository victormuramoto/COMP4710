import numpy as np
import pylab
import matplotlib.cm as cm
from Tkinter import *
import Image, ImageTk
import urllib
'''
f = pylab.figure()
for n, fname in enumerate(('1.png', '2.png','3.png')):
    image=Image.open(fname)
    arr=np.asarray(image)
    #f.add_subplot(2, 1, n)  # this line outputs images on top of each other
    f.add_subplot(1, 1, n)  # this line outputs images side-by-side    
    pylab.imshow(arr,cmap=cm.Greys_r)
    pylab.xticks([]), pylab.yticks([])    
    
#pylab.text(0.5, 0,5, "teste", fontsize = 12)
pylab.show()
'''

root = Toplevel()
url = urllib.urlretrieve('https://s3-us-west-2.amazonaws.com/hearthstats/cards/leeroy-jenkins.png',"leeroy_jenkins.png")
logo = ImageTk.PhotoImage(Image.open('leeroy_jenkins.png'))
w1 = Label(root, image=logo).pack(side="left")
explanation = """At present, only GIF and PPM/PGM
formats are supported, but an interface 
exists to allow additional image file
formats to be added easily."""
w2 = Label(root, 
           justify=LEFT,
           padx = 10, 
           text=explanation).pack(side="right")
root.mainloop()