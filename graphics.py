
import rocket
from vispy.gloo import IndexBuffer


program = rocket.program('v.glsl', 'f.glsl')


def render(mesh, view):
    program['xyz'] = mesh.vertices
    program['color'] = mesh.colors
    program['model'] = mesh.transform
    program['view'] = view.transform
    program['projection'] = view.proj
    #program.draw('points')
    program.draw('triangles', IndexBuffer(mesh.indices))
