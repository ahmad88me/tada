from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import optparse

import numpy as np

a = np.array([[1, 200], [1, 300], [4, 100], [2, 200]])

# -----------
# VARIABLES
# -----------
g_Width = 600
g_Height = 600

# -------------------------------
# Related to my drawing function
# -------------------------------
file_name = None
data_file_name = None
max_x = 1.0
min_x = 0.0
max_y = 1.0
min_y = 0.0

point_size = 10.0

# -------------------
# SCENE CONSTRUCTOR
# -------------------

def scenemodel():
    glRotate(90, 0., 0., 1.)
    #glutSolidTeapot(1.)
    draw_graph()


def export_to_image():
    global g_Width, g_Height
    from PIL import Image
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, g_Width, g_Height, GL_RGBA, GL_UNSIGNED_BYTE)
    # image = Image.fromstring("RGBA", (g_Width, g_Height), data)
    image = Image.frombytes("RGBA", (g_Width, g_Height), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    #image = image.transpose(Image.FLIP_LEFT_RIGHT)
    #image = image.transpose(Image.TRANSPOSE)
    #image.show()
    image.save('local_out.png', 'PNG')


def draw_point(min_x=0.0, max_x=1.0, min_y=0.0, max_y=1.0, x=0, y=0, color="#FF9900", alpha=0.5):
    c = []
    color_string = color.replace("#", "")
    for i in range(len(color_string) / 2):
        c.append(int(color_string[i * 2:i * 2 + 1], 16) / 15.0)
    glColor4f(c[0], c[1], c[2], alpha)
    # new_x = ((min_x*-1.0) + x) / (max_x - min_x)
    # new_y = ((min_y * -1.0) + y) / (max_y - min_y)
    new_x = (x - min_x)/ (max_x - min_x)  # get the percentage
    new_y = (y - min_y)/ (max_y - min_y)  # get the percentage
    new_x = new_x * 2 - 1
    new_y = new_y * 2 - 1
    glVertex3f(new_x, new_y, 1.0)


def draw_points():
    global file_name, max_x, max_y, min_x, min_y
    if file_name is None:
        file_name = 'points.in'
    f = open(file_name, 'r')
    glPointSize(point_size)
    glBegin(GL_POINTS)
    for line_num, line in enumerate(f.readlines()):
        # if True:
        try:
            # print "line: %s" % line
            x, y, color, alpha = line.split(',')
            x = float(x)
            y = float(y)
            alpha = float(alpha)
            draw_point(max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y, x=x, y=y, color=color, alpha=alpha)
        #else:
        except:
            print("line %d has invalid values" % line_num)
    glEnd()
    export_to_image()


def display():
    # print "DISPLAY"
    # Clear frame buffer and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Set up viewing transformation, looking down -Z axis
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    draw_points()
    # test()
    # Make sure changes appear onscreen
    glutSwapBuffers()


def reshape(width, height):
    global g_Width, g_Height
    g_Width = width
    g_Height = height
    glViewport(0, 0, g_Width, g_Height)


def keyboard(key, x, y):
    if key == 'q':
        exit(0)
    glutPostRedisplay()


if __name__ == "__main__":
    # global file_name, data_file_name, max_x, min_x, max_y, min_y, g_Width, g_Height, point_size
    # parser = optparse.OptionParser("usage: %prog input_file max_x min_x max_y min_y \
    # [--pointsize POINTSIZE --windowheight WINDOWHEIGHT --windowwidth WINDOWWIDTH ]  ")
    # parser.add_option('--windowheight', help="this is to set the height of the window in pixels")
    # parser.add_option('--windowwidth', help='this is to set the width of the window in pixels')
    # parser.add_option('--pointsize', help="this is to set the pointsize of a single point in pixels")
    # options, args = parser.parse_args()
    # print "args"
    # print args
    # print "options:"
    # print options
    # print "============"
    args = sys.argv
    if len(args) < 6:
        #print parser.print_help()
        print " file_name max_x min_x max_y min_y [WINDOWHEIGHT WINDOWWIDTH POINTSIZE]"
        exit(0)

    file_name = args[1]
    data_file_name = args[2]
    max_x = float(args[3])
    min_x = float(args[4])
    max_y = float(args[5])
    min_y = float(args[6])

    if len(args) > 7:
        g_Height = int(args[7])
    if len(args) > 8:
        g_Width = int(args[8])
    if len(args) > 9:
        point_size = float(args[9])


    # GLUT Window Initialization
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_ALPHA)  # zBuffer
    glutInitWindowSize(g_Width, g_Height)
    glutInitWindowPosition(0 + 4, g_Height / 4)
    glutCreateWindow("Scatter ")
    glEnable(GL_BLEND) # Enable blending.
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Set blending function.
    # Register callbacks
    # glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    # glutMouseFunc(mouse)
    # glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    # Turn the flow of control over to GLUT
    glutMainLoop()
