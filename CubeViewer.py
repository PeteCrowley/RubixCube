import math
import pygame
from Cube import Wireframe, Cube
from RubixCube import RubixCube


key_to_function = {
            pygame.K_LEFT: (lambda x: x.translate_all('x', -10)),
            pygame.K_RIGHT: (lambda x: x.translate_all('x', 10)),
            pygame.K_DOWN: (lambda x: x.translate_all('y', 10)),
            pygame.K_UP: (lambda x: x.translate_all('y', -10)),
            pygame.K_EQUALS: (lambda x: x.scale_all(1.25)),
            pygame.K_MINUS: (lambda x: x.scale_all(0.8)),
            pygame.K_z: (lambda x: x.rotate_all_z(0.3)),
            pygame.K_y: (lambda x: x.rotate_all_y(0.3)),
            pygame.K_x: (lambda x: x.rotate_all_x(0.3)),
            pygame.K_o: (lambda x: x.wireframes["Cube"].outputNodes()),
            pygame.K_0: (lambda x: x.wireframes["Cube"].rubix.rotate_clockwise(0)),
            pygame.K_1: (lambda x: x.wireframes["Cube"].rubix.rotate_clockwise(1)),
            pygame.K_2: (lambda x: x.wireframes["Cube"].rubix.rotate_clockwise(2)),
            pygame.K_3: (lambda x: x.wireframes["Cube"].rubix.rotate_clockwise(3)),
            pygame.K_4: (lambda x: x.wireframes["Cube"].rubix.rotate_clockwise(4)),
            pygame.K_5: (lambda x: x.wireframes["Cube"].rubix.rotate_clockwise(5)),
            # pygame.K_6: (lambda x: x.wireframes["Cube"].rubix.rotate_clockwise(6)),
            # pygame.K_7: (lambda x: x.wireframes["Cube"].rubix.rotate_clockwise(7)),
            pygame.K_s: (lambda x: x.wireframes["Cube"].rubix.scramble()),
            pygame.K_p: (lambda x: print(x.wireframes["Cube"].rubix))}

opp_key_to_function = {
            pygame.K_LEFT: (lambda x: x.translate_all('x', -10)),
            pygame.K_RIGHT: (lambda x: x.translate_all('x', 10)),
            pygame.K_DOWN: (lambda x: x.translate_all('y', 10)),
            pygame.K_UP: (lambda x: x.translate_all('y', -10)),
            pygame.K_EQUALS: (lambda x: x.scale_all(1.25)),
            pygame.K_MINUS: (lambda x: x.scale_all(0.8)),
            pygame.K_z: (lambda x: x.rotate_all_z(-0.3)),
            pygame.K_y: (lambda x: x.rotate_all_y(-0.3)),
            pygame.K_x: (lambda x: x.rotate_all_x(-0.3)),
            pygame.K_o: (lambda x: x.wireframes["Cube"].outputNodes()),
            pygame.K_0: (lambda x: x.wireframes["Cube"].rubix.rotate_counter_clockwise(0)),
            pygame.K_1: (lambda x: x.wireframes["Cube"].rubix.rotate_counter_clockwise(1)),
            pygame.K_2: (lambda x: x.wireframes["Cube"].rubix.rotate_counter_clockwise(2)),
            pygame.K_3: (lambda x: x.wireframes["Cube"].rubix.rotate_counter_clockwise(3)),
            pygame.K_4: (lambda x: x.wireframes["Cube"].rubix.rotate_counter_clockwise(4)),
            pygame.K_5: (lambda x: x.wireframes["Cube"].rubix.rotate_counter_clockwise(5)),
            # pygame.K_6: (lambda x: x.wireframes["Cube"].rubix.rotate_clockwise(6)),
            # pygame.K_7: (lambda x: x.wireframes["Cube"].rubix.rotate_clockwise(7)),
            pygame.K_s: (lambda x: x.wireframes["Cube"].rubix.scramble()),
            pygame.K_p: (lambda x: print(x.wireframes["Cube"].rubix))}


NUM_TO_COLOR = {1: (200, 0, 0), 2: (200, 200, 200), 3: (200, 100, 0), 4: (200, 200, 0),
                5: (0, 200, 0), 6: (0, 0, 200)}

FPS = 10
CLOCK = pygame.time.Clock()

class CubeViewer():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (10, 10, 50)
        self.wireframes = {}
        self.nodeColour = (255, 255, 255)
        self.edgeColour = (200, 200, 200)
        self.faceColor = (200, 0, 0)
        self.nodeRadius = 4
        self.displayFaces = True
        self.displayNodes = False
        self.displayEdges = False
        self.borders = True
        self.function_list = key_to_function

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """
        self.wireframes[name] = wireframe

    def run(self):
        """ Create a pygame screen until it is closed. """
        running = True
        while running:
            CLOCK.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.function_list:
                        self.function_list[event.key](self)
                    if event.key == pygame.K_c:
                        self.function_list = opp_key_to_function
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_c:
                        self.function_list = key_to_function

            self.display()
            pygame.display.flip()

    def display(self):
        """ Draw the wireframes on the screen. """
        self.screen.fill(self.background)
        if "Cube" in self.wireframes.keys():
            self.wireframes["Cube"].update_colors()
        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y),
                                       (edge.stop.x, edge.stop.y), 5)

            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)

            if self.displayFaces:
                for face in wireframe.faces:
                    if self.borders:
                        draw_styled_rect(self.screen, NUM_TO_COLOR[face.color], [(face.a.x, face.a.y), (face.b.x, face.b.y), (face.c.x, face.c.y), (face.d.x, face.d.y)])
                    else:
                        pygame.draw.polygon(self.screen, NUM_TO_COLOR[face.color], [(face.a.x, face.a.y), (face.b.x, face.b.y), (face.c.x, face.c.y), (face.d.x, face.d.y)])

    def translate_all(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """
        for wireframe in self.wireframes.values():
            wireframe.translate(axis, d)

    def scale_all(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """
        for wireframe in self.wireframes.values():
            wireframe.scale(scale)

    def rotate_all_z(self, radians):
        for wireframe in self.wireframes.values():
            wireframe.rotate_z(radians)

    def rotate_all_y(self, radians):
        for wireframe in self.wireframes.values():
            wireframe.rotate_y(radians)

    def rotate_all_x(self, radians):
        for wireframe in self.wireframes.values():
            wireframe.rotate_x(radians)

def draw_styled_rect(screen, color, points, bwidth = 3):
    pygame.draw.polygon(screen, pygame.Color("black"),
                        points)
    pygame.draw.polygon(screen, color, [(points[0][0]-bwidth, points[0][1]-bwidth), (points[1][0]-bwidth, points[1][1]-bwidth),
                                        (points[2][0]-bwidth, points[2][1]-bwidth), (points[3][0]-bwidth, points[3][1]-bwidth)])


if __name__ == '__main__':
    pv = CubeViewer(500, 600)
    rubix = RubixCube()
    # rubix.cube[3] = [[1, 2, 3],
    #              [6, 5, 1],
    #              [5, 3, 4]]
    # rubix.rotate_clockwise(1)
    # rubix.scramble()
    cube = Cube(rubix)

    # cube.outputNodes()
    # cube.outputEdges()
    pv.addWireframe("Cube", cube)
    pv.run()
