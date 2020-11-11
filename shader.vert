#version 300 core

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 color;
out vec4 outColor;

void main(void){
    outColor = color;
    gl_Position = position;
}
