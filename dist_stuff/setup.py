from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'bundle_files': 2}},
    zipfile = None,
    windows = [{
        'script': 'rmj2gms.py',
        'icon_resources': [(1, 'icon.ico')]
    }],
)