from tkinter import filedialog as fd
from tkinter import scrolledtext as st
from tkinter.constants import END
import tkinter as tk
import pandas as pd
import os.path

def file_to_db(a):
    file_name = ""
    file_info = ""
    dict_of_stats = dict.fromkeys(['file', 'file_info','name', 'rotate', 'xy', 'size', 'split', 'pad', 'orig', 'offset', 'index'])
    df = pd.DataFrame()
    for i in a:
        if i == "": # new File
            dict_of_stats['file'] = file_name
            dict_of_stats['file_info'] = file_info
            df = df.append(dict_of_stats,ignore_index=True)
            dict_of_stats.clear()
            file_info = ""
        elif i.startswith('  '): #Pic info
            stat, value = i.split(':')
            dict_of_stats[stat[2:]] = value[1:]
        elif i.endswith('.png'): #File name
            file_name = i
        elif ':' in i: #File info
            file_info += i
        else: #Pic name
            dict_of_stats['file'] = file_name
            dict_of_stats['file_info'] = file_info
            df = df.append(dict_of_stats,ignore_index=True)
            dict_of_stats.clear()
            dict_of_stats['name'] = i

    df = df[df.xy.notna()]

    def create_area(row):
        a = eval(row['xy'])
        b = eval(row['size'])
        return a+(a[0]+b[0],a[1]+b[1])

    df['area'] = df.apply(lambda row: create_area(row), axis=1)    
    
    return df

def insertText():
    file_name = fd.askopenfilename()
    #File opening
    text.insert(END, "Opening file "+file_name[file_name.rfind('/')+1:] + '\n')
    f = open(file_name)
    a = f.read().split('\n')
    #df creating
    text.insert(END, "Creating database"+ '\n')
    df = file_to_db(a)
    #check png files
    text.insert(END, "Check for the existence of PNG files"+ '\n')
    for i in df.file.unique():
        png_name = file_name[:file_name.rfind('/')+1] + i
        if os.path.exists(png_name):
            text.insert(END, 'Find '+i+' file'+ '\n')
        else:
            text.insert(END, 'Can not find '+i+' file'+ '\n','warning')
        
    f.close()

 
root = tk.Tk()
root.geometry("500x500")
text = st.ScrolledText(width=50, height=10)
text.pack()
text.tag_config('warning', background="yellow", foreground="red")
b1 = tk.Button(text="Открыть", command=insertText)
b1.pack()
f1 = tk.Entry(root)
f1.pack()

 
root.mainloop()