def group(lst, n):
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            yield val

rmj_to_gm = {'12':'spikeUp','9':'spikeDown','11':'spikeRight','10':'spikeLeft','2':'block','32':'save','3':'start','20':'end'}

rmj_filename = 'map.map'
with open(rmj_filename) as f:
    line = f.readlines()[3]
    entities = list(group(line[1:].split(' '), 3))
for ent in entities:
    ent[2] = rmj_to_gm[ent[2]]

template_filename = 'rTemplate.room.gmx'
output_filename = 'gm/rooms/rOutput.room.gmx'

with open(template_filename, 'r') as f:
    lines = f.readlines()

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

with open(output_filename, 'w') as f:
    f.write(''.join(lines))
