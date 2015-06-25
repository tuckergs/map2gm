import tkinter as tk
from tkinter import filedialog, messagebox
import convert, localize
import sys, os

def loc(key):
    return localize.loc(key)

def ask_path(entry, title, filetypes):
    path = filedialog.askopenfilename(filetypes=filetypes,title=title)
    if path != '':
        entry.delete(0, tk.END)
        entry.insert(0, path)
        entry.xview(tk.END)
def check_clicked(rmj_id):
    val = object_widgets[rmj_id][1].get()
    if val == 1:
        object_widgets[rmj_id][0].configure(state='normal')
    else:
        object_widgets[rmj_id][0].configure(state='disabled')
def button_go(convert_command):
    button_convert.config(text=loc('button_convert_working') + '  ')
    root.update()
    rmj = entry_rmj.get()
    roomname = entry_roomname.get()
    template = entry_template.get()
    project = entry_project.get()
    
    objects = {}
    for key, val in object_widgets.items():
        objects[key] = (val[0].get(), val[1].get())
    
    result = convert_command(rmj=rmj,roomname=roomname,template=template,project=project,objects=objects)
    button_convert.config(text=loc('button_convert') + '  ')
    root.update()
    if result != None:
        messagebox.showinfo('', result)

def row_askpath(labeltext, title, filetypes):
    global row
    tk.Label(root,text=labeltext).grid(row=row,column=0,sticky=tk.E)
    entry = tk.Entry(root)
    entry.grid(row=row,column=1,sticky=tk.EW)
    tk.Button(root,text='find...',command=lambda: ask_path(entry, title, filetypes)).grid(row=row,column=2,sticky=tk.EW)
    row += 1
    return entry
def row_entry(labeltext):
    global row
    tk.Label(root,text=labeltext).grid(row=row,column=0,sticky=tk.E)
    entry = tk.Entry(root)
    entry.grid(row=1,column=1,sticky=tk.EW)
    row += 1
    return entry

def ask_overwrite(room_name):
    return messagebox.askyesno(title=loc('warning_title'), message=loc('warning_overwrite_room') % (room_name + '.room.gmx'), type=messagebox.YESNO, icon=messagebox.WARNING)

def load_prefs():
    with open('prefs', 'r') as f:
        for line in f:
            args = line[:-1].split('|')
            args += [''] * (3 - len(args))
            type, value, arg3 = args
            if type == 'template':
                entry_template.insert(0, value)
                entry_template.xview(tk.END)
            elif type == 'project':
                entry_project.insert(0, value)
                entry_project.xview(tk.END)
            else:
                object_widgets[type][0].insert(0, value)
                object_widgets[type][1].set(int(arg3))
                if int(arg3) == 1:
                    object_widgets[type][0].configure(state='normal')
                else:
                    object_widgets[type][0].configure(state='disabled')

def run(convert_command):
    global root, canvas, row, objectrow, objectrowheight, object_widgets, entry_rmj, entry_roomname, entry_template, entry_project, button_convert
    root = tk.Tk()
    root.resizable(True, True)
    root.wm_title(loc('title'))
    icon_image = tk.Image('photo', file='icon.png')
    root.tk.call('wm','iconphoto',root._w,icon_image)

    row = 0
    entry_rmj = row_askpath(loc('label_rmj_map'), loc('open_rmj_map'), [('RMJ map', '.map'),('all files', '.*')])
    entry_roomname = row_entry(loc('label_room_name'))
    entry_template = row_askpath(loc('label_template_room'), loc('open_template_room'), [('GM:S room', '.room.gmx'),('all files', '.*')])
    entry_project = row_askpath(loc('label_project_file'), loc('open_project_file'), [('GM:S project', '.project.gmx'),('all files', '.*')])

    object_images = [('2','images/block.png'),
                     ('12','images/spikeup.png'),
                     ('11','images/spikeright.png'),
                     ('10','images/spikeleft.png'),
                     ('9','images/spikedown.png'),
                     ('19','images/minispikeup.png'),
                     ('18','images/minispikeright.png'),
                     ('17','images/minispikeleft.png'),
                     ('16','images/minispikedown.png'),
                     ('32','images/save.png'),
                     ('31','images/platform.png'),
                     ('23','images/water1.png'),
                     ('30','images/water2.png'),
                     ('20','images/cherry.png'),
                     ('27','images/hurtblock.png'),
                     ('28','images/vineright.png'),
                     ('29','images/vineleft.png'),
                     ]

    objectrowheight = 40
    frameheight = 3 * objectrowheight
    canvasheight = (len(object_images) - 1) * objectrowheight

    frame = tk.Frame(root,height=frameheight,relief=tk.GROOVE,borderwidth=2)
    frame.grid(row=row,column=0,columnspan=3,padx=5,pady=5,sticky=tk.NSEW)
    canvas = tk.Canvas(frame,scrollregion=(0,0,0,canvasheight),yscrollincrement=objectrowheight)
    row += 1
    objectrow = 0

    object_widgets = {}
    for rmj_id, imagepath in object_images:
        photo = tk.PhotoImage(file=imagepath)
        w = tk.Label(root,image=photo)
        w.photo = photo # to prevent it from being garbage collected?
        canvas.create_window((16,0+objectrow*objectrowheight),anchor=tk.CENTER,window=w)
        e = tk.Entry(root)
        canvas.create_window((50,0+objectrow*objectrowheight),anchor=tk.W,window=e)
        v = tk.IntVar()
        c = tk.Checkbutton(root,text=loc('label_object_enabled'),variable=v,command=lambda rmj_id=rmj_id: check_clicked(rmj_id))
        canvas.create_window((200,0+objectrow*objectrowheight),anchor=tk.W,window=c)
        object_widgets[rmj_id] = (e, v)
        objectrow += 1

    vbar=tk.Scrollbar(frame,orient=tk.VERTICAL)
    vbar.pack(side=tk.RIGHT,fill=tk.Y)
    vbar.config(command=canvas.yview)
    canvas.config(height=frameheight)
    canvas.config(yscrollcommand=vbar.set)
    canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH,pady=20)

    button_convert = tk.Button(root,text=loc('button_convert') + '  ',command=lambda: button_go(convert_command),image=icon_image,compound=tk.RIGHT)
    button_convert.grid(row=row,column=1,columnspan=2,sticky=tk.NSEW)

    root.grid_columnconfigure(0, weight=1, minsize=120)
    root.grid_columnconfigure(1, weight=8, minsize=150)
    root.grid_columnconfigure(2, weight=1, minsize=50)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.minsize(320, 350)
    root.geometry('320x350')

    if os.path.exists('prefs'):
        load_prefs()
    else:
        for id, widgets in object_widgets.items():
            widgets[1].set(0)
            check_clicked(id)

    root.mainloop()
