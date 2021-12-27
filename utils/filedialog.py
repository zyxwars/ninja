import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


def askopenfilename(*args, **kwargs):
    return filedialog.askopenfilename(*args, **kwargs)


def askdirectory(*args, **kwargs):
    return filedialog.askdirectory(*args, **kwargs)


def asksaveasfilename(*args, **kwargs):
    return filedialog.asksaveasfilename(*args, **kwargs)
