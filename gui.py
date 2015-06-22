import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import convert
import sys
import os

def ask_path(entry):
    path = filedialog.askopenfilename()
    if path != "":
        entry.delete(0, tk.END)
        entry.insert(0, path)
        entry.xview(tk.END)
        
def button_go():
    rmj = entry_rmj.get()
    roomname = entry_roomname.get()
    template = entry_template.get()
    project = entry_project.get()
    if rmj == '' or roomname == '' or template == '' or project == '':
        messagebox.showinfo('', 'Cant have empty fields.')
        return
    fn = os.path.join(os.path.split(project)[0], 'rooms', roomname + '.room.gmx')
    if os.path.exists(fn):
        messagebox.showinfo('', 'Room with that name currently exists. This tool won\'t overwrite it; delete the room manually if you\'re sure.')
        return
    try:
        entities = convert.get_entities_from_rmj(rmj)
        convert.write_room(entities, roomname, project, template)
        convert.add_room_to_project(roomname, project)
    except:
        info = sys.exc_info()
        with open('errorlog.txt', 'w') as f:
            f.write('Last error:\n\n%s\n%s\n%s' % info)
        messagebox.showinfo('', 'There was an error when converting. Exception logged in errorlog.txt.\nLikely reasons: File at a path doesn\'t exist, File is the wrong type or is malformed, Don\'t have permissions to modify file. Hopefully it\'s not a bug in the program.')
    
def row_askpath(labeltext):
    global row
    tk.Label(root,text=labeltext).grid(row=row,column=0)
    entry = tk.Entry(root)
    entry.grid(row=row,column=1)
    tk.Button(root,text='find...',command=lambda: ask_path(entry)).grid(row=row,column=2)
    row += 1
    return entry
def row_entry(labeltext):
    global row
    tk.Label(root,text='Room name:').grid(row=row,column=0)
    entry = tk.Entry(root)
    entry.grid(row=1,column=1)
    row += 1
    return entry

row = 0
root = tk.Tk()
root.wm_title('RMJ to GM:S converter')
root.resizable(0,0)

entry_rmj = row_askpath('RMJ file:')
entry_roomname = row_entry('Room name:')
entry_template = row_askpath('Room template:')
entry_project = row_askpath('Project file:')
tk.Button(root,text='Convert',command=button_go).grid(row=row,column=1)

root.mainloop()