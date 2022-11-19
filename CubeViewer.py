import pygame
from Cube import Cube
from RubixCube import RubixCube
from Bot import random_move, WhiteCrossBot

notation = {"r", "l", "u", "d", "f", "b", "m", "e", "s"}

key_to_function = {
            pygame.K_LEFT: (lambda x: x.cube.translate('x', -10)),
            pygame.K_RIGHT: (lambda x: x.cube.translate('x', 10)),
            pygame.K_DOWN: (lambda x: x.cube.translate('y', 10)),
            pygame.K_UP: (lambda x: x.cube.translate('y', -10)),
            pygame.K_EQUALS: (lambda x: x.cube.scale(1.25)),
            pygame.K_MINUS: (lambda x: x.cube.scale(0.8)),
            pygame.K_q: (lambda x: x.cube.rubix.scramble()),
            pygame.K_p: (lambda x: print(x.cube))}


NUM_TO_COLOR = {1: (0, 0, 200), 2: (200, 0, 0), 3: (0, 200, 0), 4: (200, 100, 0),
                5: (200, 200, 200), 6: (200, 200, 0)}

FPS = 10
CLOCK = pygame.time.Clock()

bot = WhiteCrossBot()

class CubeViewer:
    def __init__(self, width, height, cube):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Rubix Cube')
        self.background = (10, 10, 50)
        self.cube: Cube = cube
        self.nodeColour = (255, 255, 255)
        self.edgeColour = (200, 200, 200)
        self.faceColor = (200, 0, 0)
        self.nodeRadius = 4
        self.displayFaces = True
        self.displayNodes = False
        self.displayEdges = False
        self.borders = True

    def run(self):
        """ Create a pygame screen until it is closed. """
        running = True
        while running:
            CLOCK.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.unicode in notation:
                        self.cube.make_move(event.unicode, not pygame.key.get_pressed()[pygame.K_c])
                    elif event.unicode == "x" or event.unicode == "y" or event.unicode == "z":
                        if event.unicode == "x":
                            self.cube.rotate_cube_x(not pygame.key.get_pressed()[pygame.K_c])
                        elif event.unicode == "y":
                            self.cube.rotate_cube_y(not pygame.key.get_pressed()[pygame.K_c])
                        elif event.unicode == "z":
                            self.cube.rotate_cube_z(not pygame.key.get_pressed()[pygame.K_c])
                    elif event.unicode == "1":
                        self.cube.rubix.step(bot.white_cross_move(self.cube.rubix))
                    elif event.key in key_to_function:
                        key_to_function[event.key](self)

            self.display()
            pygame.display.flip()

    def display(self):
        """ Draw the wireframes on the screen. """
        self.screen.fill(self.background)
        self.cube.update_colors()
        if self.displayEdges:
            for edge in self.cube.edges:
                pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y),
                                   (edge.stop.x, edge.stop.y), 5)

        if self.displayNodes:
            for node in self.cube.nodes:
                pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)

        if self.displayFaces:
            for face in self.cube.faces:
                if self.borders:
                    draw_styled_rect(self.screen, NUM_TO_COLOR[face.color], [(face.a.x, face.a.y), (face.b.x, face.b.y), (face.c.x, face.c.y), (face.d.x, face.d.y)])
                else:
                    pygame.draw.polygon(self.screen, NUM_TO_COLOR[face.color], [(face.a.x, face.a.y), (face.b.x, face.b.y), (face.c.x, face.c.y), (face.d.x, face.d.y)])


def draw_styled_rect(screen, color, points, bwidth=3):
    pygame.draw.polygon(screen, pygame.Color("black"),
                        points)
    pygame.draw.polygon(screen, color, [(points[0][0]-bwidth, points[0][1]-bwidth), (points[1][0]-bwidth, points[1][1]-bwidth),
                                        (points[2][0]-bwidth, points[2][1]-bwidth), (points[3][0]-bwidth, points[3][1]-bwidth)])


if __name__ == '__main__':

    # rubix.cube[3] = [[1, 2, 3],
    #              [6, 5, 1],
    #              [5, 3, 4]]
    # rubix.rotate_clockwise(1)
    # rubix.scramble()
    pv = CubeViewer(500, 600, Cube(RubixCube()))

    # cube.outputNodes()
    # cube.outputEdges()

    pv.run()
