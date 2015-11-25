# handles user input / controls window

import tkinter as tk
from tkinter import filedialog, messagebox
import convert, localize
import sys, os, imp

def loc(key):
    return localize.loc(key)

def update_object_widgets(check_enabled, entry, button):
    if check_enabled:
        state = tk.NORMAL
    else:
        state = tk.DISABLED
    entry.configure(state=state)
    button.configure(state=state)

def ask_path(entry, dialogtitle, filetypes, initialdir_func, format_func):
    path = filedialog.askopenfilename(filetypes=filetypes,title=dialogtitle,initialdir=initialdir_func())
    if path != '':
        path = format_func(path)
        entry.delete(0, tk.END)
        entry.insert(0, path)
        entry.xview(tk.END)

def row_askpath(row, labeltext, dialogtitle, filetypes, initialdir_func, format_func):
    tk.Label(root,text=labeltext).grid(row=row,column=0,sticky=tk.E)
    entry = tk.Entry(root)
    entry.grid(row=row,column=1,sticky=tk.EW)
    cmd = lambda: ask_path(entry, dialogtitle, filetypes, initialdir_func, format_func)
    b = tk.Button(root,image=folder_image,width=35,height=25,command=cmd)
    b.grid(row=row,column=2)
    return entry

def ask_language():
    global chosen
    window = tk.Tk()
    window.resizable(False, False)
    window.geometry('300x100')
    window.wm_title('')
    window.protocol('WM_DELETE_WINDOW', lambda: None)
    icon_image = tk.Image('photo', file='images/icon.png')
    window.tk.call('wm','iconphoto',window._w,icon_image)
    def choose(c):
        global chosen
        window.destroy()
        chosen = c
    tk.Button(window, text='English', command=lambda: choose('English')).grid(row=0,column=0,sticky=tk.NSEW,padx=10,pady=10)
    tk.Button(window, text='日本語', command=lambda: choose('Japanese')).grid(row=0,column=1,sticky=tk.NSEW,padx=10,pady=10)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.mainloop()
    return chosen

def change_language(language):
    with open('lang', 'w') as f:
        f.write(language)
    os.execl(sys.executable, sys.executable, * sys.argv)

def show_instructions():
    instructions = {'English':'instructions_en.html','Japanese':'instructions_jp.html'}
    os.startfile(instructions[localize.language])

def show_readme():
    readmes = {'English':'readme_en.txt','Japanese':'readme_jp.txt'}
    os.startfile(readmes[localize.language])

def submit(submit_function, convert_button, *args):
    convert_button.config(text=loc('button_convert_working') + '  ')
    root.update()
    
    #try:
    #    message = submit_function(*args)
    #except:
    #    message = 'There was an error. Please tell Patrick about this.\n%s' % traceback.format_exc()
    #    traceback.print_exc()
    
    print(args)
    
    convert_button.config(text=loc('button_convert') + '  ')
    root.update()
    #messagebox.showinfo('', message)
    
def run(submit_func):
    # init stuff
    global root, folder_image
    
    root = tk.Tk()
    folder_image = tk.Image('photo', file='images/folder.png')
    
    # window contents
    current_row = 0
    labeltext = loc('label_project_file')
    dialogtitle = loc('open_project_file')
    filetypes = [('GameMaker: Studio project', '.project.gmx')]
    initialdir_func = lambda: ''
    format_func = lambda path: path
    project_textbox = row_askpath(current_row, labeltext, dialogtitle, filetypes, initialdir_func, format_func)
    
    current_row += 1
    labeltext = loc('label_template_room')
    dialogtitle = loc('open_template_room')
    filetypes = [('GameMaker: Studio room', '.room.gmx')]
    initialdir_func = lambda: os.path.join(os.path.split(project_textbox.get())[0],'rooms')
    format_func = lambda path: os.path.split(path)[1].split('.')[0]
    templateroom_textbox = row_askpath(current_row, labeltext, dialogtitle, filetypes, initialdir_func, format_func)
    
    current_row += 1
    labeltext = loc('label_rmj_map')
    dialogtitle = loc('open_rmj_map')
    filetypes = [('RMJ map', '.map')]
    initialdir_func = lambda: ''
    format_func = lambda path: path
    map_textbox = row_askpath(current_row, labeltext, dialogtitle, filetypes, initialdir_func, format_func)

    object_images = [('block','images/block.png'),#2
                     ('spikeup','images/spikeup.png'),#12
                     ('spikeright','images/spikeright.png'),#11
                     ('spikeleft','images/spikeleft.png'),#10
                     ('spikedown','images/spikedown.png'),#9
                     ('miniup','images/miniup.png'),#19
                     ('miniright','images/miniright.png'),#18
                     ('minileft','images/minileft.png'),#17
                     ('minidown','images/minidown.png'),#16
                     ('save','images/save.png'),#32
                     ('platform','images/platform.png'),#31
                     ('water1','images/water1.png'),#23
                     ('water2','images/water2.png'),#30
                     ('cherry','images/cherry.png'),#20
                     ('hurtblock','images/hurtblock.png'),#27
                     ('vineright','images/vineright.png'),#28
                     ('vineleft','images/vineleft.png'),#29
                     ('start','images/start.png'),#3
                     ]

    objectrowheight = 40
    frameheight = 3 * objectrowheight
    canvasheight = (len(object_images) - 1) * objectrowheight

    current_row += 1
    frame = tk.Frame(root,height=frameheight,relief=tk.GROOVE,borderwidth=2)
    frame.grid(row=current_row,column=0,columnspan=3,padx=5,pady=5,sticky=tk.EW)
    canvas = tk.Canvas(frame,scrollregion=(0,0,0,canvasheight),yscrollincrement=objectrowheight)
    objectrow = 0

    object_widgets = {}
    for objectname, imagepath in object_images:
        photo = tk.PhotoImage(file=imagepath)
        w = tk.Label(root,image=photo)
        w.photo = photo # to prevent it from being garbage collected
        canvas.create_window((25,0+objectrow*objectrowheight),anchor=tk.CENTER,window=w)
        e = tk.Entry(root,state=tk.DISABLED)
        canvas.create_window((60,0+objectrow*objectrowheight),anchor=tk.W,window=e,width=120)
        
        initialdir_func = lambda: os.path.join(os.path.split(project_textbox.get())[0],'objects')
        format_func = lambda path: os.path.split(path)[1].split('.')[0]
        cmd = lambda: ask_path(e, loc('open_object'), [('GM:S object', '.object.gmx')], initialdir_func, format_func)
        b = tk.Button(root,image=folder_image,command=cmd,state=tk.DISABLED)
        
        canvas.create_window((190,0+objectrow*objectrowheight),anchor=tk.W,window=b,width=40,height=30)
        v = tk.BooleanVar()
        v.set(False)
        cmd = lambda var=v,entry=e,button=b: update_object_widgets(var.get(),entry,button)
        c = tk.Checkbutton(root,text=loc('label_object_enabled'),variable=v,command=cmd)
        canvas.create_window((240,0+objectrow*objectrowheight),anchor=tk.W,window=c)
        object_widgets[objectname] = (e, v, b)
        objectrow += 1

    vbar=tk.Scrollbar(frame,orient=tk.VERTICAL)
    vbar.pack(side=tk.RIGHT,fill=tk.Y)
    vbar.config(command=canvas.yview)
    canvas.config(height=frameheight,width=340)
    canvas.config(yscrollcommand=vbar.set)
    canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH,pady=20)

    current_row += 1
    icon_image = tk.Image('photo', file='images/icon.png')
    convert_button = tk.Button(root,text=loc('button_convert') + '  ',image=icon_image,compound=tk.RIGHT)
    cmd = lambda: submit(submit_func, convert_button, project_textbox.get(), templateroom_textbox.get(), map_textbox.get(), {k: (v[0].get(),v[1].get()) for (k,v) in object_widgets.items()})
    convert_button.configure(command=cmd)
    convert_button.grid(row=current_row,column=1,columnspan=2,sticky=tk.NSEW)

    # load values from prefs file
    if os.path.exists('prefs'):
        with open('prefs', 'r') as f:
            for line in f:
                args = line[:-1].split('|')
                args += [''] * (3 - len(args))
                type, value, arg3 = args
                if type == 'template':
                    templateroom_textbox.insert(0, value)
                    templateroom_textbox.xview(tk.END)
                elif type == 'project':
                    project_textbox.insert(0, value)
                    project_textbox.xview(tk.END)
                else:
                    object_widgets[type][0].insert(0, value)
                    object_widgets[type][1].set(int(arg3))
                    update_object_widgets(type)
    
    # menu bar
    menubar = tk.Menu(root)
    optionsmenu = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label=loc('menu_options'), menu=optionsmenu)
    optionsmenu.add_command(label=loc('menu_instructions'), command=lambda: show_instructions())
    optionsmenu.add_command(label=loc('menu_readme'), command=lambda: show_readme())
    languagemenu = tk.Menu(menubar, tearoff=False)
    languagemenu.add_command(label='English (restarts program)', command=lambda: change_language('English'), state=tk.DISABLED if localize.language == 'English' else tk.NORMAL)
    languagemenu.add_command(label='日本語 (プログラームを再起動)', command=lambda: change_language('Japanese'), state=tk.DISABLED if localize.language == 'Japanese' else tk.NORMAL)
    optionsmenu.add_cascade(label=loc('menu_language'), menu=languagemenu)
    root.config(menu=menubar)
    
    # configure window and enter its main loop
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.grid_columnconfigure(0, weight=1, minsize=120)
    root.grid_columnconfigure(1, weight=8, minsize=150)
    root.grid_columnconfigure(2, minsize=50)
    root.resizable(True, True)
    root.wm_title(loc('title'))
    root.tk.call('wm','iconphoto',root._w,icon_image)
    root.mainloop()
