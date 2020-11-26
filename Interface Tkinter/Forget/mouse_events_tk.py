from tkinter import *
import tkinter
import colorsys # serve para mudar os valores das variaveis independentementes
import cv2
import PIL.Image, PIL.ImageTk


def pixel_local(event):
    print("x: ",event.x, "y:", event.y)

def pixel_color_local(event):
    color = img[event.y, event.x]
    b, g, r = color

    print("R: ",r,"G: ",g,"B: ",b)

def hide_me(event):
    event.widget.pack_forget()

def convert_hsv(event):
    color = img[event.y, event.x]

    b, g, r = color
    cores_rgb = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    hue,saturation,value = cores_rgb

    # arredonda uma casa com "1" depois da multiplicação

    h = round(hue*360,1) ###### caderno parece que o calculo que o opencv faz é a multiplicação por 120 ou 180
    s = round(saturation*100,1)
    v = round(value*100,1)

    print("H: ",h,"S: ",s,"V: ",v)

root = tkinter.Tk()

img = cv2.imread("ca.png")

height, width, canais = img.shape

canvas = tkinter.Canvas(root, width = width, height = height)
canvas.pack()

opt = eval(input(" 1 - RGB \n 2 - HSV \n\n Opção:"))

if opt == 1:
    canvas.bind('<Button-1>', pixel_color_local, "\n")
else:
    if opt == 2:
        canvas.bind('<Button-1>', convert_hsv, "\n")

photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img))

minha_imagem = canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)




button = Button(root, text="coordenadas")
button.pack()
button.bind('<Button-1>', hide_me)


root.mainloop()
