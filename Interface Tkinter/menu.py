import cv2
import tkinter as tk
# from win32api import GetSystemMetrics n ta mais usando
from threading import Thread
import numpy as np
from tkinter import *
# from skimage import data creio que n esta usando
from PIL import ImageTk, Image
#from PIL import Image
from tkinter.filedialog import askopenfilenames
# instalar pillow (pill)
# python -m pip install --upgrade Pillow
# https://pillow.readthedocs.io/en/stable/installation.html


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Setup Menu
        MainMenu(self)

        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Processar, ProcessarVideo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Menu", font=("Helvetica", 30))
        label.pack(side=TOP)

        # Label(parent, image=PhotoImage(file="transferir.png")).pack() # tentando colocar uma imagem

        page_one = Button(self, text="Avaliar", relief=RIDGE,
                          command=lambda: controller.show_frame(Processar))
        page_one.pack(padx=100, pady=100, fill=BOTH)


class Processar(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        marcador = Button(self, text="Marcador", relief=RIDGE,
                          command=lambda: controller.show_frame(ProcessarVideo))
        marcador.grid(row=0, column=0, sticky=SW)

        process = Button(self, text="Escolher Imagem", relief=RIDGE, command=self.load_image)
        process.grid(row=0, column=1, sticky=NE)

        voltar = Button(self, text="Voltar", relief=RIDGE,
                        command=lambda: controller.show_frame(StartPage))
        voltar.grid(padx=5, pady=495, sticky=SW)

    def convert_hsv(self, event):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        pixel = hsv[event.y, event.x]

        upper = np.array([pixel[0] + 20, pixel[1] + 10, pixel[2] + 40])
        lower = np.array([pixel[0] - 20, pixel[1] - 10, pixel[2] - 40])

        return self.detectar_circulo(upper, lower, hsv)

    def load_image(self):
        image_formats = [("PNG", "*.png"), ("JPEG", "*.jpg")]
        file_path_list = askopenfilenames(
            filetypes=image_formats, initialdir="C://Users//gustavo//Documents//GitHub//projeto_beta//beta//imagens", title='Selecione a imagem desejada')

        for file_path in file_path_list:
            self.img = cv2.imread(file_path)

        return self.image_main(self.img, img_drawed=0)

    def image_main(self, imagem, img_drawed):
        imageFrame = Frame(self)
        imageFrame.grid(row=0, column=0)

        mostrar = Label(imageFrame)
        mostrar.grid(row=0, column=0)
        mostrar.bind('<Button-1>', self.convert_hsv)

        sliderFrame = Frame(self)
        sliderFrame.grid(row=600, column=0)

        img = Image.fromarray(imagem)
        imgtk = ImageTk.PhotoImage(image=img)
        mostrar.imgtk = imgtk
        mostrar.configure(image=imgtk)

    def hide_me(self, event):
        event.widget.grid_forget()

    def detectar_circulo(self, upper, lower, hsv):
        thresh = cv2.inRange(hsv, lower, upper)
        circulo = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if circulo != None:
            if len(np.shape(circulo)) >= 4:
                print("array dimensional discrepante!")
            else:
                if len(np.shape(circulo)) <= 1:
                    print("Achou o array!")

                    try:
                        circulo1, circulo2 = circulo
                        M = cv2.moments(circulo1)

                        try:
                            cM = int(M["m10"] / M["m00"])
                        except ZeroDivisionError:
                            print("Nao deu certo")
                            cM = -1

                            N = cv2.moments(circulo2)

                        try:
                            cN = int(M["m01"] / M["m00"])
                        except ZeroDivisionError:
                            print("Nao deu certo")
                            cN = -1

                        cv2.drawContours(self.img, [circulo1], -1, (255, 0, 0), 2)
                        cv2.drawContours(self.img, [circulo2], -1, (255, 0, 0), 2)

                    except ValueError:
                        print("Não achou o circulo!")

        self.img_drawed = Image.fromarray(self.img)
        return self.image_main(self.img, self.img_drawed)


class ProcessarVideo(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        #label = Label(self, text="Pagina para poder selecionar o marcador")
        #label.grid(row=1, column=0)

        process = Button(self, text="Selecionar", relief=RIDGE, command=self.load_image)
        process.grid(padx=200, pady=100, sticky=S)

        voltar = Button(self, text="Voltar", relief=RIDGE,
                        command=lambda: controller.show_frame(Processar))
        voltar.grid(padx=100, pady=100, sticky=S)

    def convert_hsv(self, event):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        pixel = hsv[event.y, event.x]

        upper = np.array([pixel[0] + 20, pixel[1] + 10, pixel[2] + 40])
        lower = np.array([pixel[0] - 20, pixel[1] - 10, pixel[2] - 40])

        return self.detectar_marcador(upper, lower, hsv)

    def load_image(self):
        image_formats = [("PNG", "*.png"), ("JPEG", "*.jpg")]
        file_path_list = askopenfilenames(
            filetypes=image_formats, initialdir="C://Users//gustavo//Documents//GitHub//projeto_beta//beta//imagens", title='Selecione a imagem desejada')

        for file_path in file_path_list:
            self.img = cv2.imread(file_path)

        return self.image_main(self.img, img_drawed=0)

    def image_main(self, imagem, img_drawed):
        imageFrame = Frame(self)
        imageFrame.grid(row=0, column=0)

        mostrar = Label(imageFrame)
        mostrar.grid(row=0, column=0)
        mostrar.bind('<Button-1>', self.convert_hsv)

        sliderFrame = Frame(self)
        sliderFrame.grid(row=600, column=0)

        img = Image.fromarray(imagem)
        imgtk = ImageTk.PhotoImage(image=img)
        mostrar.imgtk = imgtk
        mostrar.configure(image=imgtk)

    def hide_me(self, event):
        event.widget.grid_forget()

    def detectar_marcador(self, upper, lower, hsv):
        thresh = cv2.inRange(hsv, lower, upper)
        contorno_marcador = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        centro = None

        if len(contorno_marcador) > 0:
            i = max(contorno_marcador, key=cv2.contourArea)
            ((x, y), radiano) = cv2.minEnclosingCircle(i)
            M = cv2.moments(i)

            try:
                centro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(self.img, (int(x), int(y)), int(radiano), 2)

                if centro != None:
                    Thread(target=self.trackingVideo, args=[lower, upper]).start()

            except ZeroDivisionError:
                pass

        self.img_drawed = Image.fromarray(self.img)
        return self.image_main(self.img, self.img_drawed)

    def trackingVideo(self, lower, upper):
        #nomeVideo = input("\n Digite o nome do video: ")
        #meuVideo = nomeVideo+".mp4"
        camera = cv2.VideoCapture("balanco.mp4")

        while True:
            imageFrame = Frame(self)
            imageFrame.grid(row=0, column=0)

            mostrar = Label(imageFrame)
            mostrar.grid(row=0, column=0)

            sliderFrame = Frame(self)
            sliderFrame.grid(row=600, column=0)

            grabbed, frame = camera.read()

            if grabbed == False:
                break
            else:
                hsv_here = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_here, lower, upper)
                # lower = (35,14,23) upper = (75,34,103)

                contorno_marcador = cv2.findContours(
                    mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                centro = None

                if len(contorno_marcador) > 0:
                    i = max(contorno_marcador, key=cv2.contourArea)
                    ((x, y), radiano) = cv2.minEnclosingCircle(i)
                    M = cv2.moments(i)

                    try:
                        centro = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
                    except ZeroDivisionError:
                        pass

                    cv2.circle(frame, (int(x), int(y)), int(radiano), 2)
                    cv2.putText(frame, "LED", (int(x-radiano), int(y-radiano)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                    # cv2.area que estava antes server para evitar o erro quando finaliza o tracking
                    key = cv2.waitKey(1)
                    #cv2.imshow("Meu video", frame)

                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                mostrar.imgtk = imgtk
                mostrar.configure(image=imgtk)
                #self.after(25, self.trackingVideo(lower, upper))

# declarar esta classe la em cima e passar um parametro para que aponte para class
# esta ficando cada vez mais dificil em trabalahar com resultados de forma atomica
# sempre tenho que estar revendo o codigo e mudando aqueles que tem dependencias


class MainMenu:
    def __init__(self, master):
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)

        w = 700  # width for the Tk root
        h = 550  # height for the Tk root

        x = (master.winfo_screenwidth()/2) - (w/2)
        y = (master.winfo_screenheight()/2) - (h/2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        master.title("GPTER")
        master.wm_iconbitmap("favicon.ico")
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)


app = App()
app.mainloop()
