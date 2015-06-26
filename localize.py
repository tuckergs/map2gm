dict = {}

def load(lang):
    global language
    language = lang
    with open('localization/%s.txt' % language, 'r', encoding='UTF-8') as f:
        for line in f:
            key, val = line[:-1].split('=')
            dict[key] = val
            
def loc(key):
    if key in dict:
        return dict[key]
    else:
        return '!!NOT LOCALIZED'
