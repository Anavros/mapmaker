#version 120

attribute vec2 xy;
attribute vec3 color;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
varying vec3 fragment_color;

void main(void) {
    gl_Position = projection * view * model * vec4(xy, 0.0, 1.0);
    gl_PointSize = 10.0;
    fragment_color = color;
}
