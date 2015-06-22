import tkinter as tk
from tkinter import filedialog
import convert

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
    entities = convert.get_entities_from_rmj(rmj)
    convert.write_room(entities, roomname, template)
    convert.add_room_to_project(roomname, project)
    
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