
import rocket
from vispy.gloo import IndexBuffer
import math


program = rocket.program('v.glsl', 'f.glsl')


colormap = {
    1 : (0.2, 0.4, 0.6),
    2 : (0.8, 0.6, 0.4),
    3 : (0.7, 0.5, 0.3),
    4 : (0.6, 0.4, 0.2),
    5 : (0.5, 0.3, 0.1),
}


def buffers(tilemap, size, resolution_level, highlights):
    vertices = []
    indices = []
    colors = []
    i = 0

    if resolution_level > 0:
        spacing = size / (3*resolution_level)
    else:
        spacing = size

    for tile in tilemap.values():
        width = size * 2
        height = math.sqrt(3) / 2 * width
        ver = height / 2
        hor = width / 2
        half = hor/2

        # Variable prefixes:
        # i = index
        # v = vertex
        # g = ground vertex (z=0)
        # j = ground index
        ic, ie, iw, ine, inw, ise, isw = [i + n for n in range(7)]
        jc, je, jw, jne, jnw, jse, jsw = [i + n + 7 for n in range(7)]

        vc = tile.pixel_spaced(spacing)
        ve =  (vc[0]+hor, vc[1], vc[2])
        vw =  (vc[0]-hor, vc[1], vc[2])
        vne = (vc[0]+half, vc[1]+ver, vc[2])
        vnw = (vc[0]-half, vc[1]+ver, vc[2])
        vse = (vc[0]+half, vc[1]-ver, vc[2])
        vsw = (vc[0]-half, vc[1]-ver, vc[2])

        gc =  (vc[0], vc[1], 0)
        ge =  (vc[0]+hor, vc[1], 0)
        gw =  (vc[0]-hor, vc[1], 0)
        gne = (vc[0]+half, vc[1]+ver, 0)
        gnw = (vc[0]-half, vc[1]+ver, 0)
        gse = (vc[0]+half, vc[1]-ver, 0)
        gsw = (vc[0]-half, vc[1]-ver, 0)

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
