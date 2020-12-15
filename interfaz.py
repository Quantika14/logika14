from tkinter import *
import os, time, sys
#from Pillow import Image
#from Pillow import ImageTk
import logika14
import threading

thread = ""

def create_report_f(t):

	t = "report"+t.split(",")[1].replace(" ","_").replace(":","_")+'_logika14.txt'
	f = open (t,'w')
	f.write("\n Hora de creación: "+time.strftime('%A %B, %d %Y %H:%M:%S'))
	f.close()
	return t

def go(listbox, root, e, filename):
	
	t = threading.Thread(target=logika14.main, args=(listbox, root, e, filename,))
	t.daemon = True
	t.start()

def on_closing():
	d = Dialog_exit(root)


def Dialog_exit(parent):
	top = Toplevel(parent)
	parent = parent
	top.title("Salir")

	Label(top, text="¿Está seguro?").grid(row=0, column=0, columnspan=2)

	button1 = Button(top, text="Si, salir de la app", command= lambda: out(top,parent))
	button2 = Button(top, text="No.", command= lambda: icon(top, parent))
	button1.grid(row=1, column=0, padx=5, pady=5)
	button2.grid(row=1, column=1, padx=5, pady=5)

def out(top,parent):
	top.destroy()
	parent.destroy()

def icon(top,parent):
	top.destroy()

if __name__ == '__main__':

	t=time.strftime('%A %B, %d %Y %H:%M:%S')
	filename=create_report_f(t)
	root = Tk()
	root.configure(width=535, height=600)
	root.resizable(width=False, height=False)
	root.title("LogiKa14")
	photo = PhotoImage(file="logika14-2.gif")
	photo_2 = PhotoImage(file="logika14-1.gif")
	label_photo_1 = Label(image=photo)
	label_photo_1.image = photo 
	label_photo_1.place(x=10, y=10)
	label_photo_2 = Label(image=photo_2)
	label_photo_2.image = photo_2
	label_photo_2.place(x=10, y=530)
	myframe=Frame(root)
	scrollbar = Scrollbar(myframe, orient=VERTICAL)
	scrollbar_h = Scrollbar(myframe, orient=HORIZONTAL)

	e = Entry(root, width=50, state=NORMAL)
	e.place(x=10,y=65)
	listbox=Listbox(myframe,yscrollcommand=scrollbar.set,xscrollcommand=scrollbar.set, background="Black", fg="white")

	listbox.configure(width=64, height=25, foreground="white")

	listbox.pack()
	myframe.place(x=10, y=100)
	button = Button(root, text='Buscar', command= lambda: go(listbox, root, e.get(), filename), height=1).place(x=450,y=65)
	info = Label(root, text="Informe:")
	info.place(x=10,y=490)
	rute_la = Label(root, text=filename)
	rute_la.place(x=110,y=490)
	scrollbar.config(command=listbox.yview)
	scrollbar_h.config(command=listbox.xview)
	#scrollbar_h.pack(side=RIGHT, fill=X)
	scrollbar.pack(side=RIGHT, fill=Y)
	root.protocol("WM_DELETE_WINDOW", on_closing)
	root.mainloop()

