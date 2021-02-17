import tkinter
from tkinter import *

# =============================================================================
# Button Toggle
# =============================================================================
root = tkinter.Tk(className="program")
def toggle():
    if folderMode.config('relief')[-1] == 'sunken':
        folderMode.config(relief="raised")
        folderMode.configure(bg='white')
    else:
        folderMode.config(relief="sunken")
        folderMode.configure(bg='#65fe5c')
        


folderMode = tkinter.Button(text="Tow Folders", width=12, relief="raised", command=toggle)
folderMode.grid()

root.mainloop()


# =============================================================================
#   Hide element
# =============================================================================
def hide_me(event):
    event.widget.grid_forget()

root = Tk()
btn=Button(root, text="Click",command=hide_me)
btn.bind('<Button-1>', hide_me)
btn.grid(row=0, column=0)

btn2=Button(root, text="Click too")
btn2.bind('<Button-1>', hide_me)
btn.grid(row=1, column=1)

root.mainloop()


# =============================================================================
#    Getting Checkbox status
# =============================================================================
from tkinter import ttk
def check():
    state = chk.state()
    print(state[-1])
          
window = tkinter.Tk()
window.geometry("300x300")
chk = ttk.Checkbutton(window, text="foo")
chk.grid(column=0, row=0)

btn = Button(window,text="Check it out", command=check)
btn.grid(row=1, column=1)
window.mainloop()

# =============================================================================
#   Read file lines
# =============================================================================
with open("test", "r") as text_file:
    data = text_file.readlines()  
print(data[1])