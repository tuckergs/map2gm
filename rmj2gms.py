import convert
import gui
import localize
import os, sys

def loc(key):
    return localize.loc(key)

def convert_pressed(rmj, roomname, template, project, rmj_to_gm):
    #for key, value in sorted(rmj_to_gm.items()):
    #    print('%s|%s|%s\n' % (key, value[0], value[1]))
    #return 'asdf'
    if rmj == '' or roomname == '' or template == '' or project == '':
        return loc('error_top_field_empty')
    for key, val in rmj_to_gm.items():
        text = val[0]
        enabled = val[1]
        if enabled:
            if text == '':
                return loc('error_object_no_name')
            else:
                fn = os.path.join(os.path.split(project)[0], 'objects', text + '.object.gmx')
                if not os.path.exists(fn):
                    return loc('error_nonexistent_object') % text
    fn = os.path.join(os.path.split(project)[0], 'rooms', roomname + '.room.gmx')
    if os.path.exists(fn):
        return loc('error_room_name_collision')
    try:
        entities = convert.get_entities_from_rmj(rmj, rmj_to_gm)
        convert.write_room(entities, roomname, project, template)
        convert.add_room_to_project(roomname, project)
        with open('prefs', 'w') as f:
            f.write('template|%s\n' % template)
            f.write('project|%s\n' % project)
            for key, value in sorted(rmj_to_gm.items()):
                f.write('%s|%s|%s\n' % (key, value[0], value[1]))
        return loc('convert_successful')
    except:
        info = sys.exc_info()
        with open('errorlog.txt', 'w') as f:
            f.write('Last error:\n\n%s\n%s\n%s' % info)
        #todo: print stack trace
        return loc('error_exception')

gui.run(convert_command=convert_pressed)