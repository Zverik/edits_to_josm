#!/usr/bin/env python3
import xml.etree.ElementTree as etree
import sys
import math


if len(sys.argv) < 2:
    print('Usage: {} <edits.xml> [<output.osm>]'.format(sys.argv[0]))
    sys.exit(1)

root = etree.parse(sys.argv[1]).getroot()
osm = etree.Element('osm', version='0.6', upload='false')
global_id = 1
for mwm in root.findall('mwm'):
    for action in mwm:
        for mod in action:
            if mod.tag not in ('node', 'way', 'relation'):
                continue
            if action.tag == 'delete':
                raise ValueError('Cannot process deleted elements.')
            elif action.tag == 'modify':
                if mod.get('upload_status') == 'Uploaded':
                    continue
            elif action.tag == 'obsolete':
                pass
            elif action.tag == 'create':
                if mod.get('upload_status') == 'Uploaded':
                    continue
            else:
                raise ValueError('Unknown action tag: {}'.format(action.tag))

            obj = etree.SubElement(osm, mod.tag, id=str(global_id), version='1')
            global_id += 1
            if mod.tag == 'node':
                obj.set('lat', mod.get('lat'))
                obj.set('lon', mod.get('lon'))
            elif mod.tag == 'way':
                cnt = 0
                for nd in mod.findall('nd'):
                    etree.SubElement(obj, 'nd', ref=str(global_id))
                    cnt += 1
                    if cnt % 3 == 0:
                        etree.SubElement(obj, 'nd', ref=str(global_id-2))
                    lat = 360.0 * math.atan(math.tanh(
                        float(nd.get('y')) * math.pi / 360.0)) / math.pi
                    etree.SubElement(osm, 'node', id=str(global_id), version='1',
                                     lon=nd.get('x'), lat=str(lat))
                    global_id += 1
            elif mod.tag == 'relation':
                raise ValueError('Cannot process relations yet')

            for tag in mod.findall('tag'):
                etree.SubElement(obj, 'tag', k=tag.get('k'), v=tag.get('v'))
            if action.tag in ('modify', 'create'):
                error = mod.get('upload_error', mod.get('upload_status'))
            elif action.tag == 'obsolete':
                error = 'Obsolete'
            etree.SubElement(obj, 'tag', k='upload_error', v=error)

result = etree.tostring(osm, encoding='utf-8').decode('utf-8')
if len(sys.argv) < 3:
    print(result)
else:
    with open(sys.argv[2], 'w') as f:
        f.write(result)
