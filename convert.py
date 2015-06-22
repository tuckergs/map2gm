def group(lst, n):
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            yield val 
def read_lines(filename):    
    with open(filename, 'r') as f:
        return f.readlines()
def write_lines(filename, lines):
    with open(filename, 'w') as f:
        f.write(''.join(lines))

def get_entities_from_rmj(rmj_filename):
    rmj_to_gm = {'12':'spikeUp','9':'spikeDown','11':'spikeRight','10':'spikeLeft','2':'block','32':'save','3':'start','20':'end'}
    with open(rmj_filename) as f:
        line = f.readlines()[3]
        entities = list(group(line[1:].split(' '), 3))
    for ent in entities:
        ent[2] = rmj_to_gm[ent[2]]
    return entities

def write_room(entities, room_name, template_filename):
    output_filename = 'gm/rooms/%s.room.gmx' % room_name
    lines = read_lines(template_filename)
    try:
        i = lines.index('  <instances/>\n')
        lines[i] = '  <instances>\n'
        lines.insert(i + 1, '  </instances>\n')
    except ValueError:
        pass
    formatstring = '    <instance objName="%s" x="%s" y="%s" name="inst_%s" locked="0" code="" scaleX="1" scaleY="1" colour="4294967295" rotation="0"/>\n'
    startindex = lines.index('  <instances>\n') + 1
    for i, ent in enumerate(entities):
        subbed = formatstring % (ent[2], ent[0], ent[1], hex(i)[2:].upper().zfill(8))
        lines.insert(startindex, subbed)
    write_lines(output_filename, lines)

def add_room_to_project(room_name, project_filename):
    lines = read_lines(project_filename)
    found = False
    for line in lines:
        if room_name in line:
            found = True
            break
    if not found:
        folder_name = 'RMJ imports'
        try:
            lines.index('    <rooms name="%s">\n' % folder_name)
        except ValueError:
            i = lines.index('  </rooms>\n')
            lines.insert(i, '    <rooms name="%s">\n' % folder_name)
            lines.insert(i + 1, '    </rooms>\n')
        startindex = lines.index('    <rooms name="%s">\n' % folder_name) + 1
        subbed = '      <room>rooms\%s</room>\n' % room_name
        lines.insert(startindex, subbed)
        write_lines(project_filename, lines)