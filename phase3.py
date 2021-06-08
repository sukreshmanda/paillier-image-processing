import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
import os
from PIL import Image
from PIL import ImageTk
from PIL import ImageEnhance
from tkinter import filedialog
import numpy as np
from paillier import *
import sys
pos=0;
class phase3:
    def __init__(self):
        self.pail=paillier()
        self.priv, self.pub=self.pail.generate_keypair(20)
        self.c_image=None
        self.d_image=None
        self.outputImage=None
        self.inputImage=None

        self.is_encrypted=False

def displayImage(imagetodisplay,f):
    if(f==1):
        imagetodisplay=ImageTk.PhotoImage(imagetodisplay)
        showWindow.config(image=imagetodisplay)
        showWindow.photo_ref=imagetodisplay
        showWindow.pack(side=tk.LEFT,anchor=tk.N)
    else:
        image=imagetodisplay.astype(np.uint8)
        im=Image.fromarray(image)
        imagetodisplay=ImageTk.PhotoImage(im)
        showWindow1.config(image=imagetodisplay)
        showWindow1.photo_ref=imagetodisplay
        showWindow1.pack(side=tk.LEFT,anchor=tk.N)
def importImage(sip):
    filename=filedialog.askopenfilename(initialdir=os.getcwd(),title="Select Image File",filetypes=(("PNG FIle","*.png"),("JPG File","*.jpg"),("All Files","*.*")))
    sip.inputImage=Image.open(filename)
    sip.inputImage.thumbnail((588,375))
    sip.is_encrypted=False
    displayImage(sip.inputImage,1)
def encryptImage(sip):    
    image=np.array(sip.inputImage)
    sip.c_image=sip.pail.encrypt_image(sip.pub,image)
    sip.is_encrypted=True
    sip.outputImage=sip.c_image

    displayImage(sip.c_image,2)
def decryptImage(sip):
    if(sip.is_encrypted==False):
        return
    sip.d_image=sip.pail.decrypt_image(sip.priv,sip.pub,sip.c_image)
    sip.is_encrypted=False
    sip.outputImage=sip.d_image

    displayImage(sip.d_image,2)

def brightness(sip,k):
    
    def bright(posi):
        global pos
        pos=posi
        print(pos)
    #def preview():

    def apply():
        sip.c_image=sip.pail.brightness(sip.pub,sip.c_image,pos)
        sip.outputImage=sip.c_image
        
        k(sip.c_image,2)
        new.destroy()
    #if sip.is_encrypted==False:
       # encryptImage(sip)
    new=tk.Toplevel(window)
    #new.bind("<Destroy>",apply)
    new.geometry("250x180")
    new.title("Adjust")
    #new.resizeable(False,False)
    lbl=tk.Label(new,text="Brightness").pack(anchor=tk.CENTER)
    
    bslider=tk.Scale(new,from_=0,to=255,orient=tk.HORIZONTAL,length=250,command=bright)
    bslider.set(256/2)
    bslider.pack(anchor=tk.CENTER)
    
    fram=tk.Frame(new,height=20,width=200)
    fram.pack(side=tk.BOTTOM,pady=5)

    sep1=ttk.Separator(new,orient="horizontal")
    sep1.pack(fill=tk.X,padx=2,pady=2,side=tk.BOTTOM)
    
    cancel=tk.Button(fram,text="Cancel",command=lambda:new.destroy())
    cancel.pack(side=tk.RIGHT,padx=5)
    
    #preview=tk.Button(fram,text="Preview",command=preview)
    #preview.pack(side=tk.RIGHT,padx=5)

    apply=tk.Button(fram,text="Apply",command=apply)
    apply.pack(side=tk.LEFT,padx=8)

def increasecolor(sip,k):
    r=tk.StringVar()
    r.set("red")
    def value(posi):
        global pos
        pos=posi
        print(pos)
    def clicked(val):
        pass
    def apply():
        sip.c_image=sip.pail.increase_color(sip.pub,sip.c_image,r.get(),pos)
        sip.outputImage=sip.c_image
        
        k(sip.c_image,2)
        new.destroy()
    new =tk.Toplevel(window)
    new.geometry("250x250")
    new.title("Color Enchancement")

    tk.Radiobutton(new,text="Red",variable=r, value ="red",command=lambda:clicked(r.get())).pack(anchor=tk.W,padx=10)
    tk.Radiobutton(new,text="Green",variable=r, value ="green",command=lambda:clicked(r.get())).pack(anchor=tk.W,padx=10)
    tk.Radiobutton(new,text="Blue",variable=r, value ="blue",command=lambda:clicked(r.get())).pack(anchor=tk.W,padx=10)
    tk.Radiobutton(new,text="Luminance",variable=r, value ="luminance",command=lambda:clicked(r.get())).pack(anchor=tk.W,padx=10)

    lbl=tk.Label(new,text="Value").pack(anchor=tk.CENTER)
    
    bslider=tk.Scale(new,from_=0,to=255,orient=tk.HORIZONTAL,length=250,command=value)
    bslider.set(256/2)
    bslider.pack(anchor=tk.CENTER)

    fram=tk.Frame(new,height=20,width=200)
    fram.pack(side=tk.BOTTOM,pady=5)

    sep1=ttk.Separator(new,orient="horizontal")
    sep1.pack(fill=tk.X,padx=2,pady=2,side=tk.BOTTOM)

    cancel=tk.Button(fram,text="Cancel",command=lambda:new.destroy())
    cancel.pack(side=tk.RIGHT,padx=5)

    apply=tk.Button(fram,text="Apply",command=apply)
    apply.pack(side=tk.LEFT,padx=8)

def swapcolor(sip,k):
    r1=tk.StringVar()
    r1.set("red")
    
    
    r2=tk.StringVar()
    r2.set("green")

    def clicked():
        pass
    def apply():
        sip.c_image=sip.pail.swap_colors(sip.pub,sip.c_image,r1.get(),r2.get())
        sip.outputImage=sip.c_image
        
        k(sip.c_image,2)
        new.destroy()
    new =tk.Toplevel(window)
    new.geometry("250x270")
    new.title("Swap Colors")

    #frame4=tk.Frame(new,height=140,width=250).pack(side=tk.TOP)
    
    tk.Radiobutton(new,text="Red",variable=r1, value ="red",command=clicked).pack(anchor=tk.W,padx=10)
    tk.Radiobutton(new,text="Green",variable=r1, value ="green",command=clicked).pack(anchor=tk.W,padx=10)
    tk.Radiobutton(new,text="Blue",variable=r1, value ="blue",command=clicked).pack(anchor=tk.W,padx=10)
    tk.Radiobutton(new,text="Luminance",variable=r1, value ="luminance",command=clicked).pack(anchor=tk.W,padx=10)

    sep2=ttk.Separator(new,orient="horizontal")
    sep2.pack(fill=tk.X,padx=2,pady=2)
    
    tk.Radiobutton(new,text="Red",variable=r2, value ="red",command=clicked).pack(anchor=tk.W,padx=10)
    tk.Radiobutton(new,text="Green",variable=r2, value ="green",command=clicked).pack(anchor=tk.W,padx=10)
    tk.Radiobutton(new,text="Blue",variable=r2, value ="blue",command=clicked).pack(anchor=tk.W,padx=10)
    tk.Radiobutton(new,text="Luminance",variable=r2, value ="luminance",command=clicked).pack(anchor=tk.W,padx=10)

    
    fram=tk.Frame(new,height=20,width=200)
    fram.pack(side=tk.BOTTOM,pady=5)

    sep1=ttk.Separator(new,orient="horizontal")
    sep1.pack(fill=tk.X,padx=2,pady=2,side=tk.BOTTOM)

    cancel=tk.Button(fram,text="Cancel",command=lambda:new.destroy())
    cancel.pack(side=tk.RIGHT,padx=5)

    apply=tk.Button(fram,text="Apply",command=apply)
    apply.pack(side=tk.LEFT,padx=8)
    
def multiplybyc(sip,k):
    
    def bright(posi):
        global pos
        pos=posi
        print(pos)
    def apply():
        sip.c_image=sip.pail.multiply_by_const(sip.pub,sip.c_image,int(pos) )
        sip.outputImage=sip.c_image

        k(sip.c_image,2)
        new.destroy()
    new=tk.Toplevel(window)
    #new.bind("<Destroy>",apply)
    new.geometry("250x150")
    new.title("Multiply")
    #new.resizeable(False,False)
    lbl=tk.Label(new,text="Select Constant").pack(anchor=tk.CENTER)
    
    bslider=tk.Scale(new,from_=0,to=20,orient=tk.HORIZONTAL,length=250,command=bright)
    bslider.set(1)
    bslider.pack(anchor=tk.CENTER)
    
    fram=tk.Frame(new,height=20,width=200)
    fram.pack(side=tk.BOTTOM,pady=5)

    sep1=ttk.Separator(new,orient="horizontal")
    sep1.pack(fill=tk.X,padx=2,pady=2,side=tk.BOTTOM)
    
    cancel=tk.Button(fram,text="Cancel",command=lambda:new.destroy())
    cancel.pack(side=tk.RIGHT,padx=5)

    apply=tk.Button(fram,text="Apply",command=apply)
    apply.pack(side=tk.LEFT,padx=8)
    
def flipImage(sip):
    if sip.is_encrypted==False:
        encryptImage(sip)
    sip.c_image=sip.pail.flip_image(sip.pub,sip.c_image)
    sip.outputImage=sip.c_image

    displayImage(sip.c_image,2)

    
def mirrorImage(sip):
    if sip.is_encrypted==False:
        encryptImage(sip)
    sip.c_image=sip.pail.mirroring_image(sip.pub,sip.c_image)
    sip.outputImage=sip.c_image

    displayImage(sip.c_image,2)

def saveImage(sip):
    #ext = tk.StringVar()
    #name = filedialog.asksaveasfilename(title="Select file", typevariable=ext, filetypes=(('PNG', '*.png'),('JPEG', ('*.jpg', '*.jpeg', '*.jpe')),  ('BMP', ('*.bmp', '*.jdib')), ('GIF', '*.gif')))
    #print(os.path.basename(name))
    #if name:
    sip.pail.save_image(sip.outputImage)
def closeButton():
    window.destroy()
sip=phase3()
k=displayImage
window = tk.Tk()
window.option_add('*Font','Helvetica')
window.title("Secure Image Processing Tool")
swidth=window.winfo_screenwidth()
sheight=window.winfo_screenheight()
        
window.geometry(f'{swidth}x{sheight}')

frame1 = tk.Frame(window,height=20,width=swidth)
frame1.pack(anchor=tk.N,pady=10)

frame2=tk.Frame(window,height=20,width=swidth)
frame2.pack(anchor=tk.NW)

sep=ttk.Separator(window,orient="horizontal")
sep.pack(fill=tk.X,padx=5,pady=20)

importbutton =tk.Button(frame1,text="Import",padx=5,pady=5,command=lambda:importImage(sip))
importbutton.grid(row=0,column=0)

encryptbutton =tk.Button(frame1,text="Encrypt",padx=5,pady=5,command=lambda:encryptImage(sip))
encryptbutton.grid(row=0,column=1)

decryptbutton =tk.Button(frame1,text="Decrypt",padx=5,pady=5,command=lambda:decryptImage(sip))
decryptbutton.grid(row=0,column=2)

brightbutton =tk.Button(frame1,text="Brightness",padx=5,pady=5,command=lambda:brightness(sip,k))
brightbutton.grid(row=0,column=3)

colorbutton =tk.Button(frame1,text="Color Enhancement",padx=5,pady=5,command=lambda:increasecolor(sip,k))
colorbutton.grid(row=0,column=4)

swapbutton =tk.Button(frame1,text="Swap Colors",padx=5,pady=5,command=lambda:swapcolor(sip,k))
swapbutton.grid(row=0,column=5)

multiplybutton =tk.Button(frame1,text="Multiply",padx=5,pady=5,command=lambda:multiplybyc(sip,k))
multiplybutton.grid(row=0,column=6)

mirrorbutton =tk.Button(frame1,text="Mirror",padx=5,pady=5,command=lambda:mirrorImage(sip))
mirrorbutton.grid(row=0,column=7)

flipbutton =tk.Button(frame1,text="Flip",padx=5,pady=5,command=lambda:flipImage(sip))
flipbutton.grid(row=0,column=8)
    
savebutton=tk.Button(frame1,text="Save",padx=5,pady=5,command=lambda:saveImage(sip))
savebutton.grid(row=0,column=9)

closebutton= tk.Button(frame1,text="Close",padx=5,pady=5,command=closeButton)
closebutton.grid(row=0,column=10)
'''
bslider=tk.Scale(frame2,label="Brightness",from_=0,to=100,orient=tk.HORIZONTAL,length=swidth,command=brightness)
bslider.set(50)
bslider.pack(anchor=tk.N)'''

showWindow=tk.Label(window,height=int(sheight/2),width=int(swidth/2))
showWindow1=tk.Label(window,height=int(sheight/2),width=int(swidth/2))
tk.mainloop()
        
       
        
