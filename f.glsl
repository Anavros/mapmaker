#version 120

varying vec3 fragment_color;

void main(void) {
    gl_FragColor = vec4(fragment_color, 1.0);
}
