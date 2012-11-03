from setuptools import setup

APP = ['main.py']

OPTIONS = {'argv_emulation':False, 'includes':['os','random','pygame', 'sys',\
                                               'boarder','clickclack','easywin','freeze',\
                                               'manager','minigame','missiles','platformer',\
                                               'runner','slides','tmx','transfer','whackamullet',\
                                               '.tbg.board','.tbg.io.mouse','itertools','.tbg.terrain',\
                                               '.tbg.units.protag','.tbg.units.archer','.tbg.units.dude',\
                                               '.tbg.units.zombie','.tbg.units.mullet', '__future__', \
                                               '.tbg.terrain.base','heapq', '.tbg.terrain.terrain',\
                                               '.tbg.terrain.sand','.tbg.terrain.grass','.tbg.terrain.water',\
                                               '.tbg.units.unit'],}

setup(
    app=APP,
    options={'py2app':OPTIONS},
    setup_requires=['py2app'],
    )
