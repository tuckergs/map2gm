langs = {}
for lang in ['English']:
    langs[lang] = {}
    with open('localization/%s.txt' % lang, 'r') as f:
        for line in f:
            key, val = line[:-1].split('=')
            langs[lang][key] = val
            
def loc(key):
    return langs['English'][key]