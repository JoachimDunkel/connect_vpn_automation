# Import the necessary library
import itertools
from tkinter import *
from tkinter import ttk

# Create an instance of tkinter window
win = Tk()
# Set the geometry of tkinter window
win.geometry("750x250")
# Define the style
style_1 = {'fg': 'black', 'bg': 'red', 'activebackground':
    'gray71', 'activeforeground': 'gray71'}
style_2 = {'fg': 'white', 'bg': 'OliveDrab2', 'activebackground':
    'gray71', 'activeforeground': 'gray71'}
style_3 = {'fg': 'black', 'bg': 'purple1', 'activebackground':
    'gray71', 'activeforeground': 'gray71'}
style_4 = {'fg': 'white', 'bg': 'coral2', 'activebackground':
    'gray71', 'activeforeground': 'gray71'}
style_cycle = itertools.cycle([style_1, style_2, style_3, style_4])


# Define a function to update the button style
def update_style():
    style = next(style_cycle)
    button.configure(**style)


button = Button(win, width=40, font=('Helvetica 18 bold'), text="ChangeStyle", command=update_style)
button.pack(padx=50, pady=50)
update_style()
win.mainloop()
