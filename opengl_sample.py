import glfw
from OpenGL.GL import *

def render():
    glClearColor(0, 0, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

def main():
    if not glfw.init():
        raise RuntimeError('Could not initialize GLFW3')

    window = glfw.create_window(320, 240, 'Hello, World!!', None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError('Could not create an window')

    glfw.make_context_current(window)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    while not glfw.window_should_close(window):
        render()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == '__main__':
    main()
