# actual conversion logic

import os, random, xml.etree.ElementTree as ET

object_ids = {
    'block':(2,1),
    'spikeup':(12,3),
    'spikeright':(11,4),
    'spikeleft':(10,5),
    'spikedown':(9,6),
    'miniup':(19,7),
    'miniright':(18,8),
    'minileft':(17,9),
    'minidown':(16,10),
    'save':(32,12),
    'platform':(31,13),
    'water1':(23,14),
    'water2':(30,15),
    'cherry':(20,11),
    'hurtblock':(27,18),
    'vineright':(28,17),
    'vineleft':(29,16),
    'start':(3,20),
    }

def convert(project_path, template_room_path, map_path, chosen_names):

    # build conversion dicts according to chosen object names
    rmj_to_objectname = {}
    jtool_to_objectname = {}
    for name, gm_name in chosen_names.items():
        rmj_id, jtool_id = object_ids[name]
        rmj_to_objectname[str(rmj_id)] = gm_name
        jtool_to_objectname[str(jtool_id)] = gm_name

    # read instances from map file
    map_instances = []
    with open(map_path) as f:
        line = f.readlines()[3]
    numbers = line[1:].split(' ')
    for i in range(0, len(numbers), 3):
        x, y, id = numbers[i:i+3]
        if id in rmj_to_objectname:
            map_instances.append((x,y,rmj_to_objectname[id]))

    # determine room name to avoid naming conflict
    output_room_name = 'rMapImport_%s' % os.path.split(map_path)[1].split('.')[0]
    project_tree = ET.parse(project_path)
    project_root = project_tree.getroot()
    def room_exists(roomname):
        for room_element in project_root.find('rooms').iter('room'):
            if room_element.text.split('\\')[1] == roomname:
                return True
        return False
    if room_exists(output_room_name):
        counter = 1
        base_room_name = output_room_name + '_'
        output_room_name = base_room_name + str(counter)
        while room_exists(output_room_name):
            counter += 1
            output_room_name = base_room_name + str(counter)

    output_room_path = os.path.join(os.path.split(project_path)[0],'rooms',output_room_name+'.room.gmx')

    # create a new room file (based on template) with the instances added
    output_room_tree = ET.parse(template_room_path)
    instances_element = output_room_tree.getroot().find('instances')
    for x, y, name in map_instances:
        attrib = {}
        attrib['x'] = x
        attrib['y'] = y
        attrib['objName'] = name
        attrib['locked'] = '0'
        attrib['code'] = ''
        attrib['scaleX'] = '1'
        attrib['scaleY'] = '1'
        attrib['colour'] = '4294967295'
        attrib['rotation'] = '0'
        attrib['name'] = 'inst_'+''.join([random.choice('0123456789ABCDEF') for i in range(8)])
        new_element = ET.Element('instance', attrib=attrib)
        instances_element.append(new_element)
        output_room_tree.write(output_room_path)

    # add our new room to the project
    new_room_element = ET.Element('room')
    new_room_element.text = 'rooms\\'+output_room_name
    project_root.find('rooms').append(new_room_element)
    project_tree.write(project_path)

    return output_room_name
