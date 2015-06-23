import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import convert
import sys
import os

def ask_path(entry, title, filetypes):
    path = filedialog.askopenfilename(filetypes=filetypes,title=title)
    if path != "":
        entry.delete(0, tk.END)
        entry.insert(0, path)
        entry.xview(tk.END)
        
def button_go():
    rmj = entry_rmj.get()
    roomname = entry_roomname.get()
    template = entry_template.get()
    project = entry_project.get()
    rmj_to_gm = {}
    emptyObject = False
    for key, val in object_entries.items():
        text = val[0].get()
        enabled = val[1].get()
        if enabled:
            rmj_to_gm[key] = text
        if text == '' and enabled:
            emptyObject = True

    if rmj == '' or roomname == '' or template == '' or project == '' or emptyObject:
        messagebox.showinfo('', 'Cant have empty fields.')
        return

    with open('prefs', 'w') as f:
        f.write('template|%s\n' % template)
        f.write('project|%s\n' % project)
        for key, value in object_entries.items():
            f.write('%s|%s|%s\n' % (key, value[0].get(), value[1].get()))

    fn = os.path.join(os.path.split(project)[0], 'rooms', roomname + '.room.gmx')
    if os.path.exists(fn):
        messagebox.showinfo('', 'Room with that name currently exists. This tool won\'t overwrite it; delete the room manually if you\'re sure.')
        return
    try:
        entities = convert.get_entities_from_rmj(rmj, rmj_to_gm)
        convert.write_room(entities, roomname, project, template)
        convert.add_room_to_project(roomname, project)
        messagebox.showinfo('', 'Successfully converted! Prefs saved.')
    except:
        info = sys.exc_info()
        with open('errorlog.txt', 'w') as f:
            f.write('Last error:\n\n%s\n%s\n%s' % info)
        #todo: print stack trace
        messagebox.showinfo('', 'There was an error when converting. Exception logged in errorlog.txt.\nLikely reasons: File at a path doesn\'t exist, File is the wrong type or is malformed, Don\'t have permissions to modify file. Hopefully it\'s not a bug in the program.')
    
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
    tk.Label(root,text='Room name:').grid(row=row,column=0,sticky=tk.E)
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
    canvas.create_window((0,0+objectrow*objectrowheight),anchor=tk.W,window=w)
    e = tk.Entry(root)
    canvas.create_window((50,0+objectrow*objectrowheight),anchor=tk.W,window=e)
    v = tk.IntVar()
    c = tk.Checkbutton(root,text="Enabled",variable=v,command=lambda: check_clicked(rmj_id))
    canvas.create_window((200,0+objectrow*objectrowheight),anchor=tk.W,window=c)
    object_entries[rmj_id] = (e, v)
    objectrow += 1


object_images = [('2','images/temp.gif'),#block
                 ('12','images/temp.gif'),#spike up right left down
                 ('11','images/temp.gif'),
                 ('10','images/temp.gif'),
                 ('9','images/temp.gif'),
                 #('19','images/temp.gif'),#mini spike up right left down
                 #('18','images/temp.gif'),
                 #('17','images/temp.gif'),
                 #('16','images/temp.gif'),
                 #('32','images/temp.gif'),#save
                 #('31','images/temp.gif'),#movingPlatform
                 #('23','images/temp.gif'),#water1
                 #('30','images/temp.gif'),#water2
                 #('20','images/temp.gif'),#apple
                 #('27','images/temp.gif'),#hurt block
                 #('28','images/temp.gif'),#ivy right
                 #('29','images/temp.gif'),#ivy left
                 ]

objectrowheight = 40
frameheight = 3 * objectrowheight
canvasheight = (len(object_images) - 1) * objectrowheight

row = 0
root = tk.Tk()
root.wm_title('RMJ to GM:S converter')

object_entries = {}

entry_rmj = row_askpath('RMJ map:', 'Select RMJ Map', [('RMJ map', '.map'),('all files', '.*')])
entry_roomname = row_entry('Room name:')
entry_template = row_askpath('Template room:', 'Select Template Room', [('GM:S room', '.room.gmx'),('all files', '.*')])
entry_project = row_askpath('Project file:', 'Select Project', [('GM:S project', '.project.gmx'),('all files', '.*')])

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

tk.Button(root,text='Convert',command=button_go).grid(row=row,column=1)

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
