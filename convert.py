def group(lst, n):
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            yield tuple(val)

name_to_rmj = {'12':'spikeUp','9':'spikeDown','11':'spikeRight','10':'spikeLeft','2':'block','32':'save','3':'start','20':'end'}

rmj_filename = 'map.map'
with open(rmj_filename) as f:
    line = f.readlines()[3]
    entities = list(group(line.split(' ')[1:], 3))
for i, ent in enumerate(entities):
    entities[i] = (ent[0], ent[1], name_to_rmj[ent[2]])

formatstring = '    <instance objName="%s" x="%s" y="%s" name="inst_%s" locked="0" code="" scaleX="1" scaleY="1" colour="4294967295" rotation="0"/>'

template_filename = 'rTemplate.room.gmx'
output_filename = 'gm/gm/rooms/rOutput.room.gmx'

f = open(template_filename, 'r')
contents = f.readlines()
f.close()

for i, ent in enumerate(entities):
    subbed = formatstring % (ent[2], ent[0], ent[1], hex(i)[2:].upper().zfill(8))
    contents.insert(53, subbed)

f = open(output_filename, 'w')
contents = ''.join(contents)
f.write(contents)
f.close()