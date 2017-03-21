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
    #glPopMatrix()
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, g_Width, g_Height, GL_RGBA, GL_UNSIGNED_BYTE)
    # image = Image.fromstring("RGBA", (g_Width, g_Height), data)
    image = Image.frombytes("RGBA", (g_Width, g_Height), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    #image = image.transpose(Image.FLIP_LEFT_RIGHT)
    #image = image.transpose(Image.TRANSPOSE)
    #image.show()
    image.save('local_out.png', 'PNG')
    #image.save('/Users/aalobaid/workspaces/Pyworkspace/tada/tadacode/local_out.png', 'PNG')


def draw_graph():

    glPointSize(50.0)
    glBegin(GL_POINTS)  # starts drawing of points
    glColor4f(0.0, 0.0, 1.0, 0.5)
    glVertex3f(1.0, 1.0, 0.0)  # upper-right corner
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)  # lower-left corner
    glEnd()  # end drawing of points
    global a
    for aa in a:
        #draw_point(width=g_Width, height=g_Height, x=aa[0],y=aa[1], color="#abd231", alpha=0.5)
        draw_point(min_x=0.0, max_x=5.0, min_y=0.0, max_y=400.0, x=aa[0], y=aa[1], color="#abd231", alpha=0.5)


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


# def draw_point(width=1.0, height=1.0, x=0, y=0, color="#FF9900", alpha=0.5):
#     global g_Width, g_Height
#     c = []
#     color_string = color.replace("#", "")
#     for i in range(len(color_string)/2):
#         c.append(int(color_string[i*2:i*2+1], 16)/ 15.0)
#     glPointSize(10.0)
#     glBegin(GL_POINTS)
#     glColor4f(c[0], c[1], c[2], alpha)
#     glVertex3f(x*1.0/width, y*1.0/height, 1.0)
#     glEnd()


# --------
# VIEWER
# --------

def printHelp():
    print """\n\n
         -------------------------------------------------------------------\n
          q Key                - exit the program\n
         -------------------------------------------------------------------\n
         \n"""


def draw_points():
    global file_name, max_x, max_y, min_x, min_y
    if file_name is None:
        file_name = 'points.in'
    f = open(file_name, 'r')
    glPointSize(point_size)
    #glLineWidth(10.0)
    glBegin(GL_POINTS)
    #glBegin(GL_LINES)
    #glBegin(GL_TRIANGLES)
    #glBegin(GL_POLYGON)
    #glBegin(GL_QUADS)
    prev_x, prev_y, prev_color, prev_alpha = 0,0,"#FFFFFF","#FFFFFF"
    for line_num, line in enumerate(f.readlines()):
        #if True:
        try:
            #print "line: %s" % line
            x, y, color, alpha = line.split(',')
            x = float(x)
            y = float(y)
            alpha = float(alpha)
            # print "line is parsed"
            # if line_num % 2 == 0:
            #     print "even: line num %d" % line_num
            #     prev_x, prev_y, prev_color, prev_alpha = x, y, color, alpha
            # else:
            #     print "odd: line num %d" % line_num
            #     glBegin(GL_LINES)
            #     #glBegin(GL_POINTS)
            #     print "prev x: %f, prev y: %f" % (prev_x, prev_y)
            #     print "prev x: %f, prev y: %f" % (x, y)
            #     draw_point_cont(max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y, x=prev_x, y=prev_y, color=prev_color, alpha=prev_alpha)
            #     draw_point_cont(max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y, x=x, y=y, color=color, alpha=alpha)
            #     glEnd()
            draw_point(max_x=max_x, max_y=max_y, min_x=min_x, min_y=min_y, x=x, y=y, color=color, alpha=alpha)
        #else:
        except:
            print("line %d has invalid values" % line_num)
    glEnd()
    export_to_image()



def display():
    print "DISPLAY"
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
    global zTr, yTr, xTr
    # if (key == 'r'): resetView()
    if key == 'q':
        exit(0)
    glutPostRedisplay()


if __name__ == "__main__":
    global file_name, max_x, min_x, max_y, min_y, g_Width, g_Height, point_size
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
    #file_name, max_x, min_x, max_y, min_y = args[1:]
    file_name = args[1]
    max_x = float(args[2])
    min_x = float(args[3])
    max_y = float(args[4])
    min_y = float(args[5])

    if len(args) > 6:
        g_Height = int(args[6])
    if len(args) > 7:
        g_Width = int(args[7])
    if len(args) > 8:
        point_size = float(args[8])

    # if options.pointsize:
    #     point_size = options.pointsize
    # if options.windowheight:
    #     g_Height = options.windowheight
    # if options.windowwidth:
    #     g_Width = options.windowwidth

    # GLUT Window Initialization
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_ALPHA)  # zBuffer
    glutInitWindowSize(g_Width, g_Height)
    glutInitWindowPosition(0 + 4, g_Height / 4)
    glutCreateWindow("Scatter ")
    # Initialize OpenGL graphics state
    # init()
    glEnable(GL_BLEND) # Enable blending.
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Set blending function.
    # Register callbacks
    # glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    # glutMouseFunc(mouse)
    # glutMotionFunc(motion)
    glutKeyboardFunc(keyboard)
    printHelp()
    # Turn the flow of control over to GLUT
    glutMainLoop()



# ------
# MAIN
# ------
# if __name__ == "__main__":
#     # GLUT Window Initialization
#     glutInit()
#     glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_ALPHA)  # zBuffer
#     glutInitWindowSize(g_Width, g_Height)
#     glutInitWindowPosition(0 + 4, g_Height / 4)
#     glutCreateWindow("Scatter ")
#     # Initialize OpenGL graphics state
#     #init()
#     glEnable(GL_BLEND) # Enable blending.
#     glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # Set blending function.
#     # Register callbacks
#     # glutReshapeFunc(reshape)
#     glutDisplayFunc(display)
#     #glutMouseFunc(mouse)
#     #glutMotionFunc(motion)
#     glutKeyboardFunc(keyboard)
#     printHelp()
#     # Turn the flow of control over to GLUT
#     glutMainLoop()
