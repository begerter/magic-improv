# "Tiled" TMX loader/renderer and more
# inspired initially by http://silveiraneto.net/2009/12/19/tiled-tmx-map-loader-for-pygame/
# but mostly rewritten and much broader in scope.

# Taken from Richard Jones' pygame tutorial
# Loads xml tile maps

import sys, pygame, struct
from pygame.locals import *
from pygame import Rect
from xml import sax

class Tile(object):
    def __init__(self, gid, surface, tileset):
        self.gid = gid
        self.surface = surface
        self.tile_width = tileset.tile_width
        self.tile_height = tileset.tile_height
        self.properties = {}
    def __repr__(self):
        return '<Tile %d>' % self.gid

class Tileset(object):
    def __init__(self, name, tile_width, tile_height, firstgid):
        self.name = name
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.firstgid = firstgid
        self.tiles = []

    def add_image(self, file):
        image = pygame.image.load(file).convert_alpha()
        if not image:
            sys.exit("Error creating new Tileset: file %s not found" % file)
        id = self.firstgid
        for line in xrange(image.get_height()/self.tile_height):
            for column in xrange(image.get_width()/self.tile_width):
                pos = Rect(column*self.tile_width,
                    line*self.tile_height,
                    self.tile_width,
                    self.tile_height )
                self.tiles.append(Tile(id, image.subsurface(pos), self))
                id += 1

    def get_tile(self, gid):
        return self.tiles[gid - self.firstgid]

class Tilesets(dict):
    def add(self, tileset):
        for i, tile in enumerate(tileset.tiles):
            i += tileset.firstgid
            self[i] = tile

class Cell(object):
    '''Layers are made of Cells (or empty space).

    Cells have some basic properties:

    x, y - the cell's index in the layer
    px, py - the cell's pixel position
    left, right, top, bottom - the cell's pixel boundaries

    Additionally the cell may have other properties which are accessed using
    standard dictionary methods:

       cell['property name']

    You may assign a new value for a property to or even delete an existing
    property from the cell - this will not affect the Tile or any other Cells
    using the Cell's Tile.
    '''
    def __init__(self, x, y, px, py, tile):
        self.x, self.y = x, y
        self.px, self.py = px, py
        self.tile = tile
        self.left = px
        self.right = px + tile.tile_width
        self.top = py
        self.bottom = py + tile.tile_height
        self._added_properties = {}
        self._deleted = set()
    def __repr__(self):
        return '<Cell %s,%s %d>' % (self.px, self.py, self.tile.gid)
    def __contains__(self, key):
        if key in self._deleted:
            return False
        return key in self._added_properties or key in self.tile.properties
    def __getitem__(self, key):
        if key in self._deleted:
            raise KeyError(key)
        if key in self._added_properties:
            return self._added_properties[key]
        if key in self.tile.properties:
            return self.tile.properties[key]
        raise KeyError(key)
    def __setitem__(self, key, value):
        self._added_properties[key] = value
    def __delitem__(self, key, value):
        self._deleted_properties.add(key)
    def intersects(self, other):
        '''Determine whether this Cell intersects with the other rect (which has
        .x, .y, .width and .height attributes.)
        '''
        if self.px + self.tile.tile_width < other.x: return False
        if other.x + other.width < self.px: return False
        if self.py + self.tile.tile_height < other.y: return False
        if other.y + other.height < self.py: return False
        return True

class Layer(object):
    def __init__(self, name, visible, map):
        self.name = name
        self.visible = visible
        # TODO get from TMX
        self.px_width = map.px_width
        self.px_height = map.px_height
        self.tile_width = map.tile_width
        self.tile_height = map.tile_height
        self.width = map.width
        self.height = map.height
        self.tilesets = map.tilesets
        self.group = pygame.sprite.Group()
        self.properties = {}
        self.cells = {}

    def set_data(self, data):
        assert len(data) == self.width * self.height
        for i, gid in enumerate(data):
            if gid < 1: continue   # not set
            tile = self.tilesets[gid]
            x = i % self.width
            y = i // self.width
            self.cells[x,y] = Cell(x, y, x*self.tile_width, y*self.tile_height, tile)

    def update(self, dt, *args):
        pass

    def set_view(self, x, y, w, h, viewport_ox=0, viewport_oy=0):
        self.view_x, self.view_y = x, y
        self.view_w, self.view_h = w, h
        x -= viewport_ox
        y -= viewport_oy
        self.position = (x, y)

    def draw(self, screen):
        ox, oy = self.position
        w, h = self.view_w, self.view_h
        for x in range(ox, ox+w+self.tile_width, self.tile_width):
            i = x // self.tile_width
            for y in range(oy, oy+h+self.tile_height, self.tile_height):
                j = y // self.tile_height
                if (i, j) not in self.cells:
                    continue
                cell = self.cells[i, j]
                screen.blit(cell.tile.surface, (cell.px-ox, cell.py-oy))

    def find(self, *properties):
        '''Find all cells with the given properties set.
        '''
        r = []
        for propname in properties:
            for cell in self.cells.values():
                if propname in cell:
                    r.append(cell)
        return r

    def match(self, **properties):
        '''Find all cells with the given properties set to the given values.
        '''
        r = []
        for propname in properties:
            for cell in self.cells.values():
                if propname not in cell:
                    continue
                if properties[propname] == cell[propname]:
                    r.append(cell)
        return r

    def collide(self, rect, propname):
        '''Find all cells the rect is touching that have the indicated property
        name set.
        '''
        r = []
        for cell in self.get_in_region(rect.left, rect.top, rect.right, rect.bottom):
            if not cell.intersects(rect):
                continue
            if propname in cell.tile.properties:
                r.append(cell)
        return r

    def get_in_region(self, x1, y1, x2, y2):
        '''Return cells (in [column][row]) that are within the map-space
        pixel bounds specified by the bottom-left (x1, y1) and top-right
        (x2, y2) corners.

        Return a list of Cell instances.
        '''
        i1 = max(0, x1 // self.tile_width)
        j1 = max(0, y1 // self.tile_height)
        i2 = min(self.width, x2 // self.tile_width + 1)
        j2 = min(self.height, y2 // self.tile_height + 1)
        return [self.cells[i, j]
            for i in range(int(i1), int(i2))
                for j in range(int(j1), int(j2))
                    if (i, j) in self.cells]

class SpriteLayer(pygame.sprite.AbstractGroup):
    def __init__(self):
        super(SpriteLayer, self).__init__()
        self.visible = True

    def set_view(self, x, y, w, h, viewport_ox=0, viewport_oy=0):
        self.view_x, self.view_y = x, y
        self.view_w, self.view_h = w, h
        x -= viewport_ox
        y -= viewport_oy
        self.position = (x, y)

    def draw(self, screen):
        ox, oy = self.position
        w, h = self.view_w, self.view_h
        for sprite in self.sprites():
            sx, sy = sprite.rect.topleft
            screen.blit(sprite.image, (sx-ox, sy-oy))

class Layers(list):
    def __init__(self):
        self.by_name = {}

    def add_named(self, layer, name):
        self.append(layer)
        self.by_name[name] = layer

    def __getitem__(self, item):
        if isinstance(item, int):
            return self[item]
        return self.by_name[item]

class TileMap(sax.ContentHandler):
    def __init__(self, size, origin=(0,0)):
        self.px_width = 0
        self.px_height = 0
        self.tile_width = 0
        self.tile_height = 0
        self.width = 0
        self.height  = 0
        self.properties = {}
        self.layers = Layers()
        self.tilesets = Tilesets()
        self.layer = None
        self.tile = None
        self.tileset = None
        self.is_data = False
        self.fx, self.fy = 0, 0             # viewport focus point
        self.view_w, self.view_h = size     # viewport size
        self.view_x, self.view_y = origin   # viewport offset

    def update(self, dt, *args):
        for layer in self.layers:
            layer.update(dt, *args)

    def draw(self, screen):
        for layer in self.layers:
            if layer.visible:
                layer.draw(screen)

    def startElement(self, name, attrs):
        # get most general map informations and create a surface
        if name == 'map':
            self.width = int(attrs['width'])
            self.height  = int(attrs['height'])
            self.tile_width = int(attrs['tilewidth'])
            self.tile_height = int(attrs['tileheight'])
            self.px_width = self.width * self.tile_width
            self.px_height = self.height * self.tile_height

        elif name=="tileset":
            name = attrs['name']
            firstgid = int(attrs['firstgid'])
            ts = Tileset(name, self.tile_width, self.tile_height, firstgid)
            self.tileset = ts

        elif name=="image":
            # create a tileset
            # TODO width, height
            self.tileset.add_image(attrs['source'])

        elif name == 'property':
            # store additional properties.
            name = attrs['name']
            value = attrs['value']
            # TODO hax
            if value.isdigit():
                value = int(value)
            if self.tile is not None:
                self.tile.properties[name] = value
            elif self.layer is not None:
                self.layer.properties[name] = value
            else:
                self.properties[name] = value

        # starting counting
        elif name == 'layer':
            self.layer = Layer(attrs['name'], int(attrs.get('visible', 1)), self)
            self.layers.add_named(self.layer, attrs['name'])

        elif name == 'data':
            self.is_data = True

        elif name == 'tile':
            gid = self.tileset.firstgid + int(attrs['id'])
            self.tile = self.tileset.get_tile(gid)

    def characters(self, data):
        if self.is_data:
            data = data.strip()
            if not data: return
            data = data.decode('base64').decode('zlib')
            data = struct.unpack('<%di' % (len(data)/4,), data)
            self.layer.set_data(data)
        else:
            pass

    def endElement(self, name):
        if name == 'layer':
            self.layer = None
        elif name=="tileset":
            self.tilesets.add(self.tileset)
            self.tileset = None
        elif name=="tile":
            self.tile = None
        elif name == 'data':
            self.is_data = False

    _old_focus = None
    def set_focus(self, fx, fy, force=False):
        '''Determine the viewport based on a desired focus pixel in the
        Layer space (fx, fy) and honoring any bounding restrictions of
        child layers.

        The focus will always be shifted to ensure no child layers display
        out-of-bounds data, as defined by their dimensions px_width and px_height.
        '''
        # The result is that all chilren will have their viewport set, defining
        # which of their pixels should be visible.
        fx, fy = int(fx), int(fy)
        self.fx, self.fy = fx, fy

        a = (fx, fy)

        # check for NOOP (same arg passed in)
        if not force and self._old_focus == a:
            return
        self._old_focus = a

        # get our viewport information, scaled as appropriate
        w = int(self.view_w)
        h = int(self.view_h)
        w2, h2 = w//2, h//2

        if self.px_width <= w:
            # this branch for centered view and no view jump when
            # crossing the center; both when world width <= view width
            restricted_fx = self.px_width / 2
        else:
            if (fx - w2) < 0:
                restricted_fx = w2       # hit minimum X extent
            elif (fx + w2) > self.px_width:
                restricted_fx = self.px_width - w2       # hit maximum X extent
            else:
                restricted_fx = fx
        if self.px_height <= h:
            # this branch for centered view and no view jump when
            # crossing the center; both when world height <= view height
            restricted_fy = self.px_height / 2
        else:
            if (fy - h2) < 0:
                restricted_fy = h2       # hit minimum Y extent
            elif (fy + h2) > self.px_height:
                restricted_fy = self.px_height - h2       # hit maximum Y extent
            else:
                restricted_fy = fy

        # ... and this is our focus point, center of screen
        self.restricted_fx = int(restricted_fx)
        self.restricted_fy = int(restricted_fy)

        # determine child view bounds to match that focus point
        x, y = int(restricted_fx - w2), int(restricted_fy - h2)

        self.childs_ox = x - self.view_x
        self.childs_oy = y - self.view_y

        for layer in self.layers:
            layer.set_view(x, y, w, h, self.view_x, self.view_y)

    def force_focus(self, fx, fy):
        '''Force the manager to focus on a point, regardless of any managed layer
        visible boundaries.

        '''
        # This calculation takes into account the scaling of this Layer (and
        # therefore also its children).
        # The result is that all chilren will have their viewport set, defining
        # which of their pixels should be visible.
        self.fx, self.fy = map(int, (fx, fy))
        self.fx, self.fy = fx, fy

        # get our view size
        w = int(self.view_w)
        h = int(self.view_h)
        w2, h2 = w//2, h//2

        # bottom-left corner of the
        x, y = fx - w2, fy - h2

        self.childs_ox = x - self.view_x
        self.childs_oy = y - self.view_y

        for layer in self.layers:
            layer.set_view(x, y, w, h, self.view_x, self.view_y)

    def pixel_from_screen(self, x, y):
        '''Look up the Layer-space pixel matching the screen-space pixel.
        '''
        vx, vy = self.childs_ox, self.childs_oy
        return int(vx + x), int(vy + y)

    def pixel_to_screen(self, x, y):
        '''Look up the screen-space pixel matching the Layer-space pixel.
        '''
        screen_x = x-self.childs_ox
        screen_y = y-self.childs_oy
        return int(screen_x), int(screen_y)

def load(filename, viewport):
    parser = sax.make_parser()
    tilemap = TileMap(viewport)
    parser.setContentHandler(tilemap)
    parser.parse(filename)
    return tilemap
