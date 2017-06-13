
import rocket
from vispy.gloo import IndexBuffer
import math


program = rocket.program('shaders/v.glsl', 'shaders/f.glsl')


colormap = {
    1 : (0.2, 0.4, 0.6),
    2 : (0.8, 0.6, 0.4),
    3 : (0.7, 0.5, 0.3),
    4 : (0.6, 0.4, 0.2),
    5 : (0.5, 0.3, 0.1),
}


def buffers(world, highlights):
    vertices = []
    indices = []
    colors = []
    i = 0

    for tile in world.tiles.values():
        size = world.tile_size
        width = size * 2
        height = math.sqrt(3) / 2 * width
        ver = height / 2
        hor = size
        half = hor/2

        # Variable prefixes:
        # i = index
        # v = vertex
        # g = ground vertex (z=0)
        # j = ground index
        ic, ie, iw, ine, inw, ise, isw = [i + n for n in range(7)]
        jc, je, jw, jne, jnw, jse, jsw = [i + n + 7 for n in range(7)]

        x, y = world.cartesian_center(tile.cubal())
        z = tile.height * world.spacing()
        vc =  (x, y, z)
        ve =  (x+hor, y, z)
        vw =  (x-hor, y, z)
        vne = (x+half, y+ver, z)
        vnw = (x-half, y+ver, z)
        vse = (x+half, y-ver, z)
        vsw = (x-half, y-ver, z)
        gc =  (x, y, 0)
        ge =  (x+hor, y, 0)
        gw =  (x-hor, y, 0)
        gne = (x+half, y+ver, 0)
        gnw = (x-half, y+ver, 0)
        gse = (x+half, y-ver, 0)
        gsw = (x-half, y-ver, 0)

        vertices.extend([
            vc, ve, vw, vne, vnw, vse, vsw,
            gc, ge, gw, gne, gnw, gse, gsw,
        ])

        indices.extend([
            # Top Face
            ic, ie, ine,
            ic, ine, inw,
            ic, inw, iw,
            ic, iw, isw,
            ic, isw, ise,
            ic, ise, ie,

            # Bottom Face
            jc, je, jne,
            jc, jne, jnw,
            jc, jnw, jw,
            jc, jw, jsw,
            jc, jsw, jse,
            jc, jse, je,

            # Walls
            ie, ine, jne,
            ie, jne, je,
            ine, inw, jnw,
            ine, jnw, jne,
            inw, iw, jw,
            inw, jw, jnw,
            iw, isw, jsw,
            iw, jsw, jw,
            isw, ise, jse,
            isw, jse, jsw,
            ise, ie, je,
            ise, je, jse,
        ])

        r, g, b = colormap[tile.height]
        if tile.cubal() in highlights:
            colors.extend([(r+0.1, g+0.1, b+0.1)]*7)
            colors.extend([(r+0.3, g+0.3, b+0.3)]*7)
        else:
            colors.extend([(r, g, b)]*7)
            colors.extend([(r-0.2, g-0.2, b-0.2)]*7)
        i += 14
    return vertices, indices, colors


def render(mesh, view):
    program['xyz'] = mesh.vertices
    program['color'] = mesh.colors
    program['model'] = mesh.transform
    program['view'] = view.transform
    program['projection'] = view.proj
    program.draw('triangles', IndexBuffer(mesh.indices))
