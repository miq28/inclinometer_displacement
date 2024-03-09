from tkinter import *           # Python interface to the Tk GUI toolkit
from tkinter import filedialog  # open file
from tkinter import ttk         # Tk themed widget set

root = Tk()

#menu itmes removed for space

win2 = Toplevel(master=root)    # create a new top level window
frame1 = Frame(win2)
frame2 = Frame(win2)
frame3 = Frame(win2)
scrollbar = Scrollbar(frame1)     # put a scrolbar widget on the right side of the window
scrollbar.pack(side = RIGHT, fill = Y)
sizegrip=ttk.Sizegrip(frame3)     # put a sizegrip widget on the southeast corner of the window
sizegrip.pack(side = RIGHT, anchor = SE)

# put a treeview widget on the window with stylized column headers and use show="headings" to hide the first hierarchy column
column_headers=['PID', 'Name', 'DNA Company Name', 'DNA User Name', 'Admin Name', 'Email']
style = ttk.Style()
style.configure("Treeview.Heading", font=("Verdana", 11))
tv = ttk.Treeview(frame1, height=30, columns=column_headers, show="headings", yscrollcommand = scrollbar.set) 
tv.pack(side=LEFT, fill=BOTH, expand=TRUE)
scrollbar.config(command = tv.yview)

export_button = ttk.Button(frame2, text = "Export", width=15,command=win2.destroy)
export_button.pack(side = LEFT, anchor = E, padx=5, pady=5)

close_button = ttk.Button(frame2, text = "Close", width=15, command=win2.destroy)
close_button.pack(side = RIGHT, anchor = W, padx=5, pady=5)

tv.heading('PID', text='PID')
tv.column('PID', anchor='w', width = 80)

tv.heading('Name', text='Name')
tv.column('Name', anchor='w')

tv.heading('DNA Company Name', text='DNA Company Name')
tv.column('DNA Company Name', anchor='w')

tv.heading('DNA User Name', text='DNA User Name')
tv.column('DNA User Name', anchor='w')

tv.heading('Admin Name', text='Admin Name')
tv.column('Admin Name', anchor='w')

tv.heading('Email', text='Email')
tv.column('Email', anchor='w')

frame1.grid(column=0, row=0, sticky="ns")
frame2.grid(column=0, row=1, sticky="n")
frame3.grid(column=0, row=2, sticky="se")
root.rowconfigure(0, weight=1)

win2.grid_rowconfigure(0, weight=1)
win2.grid_columnconfigure(0, weight=1)

frame1.grid(column=0, row=0, sticky="nsew")

root.mainloop()