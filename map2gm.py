# entry point, input sanitization, general controller stuff

import os
import gui, convert, localize, util

def loc(key):
    return localize.loc(key)

# object_inputs is a map: {object_name: (gm_object_name, enabled)}
def submitted(project_path, template_room_name, map_path, object_inputs):

    project_extension = project_path.split('.')[-1]

    # input sanitization
    if project_path == '' or template_room_name == '' or map_path == '':
        return loc('error_top_field_empty')
    if not os.path.exists(project_path):
        # TODO localize
        return 'project does not exist'
    if not os.path.exists(map_path):
        # TODO localize
        return 'map does not exist'
    if project_extension == 'gmx':
        template_room_path = os.path.join(os.path.split(project_path)[0], 'rooms', template_room_name+'.room.gmx')
    else:
        template_room_path = os.path.join(util.get_application_path(), 'temp_gmksplit', 'Rooms', template_room_name+'.xml')
    if not os.path.exists(template_room_path):
        # TODO localize
        return 'template room does not exist'
    for objectname, enabled in object_inputs.values():
        if enabled:
            if objectname == '':
                return loc('error_object_no_name')
            if project_extension == 'gmx':
                object_path = os.path.join(os.path.split(project_path)[0], 'objects', objectname + '.object.gmx')
            else:
                object_path = os.path.join(util.get_application_path(), 'temp_gmksplit', 'Objects', objectname +'.xml')
            if not os.path.exists(object_path):
                return loc('error_nonexistent_object') % objectname

    # build dict of object names that were enabled
    chosen_object_names = {}
    for object_name, (gm_object_name, enabled) in object_inputs.items():
        if enabled:
            chosen_object_names[object_name] = gm_object_name

    output_room_name = convert.convert(project_path, template_room_path, map_path, chosen_object_names)

    # save preferences
    with open('prefs', 'w') as f:
        f.write('project|%s\n' % project_path)
        f.write('template|%s\n' % template_room_name)
        for object_name, (gm_object_name, enabled) in sorted(object_inputs.items()):
            f.write('%s|%s|%i\n' % (object_name, gm_object_name, enabled))

    return loc('convert_success') % output_room_name

# prompt and load language
if os.path.exists('lang'):
    with open('lang', 'r') as f:
        language = list(f)[0]
    localize.load(language)
else:
    language = gui.ask_language()
    with open('lang', 'w') as f:
        f.write(language)
    localize.load(language)
    gui.show_instructions()

# kick off the gui
gui.run(submit_func=submitted)
