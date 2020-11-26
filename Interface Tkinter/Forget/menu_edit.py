import cv2
import tkinter as tk
from threading import Thread
import numpy as np
from tkinter import *
from skimage import data
from PIL import ImageTk
from PIL import Image
from tkinter.filedialog import askopenfilenames


class App(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)

		#Setup Menu
		MainMenu(self)

		#Setup Frame
		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		#for F in (StartPage, PageOne, PageTwo):
		for F in (StartPage, PageOne, Processar):
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

		label = Label(self, text="Menu")
		label.pack(side=TOP)

		page_one = Button(self, text="Avaliação", command=lambda:controller.show_frame(PageOne))
		page_one.pack(side=BOTTOM)

		#page_two = Button(self, text="Page Two", command=lambda:controller.show_frame(PageTwo))
		#page_two.pack()

class PageOne(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		label = Label(self, text="Avaliar")
		label.pack(padx=100, pady=100)

		start_page = Button(self, text="Voltar", command=lambda:controller.show_frame(StartPage))
		start_page.pack(side=LEFT)

		start_page = Button(self, text="Calibrar", command=lambda:controller.show_frame(Processar))
		start_page.pack(side=RIGHT)

		#page_two = Button(self, text="Page Two", command=lambda:controller.show_frame(PageTwo))
		#page_two.pack()

#class PageTwo(Frame):
#	def __init__(self, parent, controller):
#		Frame.__init__(self, parent)
#
#		label = Label(self, text="Page Two")
#		label.pack(padx=10, pady=10)
#		start_page = Button(self, text="Start Page", command=lambda:controller.show_frame(StartPage))
#		start_page.pack()
#		page_one = Button(self, text="Page One", command=lambda:controller.show_frame(PageOne))
#		page_one.pack()

class Processar(Frame):
	def __init__(self, parent, controller, imagem, img_drawed):
		Frame.__init__(self, parent)

		process = Button(self, text="Escolher Imagem", command=self.load_image)
		process.grid()

		imageFrame = Frame(self)
		imageFrame.grid(row=0, column=0)

		mostrar = Label(imageFrame)
		mostrar.grid(row=0, column=0)
		mostrar.bind('<Button-1>', self.convert_hsv)

		sliderFrame = Frame(self)
		sliderFrame.grid(row = 600, column=0)

		#video = Button(text="Voltar", command=lambda:controller.show_frame(Processar))
		#video.pack()

		img = Image.fromarray(imagem)
		imgtk = ImageTk.PhotoImage(image=img)
		mostrar.imgtk = imgtk
		mostrar.configure(image=imgtk)

		#self.after(10, hide_me)
		#process.bind('<Button-1>', self.hide_me)

	def convert_hsv(self, event):
		hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
		pixel = hsv[event.y, event.x]

		upper = np.array([pixel[0] + 20, pixel[1] + 10, pixel[2] + 40])
		lower = np.array([pixel[0] - 20, pixel[1] - 10, pixel[2] - 40])

		return self.detectar_circulo(upper, lower, hsv)

	def load_image(self):
		image_formats= [("JPEG", "*.jpg"), ("PNG", "*.png")]
		file_path_list = askopenfilenames(filetypes=image_formats, initialdir="/", title='Selecione a imagem desejada')

		for file_path in file_path_list:
			self.img = cv2.imread(file_path)

		return self.__init__(self.img, img_drawed = 0)

	#def image_main(self, imagem, img_drawed):

		#hei, wid, canais = imagem.shape

		#imageFrame = Frame(self)
		#imageFrame.grid(row=0, column=0)

		#mostrar = Label(imageFrame)
		#mostrar.grid(row=0, column=0)
		#mostrar.bind('<Button-1>', self.convert_hsv)

		#sliderFrame = Frame(self)
		#sliderFrame.grid(row = 600, column=0)

		#video = Button(text="Voltar", command=lambda:controller.show_frame(Processar))
		#video.pack()

		#img = Image.fromarray(imagem)
		#imgtk = ImageTk.PhotoImage(image=img)
		#mostrar.imgtk = imgtk
		#mostrar.configure(image=imgtk)

	def hide_me(self, event):
		event.widget.grid_forget()

	def detectar_circulo(self, upper, lower, hsv):

		thresh = cv2.inRange(hsv, lower, upper)
		circulo = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

		if circulo != None:
			if len(np.shape(circulo)) >= 4:
				print("Não achou nada, ou seja, array dimensional discrepante!")
			else:
				if len(np.shape(circulo)) <= 1:
					print("Achou o tamanho certo do array!")

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

						#return self.processamento_video

					except ValueError:
						print("Não achou o circulo!")


		self.img_drawed = Image.fromarray(self.img)
		return self.__init__(self.img, self.img_drawed)

	#def processamento_video(self):
		#print("botão Selecionado")

class ProcessarVideo(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		label = Label(self, text="Page Two")
		label.pack(padx=10, pady=10)

		start_page = Button(self, text="Start Page", command=lambda:controller.show_frame(StartPage))
		start_page.pack()

		page_one = Button(self, text="Page One", command=lambda:controller.show_frame(PageOne))
		page_one.pack()






#	def load_image(self):
#		image_formats= [("JPEG", "*.jpg"), ("PNG", "*.png")]
#		file_path_list = askopenfilenames(filetypes=image_formats, initialdir="/", title='Selecione a imagem desejada')
#
#		for file_path in file_path_list:
#			self.img = cv2.imread(file_path)
#
#		height, width, canais = self.img.shape
#
#
#Thread(target=self.convert_hsv, args=[self.img]).start() --> n estou usando o thread
#
#
#
#		canvas = tk.Canvas(self, width = width, height = height)
#		canvas.grid()
#
#		self.image = Image.fromarray(self.img)
#		self.foto = ImageTk.PhotoImage(self.image)
#
#		canvas.create_image(0, 0, image=self.foto, anchor=tk.NW)
#		#canvas.bind('<Button-1>', self.hide_me) --> deleta a imagem
#		canvas.bind('<Button-1>', self.convert_hsv)


class MainMenu:
	def __init__(self, master):
		menubar = Menu(master)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Exit", command=master.quit)
		#menubar.add_cascade(label="File", menu=filemenu)
		master.config(menu=menubar)

app = App()
app.mainloop()
