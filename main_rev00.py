import tkinter as tk
from tkinter import ttk
import openpyxl
# import inclinometer_plotly_rev04

file_path = "people.xlsx"

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

TZ_ORIGIN='Asia/Makassar'

def my_date_parser_2(dt_naive):
    dt_aware = pd.to_datetime(dt_naive, errors='coerce', utc=False).tz_localize(TZ_ORIGIN)
    return dt_aware

num_of_ipis=15
base_row=4

start_column=34
end_skip_row=4


skip_row = list(range(2, base_row))
skip_rows = list(range(base_row+1, end_skip_row))

skip_rows = skip_row+skip_rows
print(skip_rows)


def load_data():
    #------------
    # A-Axis
    #------------

    used_cols= list(range(start_column, start_column+num_of_ipis))
    used_cols.insert(0,0)


    df_a = pd.read_csv(
        'sample_data.dat',
        skiprows=skip_rows,
        index_col='TIMESTAMP',    
        parse_dates=True,
        header=1,
        # usecols=lambda x: x != 'RECORD',
        usecols=used_cols,
        na_values='NAN',
        # error_bad_lines=False,
        # warn_bad_lines=True,
        on_bad_lines='skip',
        # date_format = my_date_parser_2,
    )
    
    return df_a
    



def insert_row():
    name = name_entry.get()
    age = int(age_spinbox.get())
    subscription_status = status_combobox.get()
    employment_status = "Employed" if a.get() else "Unemployed"

    print(name, age, subscription_status, employment_status)

    # Insert row into Excel sheet
    path = file_path
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    row_values = [name, age, subscription_status, employment_status]
    sheet.append(row_values)
    workbook.save(path)

    # Insert row into treeview
    treeview.insert('', tk.END, values=row_values)
    
    # Clear the values
    name_entry.delete(0, "end")
    name_entry.insert(0, "Name")
    age_spinbox.delete(0, "end")
    age_spinbox.insert(0, "Age")
    status_combobox.set(combo_list[0])
    checkbutton.state(["!selected"])


def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")
        
def quit_me():
    print('quit')
    root.quit()
    root.destroy()

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", quit_me)

style = ttk.Style(root)
# root.tk.call("source", "forest-light.tcl")
# root.tk.call("source", "forest-dark.tcl")
# style.theme_use("forest-dark")

combo_list = ["Subscribed", "Not Subscribed", "Other"]

frame = tk.Frame(root, bg ="red",
                #  uniform=1
                 )

frame.grid_rowconfigure(0, weight=1,uniform=1)
frame.grid_columnconfigure(1, weight=1,uniform=1)
frame.pack(fill='both', expand="yes")

widgets_frame = tk.LabelFrame(frame, text="Insert Row")
widgets_frame.grid(row=0, column=0, padx=20, pady=10)

name_entry = tk.Entry(widgets_frame)
name_entry.insert(0, "Name")
name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")

age_spinbox = tk.Spinbox(widgets_frame, from_=18, to=100)
age_spinbox.insert(0, "Age")
age_spinbox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

status_combobox = ttk.Combobox(widgets_frame, values=combo_list)
status_combobox.current(0)
status_combobox.grid(row=2, column=0, padx=5, pady=5,  sticky="ew")

a = tk.BooleanVar()
checkbutton = tk.Checkbutton(widgets_frame, text="Employed", variable=a)
checkbutton.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

button = tk.Button(widgets_frame, text="Insert", command=insert_row)
button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

separator = ttk.Separator(widgets_frame)
separator.grid(row=5, column=0, padx=(20, 10), pady=10, sticky="ew")

mode_switch = tk.Checkbutton(
    widgets_frame, text="Mode",
    # style="Switch",
    command=toggle_mode)
mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")


df_a = load_data()

cols = tuple(filter(None, df_a.index.names + df_a.columns.values.tolist()))

rows = list(df_a.itertuples(index=True, name=None))
# print(rows)

tabControl = ttk.Notebook(frame) 
tabControl.grid(row=0, column=1, padx=20,pady=20)

tab1 = tk.Frame(tabControl, bg='yellow') 
tab2 = tk.Frame(tabControl) 
  
tabControl.add(tab1, text ='Data') 
tabControl.add(tab2, text ='Cummulative') 
# tabControl.pack(expand = 1, fill ="both") 



treeFrame = tk.Frame(tab1, padx=100,pady=100, bg='blue')
treeFrame.grid(row=1, column=1, pady=50,sticky="nsew")
# frame1.grid(column=0, row=0, sticky="nsew")

treeFrame.grid_rowconfigure(0, weight=1,uniform=1)
treeFrame.grid_columnconfigure(1, weight=1,uniform=1)

treeview = ttk.Treeview(treeFrame, show="headings",
                        # yscrollcommand=treeScrollV.set,
                        # xscrollcommand=treeScrollH.set,
                        columns=cols,
                        # displaycolumns=('TIMESTAMP', 'IPI_1_Def_A(1)', 'IPI_1_Def_A(2)', 'IPI_1_Def_A(3)'),
                        # height=13,
                        # selectmode ='browse'
                        )


treeview.grid_rowconfigure(1, weight=1,uniform=1)
treeview.grid_columnconfigure(1, weight=1,uniform=1)


treeScrollV = tk.Scrollbar(treeFrame,orient=tk.VERTICAL)
treeScrollV.configure(command=treeview.yview)

treeScrollH = tk.Scrollbar(treeFrame, orient=tk.HORIZONTAL)
treeScrollH.configure(command=treeview.xview)

treeview.configure(xscrollcommand=treeScrollH.set, yscrollcommand=treeScrollV.set,)

treeScrollV.pack(side="right", fill="y")
treeScrollH.pack(side="bottom", fill='x')

treeview.pack(fill=tk.BOTH, expand=True)


  




# for col_name in cols:
#     treeview.column(col_name, width=50, stretch=False)
# treeview.update()
# for col_name in cols:
#     treeview.column(col_name, width=125, stretch=False)


# # load_data()
# for col_name in cols:
#     treeview.heading(col_name, text=col_name)
# for value_tuple in rows:
#     treeview.insert('', tk.END, values=value_tuple)
    
    
    
    
df_incremental_a = df_a.sub(df_a.iloc[0,:],axis=1)
df = df_incremental_a.iloc[:, ::-1].cumsum(axis=1).iloc[:, ::-1]


# source: https://stackoverflow.com/a/56873009
df=df.assign(TIMESTAMP=df.index).resample('1D').first().set_index('TIMESTAMP')

print(df)
num_of_lines=5
x1 = np.linspace(0, len(df)-1, num_of_lines+1, dtype='int64',endpoint = True)

df=df.iloc[x1]
df.dropna(inplace=True)


df=df.reset_index()
print(df)
df=pd.melt(
    df,
    id_vars=['TIMESTAMP'], value_vars=list(df.columns),
    # id_vars=list(df.columns), value_vars=['TIMESTAMP'],
    var_name='Depth', value_name='Displacement'
    )
# df = df.set_index(df.columns[0])
df.insert(1, 'Axis', 'A')
df_cum_a=df
print(df_cum_a)


#------------
# B-Axis
#------------

used_cols= list(range(start_column+num_of_ipis, start_column+num_of_ipis+num_of_ipis))
# used_cols= list(range(start_column, start_column+num_of_ipis+num_of_ipis))
used_cols.insert(0,0)

df = pd.read_csv(
    'sample_data.dat',
    skiprows=skip_rows,
    index_col='TIMESTAMP',    
    header=1,
    # usecols=lambda x: x != 'RECORD',
    usecols=used_cols,
    na_values='NAN',
    # error_bad_lines=False,
    # warn_bad_lines=True,
    on_bad_lines='skip',
    # date_format = my_date_parser_2,
    # date_parser=my_date_parser_2,
    # parse_dates=['TIMESTAMP'],
    parse_dates=True,
)

# df.index = pd.to_datetime(df.index, errors='coerce', utc=False).tz_localize(TZ_ORIGIN)

print(df.index)


# df['Datetime'] = pd.to_datetime(df['TIMESTAMP'])
# df = pd.to_datetime(df.index.get_level_values, errors='coerce', utc=False).tz_localize(TZ_ORIGIN)
# df = df.set_index('Datetime')


# df.index = pd.to_datetime(df.index)


# df = df.resample('ME').mean()
# df = df.interpolate(method='time')
# df = df.resample('5D').first()


# INCREMENTAL
df = df.sub(df.iloc[0,:],axis=1)
# CUMMULATIVE
df = df.iloc[:, ::-1].cumsum(axis=1).iloc[:, ::-1]

# source: https://stackoverflow.com/a/56873009
df=df.assign(TIMESTAMP=df.index).resample('1D').first().set_index('TIMESTAMP')

print(df)
num_of_lines=5
x1 = np.linspace(0, len(df)-1, num_of_lines+1, dtype='int64',endpoint = True)

df=df.iloc[x1]
df.dropna(inplace=True)

# print(df)
# 
# df = df.transpose()
# # df = df.T
df=df.reset_index()

# df.index = pd.to_datetime(df['TIMESTAMP'])

# print(df)
df=pd.melt(
    df,
    id_vars=['TIMESTAMP'], value_vars=list(df.columns),
    # id_vars=list(df.columns), value_vars=['TIMESTAMP'],
    var_name='Depth', value_name='Displacement'
    )
# df = df.set_index(df.columns[0])


# COMBINE WITH B-Axis
joined = 1
my_axis = None
if joined:
    my_axis = 'Axis'
    df.insert(1, my_axis, 'B')
    df_cum_b=df
    df=pd.concat([df_cum_a,df_cum_b], ignore_index=True,
)

    
sns.set_theme()

# seaborn.FacetGrid(data, *, row=None, col=None, hue=None, col_wrap=None, sharex=True, sharey=True, height=3, aspect=1, palette=None, row_order=None, col_order=None, hue_order=None, hue_kws=None, dropna=False, legend_out=True, despine=True, margin_titles=False, xlim=None, ylim=None, subplot_kws=None, gridspec_kws=None)

# df = df.sort_values('Axis')
# fig, ax = plt.subplots(figsize=(6, 6))

# https://seaborn.pydata.org/tutorial/color_palettes.html
# https://www.practicalpythonfordatascience.com/ap_seaborn_palette
palette = sns.color_palette("Purples")
df=df.reset_index()
g = sns.relplot(data=df,
            x='Displacement',
            y='Depth',
            # hue=df.index.get_level_values('TIMESTAMP'),
            # hue_norm=mpl.colors.LogNorm(),
            hue='TIMESTAMP',
            palette=palette,
            # palette='hls',
            # col="Axis",
            col=my_axis,
            # sharex=False,
            # sharey=False,            
            kind='line',
            sort=False,
            style="TIMESTAMP",
            markers=True,
            dashes=False,
            errorbar=None,
            # size='index',
            # sizes=(.25, 2.5),
            # height=6,
            # aspect=5/6,
            # legend=True,
            legend=True,
            estimator=None,
            facet_kws={'sharey':False},
            # kwargs={'s':10}
            # ax=ax,
            )


g.set(xlabel ="Displacement (mm)", ylabel = "Depth (m)")
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)



canvas = FigureCanvasTkAgg(g.figure, master=tab2)  # A tk.DrawingArea.
canvas.draw()
# canvas.get_tk_widget().pack()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)





# load_data()
for col_name in cols:
    treeview.heading(col_name, text=col_name)
for value_tuple in rows:
    treeview.insert('', tk.END, values=value_tuple)
    
for col_name in cols:
    treeview.column(col_name, width=50, stretch=False)
treeview.update()
for col_name in cols:
    treeview.column(col_name, width=125, stretch=False)
    

root.mainloop()