
import numpy
import random
import math


def root(s=1.0):
    w = s*2
    h = math.sqrt(3) / 2 * w
    a = s/2
    b = h/2
    z = 0.0
    return Tile({
        'e':      ( s,  z),
        'sse':    ( a, -b),
        'ssw':    (-a, -b),
        'w':      (-s,  z),
        'nnw':    (-a,  b),
        'nne':    ( a,  b),
        'center': ( z,  z),
    }, root=True)


class Tile:
    def __init__(s, points=None, height_bias=0, root=False):
        if points is None:
            s.points = {
                'e': None,
                'sse': None,
                'ssw': None,
                'w': None,
                'nnw': None,
                'nne': None,
                'center': None,
            }
        else:
            s.points = points

        s.subtiles = {
            'north': None,
            'northeast': None,
            'northwest': None,
            'south': None,
            'southeast': None,
            'southwest': None,
            'center': None,
        }
        # We need a more robust check.
        # After we start marking neighbors.
        # If a tile has no neighbor to the east or west, then don't bother with these corners.
        if not root:
            s.subtiles['eastcorner'] = None
            s.subtiles['westcorner'] = None

        s.neighbors = {
            'north': None,
            'northeast': None,
            'northwest': None,
            'south': None,
            'southeast': None,
            'southwest': None,
        }
        s.subdivided = False
        heightmap = {
            1: (0.2, 0.4, 0.6),
            2: (0.8, 0.4, 0.2),
            3: (0.6, 0.3, 0.2),
            4: (0.4, 0.2, 0.2),
            5: (0.2, 0.1, 0.2),
        }
        s.height = random.choice(list(heightmap.keys()))
        s.height = min(5, max(1, s.height + height_bias - 3))
        s.color = heightmap[s.height]
        s.root = root

    def subdivide(s):
        if any(p is None for p in s.points.values()):
            raise ValueError("Can not divide tile whose points have not been specified!")

        if s.subdivided:
            for subtile in s.subtiles.values():
                subtile.subdivide()
            return

        e   = s.points['e']
        sse = s.points['sse']
        ssw = s.points['ssw']
        w   = s.points['w']
        nnw = s.points['nnw']
        nne = s.points['nne']
        c   = s.points['center']

        s.subtiles['north'] = Tile(hex_in_south_facing_triangle(c, nne, nnw), height_bias=s.height)
        s.subtiles['south'] = Tile(hex_in_north_facing_triangle(c, sse, ssw), height_bias=s.height)
        s.subtiles['northeast'] = Tile(hex_in_north_facing_triangle(nne, e, c), height_bias=s.height)
        s.subtiles['northwest'] = Tile(hex_in_north_facing_triangle(nnw, c, w), height_bias=s.height)
        s.subtiles['southeast'] = Tile(hex_in_south_facing_triangle(sse, e, c), height_bias=s.height)
        s.subtiles['southwest'] = Tile(hex_in_south_facing_triangle(ssw, c, w), height_bias=s.height)
        s.subtiles['center'] = Tile(hex_in_center(e, sse, ssw, w, nnw, nne, c), height_bias=s.height)

        if not s.root:
            centerpoints = s.subtiles['center'].points
            width = centerpoints['e'][0] - centerpoints['w'][0]
            s.subtiles['eastcorner'] = Tile(shifted(centerpoints, x = width*1.5))
            s.subtiles['westcorner'] = Tile(shifted(centerpoints, x = -(width*1.5)))

        s.subdivided = True

    def buffers(s):
        vertices = []
        indices = []
        colors = []
        i = 0
        scale = 0.05
        for tile in s.tiles_at_bottom_level():
            e, sse, ssw, w, nnw, nne, c, _e, _sse, _ssw, _w, _nnw, _nne, _c = [i+n for n in range(14)]
            vertices.append(tile.points['e']      + (0,))
            vertices.append(tile.points['sse']    + (0,))
            vertices.append(tile.points['ssw']    + (0,))
            vertices.append(tile.points['w']      + (0,))
            vertices.append(tile.points['nnw']    + (0,))
            vertices.append(tile.points['nne']    + (0,))
            vertices.append(tile.points['center'] + (0,))

            vertices.append(tile.points['e']      + (tile.height*scale,))
            vertices.append(tile.points['sse']    + (tile.height*scale,))
            vertices.append(tile.points['ssw']    + (tile.height*scale,))
            vertices.append(tile.points['w']      + (tile.height*scale,))
            vertices.append(tile.points['nnw']    + (tile.height*scale,))
            vertices.append(tile.points['nne']    + (tile.height*scale,))
            vertices.append(tile.points['center'] + (tile.height*scale,))
            colors.extend([tile.color]*14)
            indices.extend([
                # Ground level.
                e, sse, c,
                sse, ssw, c,
                ssw, w, c,
                w, nnw, c,
                nnw, nne, c,
                nne, e, c,
                # Raised.
                _e, _sse, _c,
                _sse, _ssw, _c,
                _ssw, _w, _c,
                _w, _nnw, _c,
                _nnw, _nne, _c,
                _nne, _e, _c,
                # Walls.
                e, sse, _sse,
                e, _sse, _e,
                sse, ssw, _ssw,
                sse, _ssw, _sse,
                ssw, w, _w,
                ssw, _w, _ssw,
                w, nnw, _nnw,
                w, _nnw, _w,
                nnw, nne, _nne,
                nnw, _nne, _nnw,
                nne, e, _e,
                nne, _e, _nne,
            ])
            i += 14
        return vertices, indices, colors

    def flat_buffers(s):
        vertices = []
        indices = []
        colors = []
        i = 0
        for tile in s.tiles_at_bottom_level():
            e, sse, ssw, w, nnw, nne, c = [i+n for n in range(7)]
            vertices.append(tile.points['e']      + (0,))
            vertices.append(tile.points['sse']    + (0,))
            vertices.append(tile.points['ssw']    + (0,))
            vertices.append(tile.points['w']      + (0,))
            vertices.append(tile.points['nnw']    + (0,))
            vertices.append(tile.points['nne']    + (0,))
            vertices.append(tile.points['center'] + (0,))
            colors.extend([tile.color]*7)
            indices.extend([
                # Ground level.
                e, sse, c,
                sse, ssw, c,
                ssw, w, c,
                w, nnw, c,
                nnw, nne, c,
                nne, e, c,
            ])
            i += 7
        return vertices, indices, colors

    def tiles_at_bottom_level(s):
        if s.subdivided:
            for subtile in s.subtiles.values():
                for tile in subtile.tiles_at_bottom_level():
                    yield tile
        else:
            yield s

    def __contains__(s, point):
        assert len(point) == 2
        x, y = point
        e   = s.points['e']
        sse = s.points['sse']
        ssw = s.points['ssw']
        w   = s.points['w']
        nnw = s.points['nnw']
        nne = s.points['nne']
        c   = s.points['center']
        tests = [
            w[0] <= x <= e[0],
            sse[1] <= y <= nne[1],
        ]
        return all(tests)

    def lowest_tile_at_point(s, point):
        if point in s:
            if s.subdivided:
                for subtile in s.subtiles.values():
                    if point in subtile:
                        return subtile.lowest_tile_at_point(point)
            else:
                return s
        else:
            return None


def hex_in_north_facing_triangle(n, e, w):
    points = {
        'e':        thirdway(e, n),
        'sse':      thirdway(e, w),
        'ssw':      thirdway(w, e),
        'w':        thirdway(w, n),
        'nnw':      thirdway(n, w),
        'nne':      thirdway(n, e),
        'center':   centerpoint(n, e, w),
    }
    return points


def hex_in_south_facing_triangle(s, e, w):
    points = {
        'e':        thirdway(e, s),
        'sse':      thirdway(s, e),
        'ssw':      thirdway(s, w),
        'w':        thirdway(w, s),
        'nnw':      thirdway(w, e),
        'nne':      thirdway(e, w),
        'center':   centerpoint(s, e, w),
    }
    return points


def hex_in_center(e, sse, ssw, w, nnw, nne, c):
    points = {
        'e':        thirdway(c, e),
        'sse':      thirdway(c, sse),
        'ssw':      thirdway(c, ssw),
        'w':        thirdway(c, w),
        'nnw':      thirdway(c, nnw),
        'nne':      thirdway(c, nne),
        'center':   c,
    }
    return points


def shifted(points, x=0, y=0):
    new_points = {}
    for name, p in points.items():
        px, py = p
        new_points[name] = (px+x, py+y)
    return new_points


def hex_in_corner(e, c, sse, nne):
    # This assumes a regular hexagon with no stretch.
    # It also places the hex at the east corner.
    d = distance(e, c)
    s = d[0]/2
    points = {}
    points['center'] = e
    points['w']      = thirdway(e, c)
    points['nnw']    = thirdway(e, nne)
    points['ssw']    = thirdway(e, sse)
    points['e']      = (e[0] + s, e[1])
    points['nne']    = (points['nnw'][0] + s, points['nnw'][1])
    points['sse']    = (points['ssw'][0] + s, points['ssw'][1])
    return points


def thirdway(a, b):
    ax, ay = a
    bx, by = b
    return (ax*2 + bx) / 3, (ay*2 + by) / 3


def centerpoint(*points):
    n = len(points)
    x = sum(p[0] for p in points)
    y = sum(p[1] for p in points)
    return x/n, y/n


def distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax-bx), abs(ay-by)


def duplicate_tile_check(root):
    found = {}
    for tile in root.tiles_at_bottom_level():
        c = tile.points['center']
        if c in found.keys():
            return True
        found[c] = True
    return False
