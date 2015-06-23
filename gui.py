import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import convert
import sys
import os
import localize

def loc(key):
    return localize.loc(key)

def ask_path(entry, title, filetypes):
    path = filedialog.askopenfilename(filetypes=filetypes,title=title)
    if path != '':
        entry.delete(0, tk.END)
        entry.insert(0, path)
        entry.xview(tk.END)
        
def button_go():
    rmj = entry_rmj.get()
    roomname = entry_roomname.get()
    template = entry_template.get()
    project = entry_project.get()
    if rmj == '' or roomname == '' or template == '' or project == '':
        messagebox.showinfo('', loc('error_top_field_empty'))
        return
    rmj_to_gm = {}
    for key, val in object_entries.items():
        text = val[0].get()
        enabled = val[1].get()
        if enabled:
            if text == '':
                messagebox.showinfo('', loc('error_object_no_name'))
                return
            else:
                rmj_to_gm[key] = text
                fn = os.path.join(os.path.split(project)[0], 'objects', text + '.object.gmx')
                if not os.path.exists(fn):
                    messagebox.showinfo('', loc('error_nonexistent_object') % text)
                    return

    fn = os.path.join(os.path.split(project)[0], 'rooms', roomname + '.room.gmx')
    if os.path.exists(fn):
        messagebox.showinfo('', loc('error_room_name_collision'))
        return
    try:
        entities = convert.get_entities_from_rmj(rmj, rmj_to_gm)
        convert.write_room(entities, roomname, project, template)
        convert.add_room_to_project(roomname, project)
        with open('prefs', 'w') as f:
            f.write('template|%s\n' % template)
            f.write('project|%s\n' % project)
            for key, value in sorted(object_entries.items()):
                f.write('%s|%s|%s\n' % (key, value[0].get(), value[1].get()))
        messagebox.showinfo('', 'Successfully converted! Prefs saved.')
    except:
        info = sys.exc_info()
        with open('errorlog.txt', 'w') as f:
            f.write('Last error:\n\n%s\n%s\n%s' % info)
        #todo: print stack trace
        messagebox.showinfo('', loc('error_exception'))
    
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
def check_clicked(rmj_id):
    val = object_entries[rmj_id][1].get()
    if val == 1:
        object_entries[rmj_id][0].configure(state='normal')
    else:
        object_entries[rmj_id][0].configure(state='disabled')
def row_object(rmj_id, image_filename):
    global objectrow
    photo = tk.PhotoImage(file=image_filename)
    w = tk.Label(root,image=photo)
    w.photo = photo # to prevent it from being garbage collected?
    canvas.create_window((16,0+objectrow*objectrowheight),anchor=tk.CENTER,window=w)
    e = tk.Entry(root)
    canvas.create_window((50,0+objectrow*objectrowheight),anchor=tk.W,window=e)
    v = tk.IntVar()
    c = tk.Checkbutton(root,text=loc('label_object_enabled'),variable=v,command=lambda: check_clicked(rmj_id))
    v.set(1)
    canvas.create_window((200,0+objectrow*objectrowheight),anchor=tk.W,window=c)
    object_entries[rmj_id] = (e, v)
    objectrow += 1


object_images = [('2','images/block.gif'),
                 ('12','images/spikeup.gif'),
                 ('11','images/spikeright.gif'),
                 ('10','images/spikeleft.gif'),
                 ('9','images/spikedown.gif'),
                 ('19','images/minispikeup.gif'),
                 ('18','images/minispikeright.gif'),
                 ('17','images/minispikeleft.gif'),
                 ('16','images/minispikedown.gif'),
                 ('32','images/save.gif'),
                 ('31','images/platform.gif'),
                 ('23','images/water1.gif'),
                 ('30','images/water2.gif'),
                 ('20','images/cherry.gif'),
                 ('27','images/hurtblock.gif'),
                 ('28','images/vineright.gif'),
                 ('29','images/vineleft.gif'),
                 ]

objectrowheight = 40
frameheight = 3 * objectrowheight
canvasheight = (len(object_images) - 1) * objectrowheight

row = 0
root = tk.Tk()
root.wm_title(loc('title'))

object_entries = {}

entry_rmj = row_askpath(loc('label_rmj_map'), loc('open_rmj_map'), [('RMJ map', '.map'),('all files', '.*')])
entry_roomname = row_entry(loc('label_room_name'))
entry_template = row_askpath(loc('label_template_room'), loc('open_template_room'), [('GM:S room', '.room.gmx'),('all files', '.*')])
entry_project = row_askpath(loc('label_project_file'), loc('open_project_file'), [('GM:S project', '.project.gmx'),('all files', '.*')])

frame = tk.Frame(root,height=frameheight,relief=tk.GROOVE,borderwidth=2)
frame.grid(row=row,column=0,columnspan=3,padx=5,pady=5)
canvas = tk.Canvas(frame,width='8c',height=600,scrollregion=(0,0,0,canvasheight),yscrollincrement=objectrowheight)
row += 1
objectrow = 0

for rmj_id, imagepath in object_images:
    row_object(rmj_id, imagepath)

vbar=tk.Scrollbar(frame,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)
vbar.config(command=canvas.yview)
canvas.config(height=frameheight)
canvas.config(yscrollcommand=vbar.set)
canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH,pady=20)

tk.Button(root,text=loc('button_convert'),command=button_go).grid(row=row,column=1)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=8)
root.grid_columnconfigure(2, weight=1)

if os.path.exists('prefs'):
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
                object_entries[type][0].insert(0, value)
                object_entries[type][1].set(int(arg3))
                if int(arg3) == 1:
                    object_entries[type][0].configure(state='normal')
                else:
                    object_entries[type][0].configure(state='disabled')

root.mainloop()
