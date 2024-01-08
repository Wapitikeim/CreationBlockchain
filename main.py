from tkinter import *
from tkinter import ttk

from pdc import startBlenderAndStartTakingScreenshots

root = Tk()
frm = ttk.Frame(root, padding=20)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Screenshot", command=startBlenderAndStartTakingScreenshots).grid(column=1, row=0)
root.mainloop()