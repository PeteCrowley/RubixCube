import math
import pygame
import random
from RubixCube import RubixCube

X_ROT_VAL = -0.3
Y_ROT_VAL = 0.4


class Node:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def is_connected(self, other, distance):
        if abs(self.x + self.y + self.z - other.x - other.y - other.z) == distance:
            equal = 0
            if self.x == other.x:
                equal += 1
            if self.y == other.y:
                equal += 1
            if self.z == other.z:
                equal += 1
            return equal == 2


class Edge:
    def __init__(self, start: Node, stop: Node):
        self.start = start
        self.stop = stop


class Rectangle:
    def __init__(self, a: Node, b: Node, c: Node, d: Node, col: int):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.color = col

    def mean_z(self):
        return (self.a.z + self.b.z + self.c.z + self.d.z) / 4

    def mean_x(self):
        return (self.a.x + self.b.x + self.c.x + self.d.x) / 4

    def mean_y(self):
        return (self.a.y + self.b.y + self.c.y + self.d.y) / 4


class Wireframe:
    def __init__(self):
        self.nodes: [Node] = []
        self.edges: [Edge] = []

    def add_nodes(self, node_list: [(int, int, int)]):
        for (x, y, z) in node_list:
            self.nodes.append(Node(x, y, z))

    def add_edges(self, edge_list):
        for (start, stop) in edge_list:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop]))

    def outputNodes(self):
        print("\n --- Nodes --- ")
        for i, node in enumerate(self.nodes):
            print(" %d: (%.2f, %.2f, %.2f)" % (i+1, node.x, node.y, node.z))

    def outputEdges(self):
        print("\n --- Edges --- ")
        for i, edge in enumerate(self.edges):
            print(" %d: (%.2f, %.2f, %.2f)" % (i+1, edge.start.x, edge.start.y, edge.start.z), end="")
            print("to (%.2f, %.2f, %.2f)" % (edge.stop.x, edge.stop.y, edge.stop.z))


    def translate(self, axis, d):
        """ Translate each node of a wireframe by d along a given axis. """

        if axis in ['x', 'y', 'z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node, axis) + d)

    def find_center(self):
        """ Find the center of the wireframe. """
        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes
        return (meanX, meanY, meanZ)

    def scale(self, scale):
        center = self.find_center()
        for node in self.nodes:
            node.x = center[0] + scale * (node.x - center[0])
            node.y = center[1] + scale * (node.y - center[1])
            node.z = center[2] + scale * (node.z - center[2])

    def rotate_z(self, radians):
        center = self.find_center()
        for node in self.nodes:
            x = node.x - center[0]
            y = node.y - center[1]
            d = math.hypot(y, x)
            theta = math.atan2(y, x) + radians
            node.x = center[0] + d * math.cos(theta)
            node.y = center[1] + d * math.sin(theta)

    def rotate_y(self, radians):
        center = self.find_center()
        for node in self.nodes:
            x = node.x - center[0]
            z = node.z - center[2]
            d = math.hypot(x, z)
            theta = math.atan2(z, x) + radians
            node.x = center[0] + d * math.cos(theta)
            node.z = center[2] + d * math.sin(theta)

    def rotate_x(self, radians):
        center = self.find_center()
        for node in self.nodes:
            y = node.y - center[1]
            z = node.z - center[2]
            d = math.hypot(y, z)
            theta = math.atan2(z, y) + radians
            node.y = center[1] + d * math.cos(theta)
            node.z = center[2] + d * math.sin(theta)


class Cube(Wireframe):
    def __init__(self, rubix_cube: RubixCube):
        super().__init__()
        self.rubix = rubix_cube
        self.graphic_cube = []

        self.faces = []
        self.construct()
        self.translate("x", 250)
        self.translate("y", 300)
        self.scale(50)
        self.rotate_y(Y_ROT_VAL)
        self.rotate_x(X_ROT_VAL)

    def construct(self):
        self.graphic_cube = []

        # face = 1
        x = 0
        rects: list[list[Rectangle]] = [[], [], []]
        for z in range(0, 3):
            for y in range(0, 3):
                rects[z].append(Rectangle(Node(x, y, z), Node(x, y, z+1), Node(x, y+1, z+1), Node(x, y+1, z),
                                          self.rubix.cube[0][y][z]))
        self.graphic_cube.append(rects)
        # face = 2
        y = 3
        rects: list[list[Rectangle]] = [[], [], []]
        for z in range(0, 3):
            for x in range(0, 3):
                rects[z].append(
                    Rectangle(Node(x, y, z), Node(x+1, y, z), Node(x+1, y, z + 1), Node(x, y, z+1),
                              self.rubix.cube[1][z][x]))
        self.graphic_cube.append(rects)
        # face = 3
        x = 3
        rects: list[list[Rectangle]] = [[], [], []]
        for z in range(0, 3):
            for y in range(1, 4).__reversed__():
                rects[z].append(Rectangle(Node(x, y, z), Node(x, y, z + 1), Node(x, y - 1, z + 1), Node(x, y - 1, z),
                                          self.rubix.cube[2][z][3-y]))
        self.graphic_cube.append(rects)
        # face = 4
        y = 0
        rects: list[list[Rectangle]] = [[], [], []]
        for z in range(0, 3):
            for x in range(1, 4).__reversed__():
                rects[z].append(
                    Rectangle(Node(x, y, z), Node(x - 1, y, z), Node(x - 1, y, z + 1), Node(x, y, z + 1),
                              self.rubix.cube[3][z][3-x]))
        self.graphic_cube.append(rects)
        # face = 5
        z = 0
        rects: list[list[Rectangle]] = [[], [], []]
        for y in range(0, 3):
            for x in range(0, 3):
                rects[y].append(
                    Rectangle(Node(x, y, z), Node(x + 1, y, z), Node(x + 1, y + 1, z), Node(x, y + 1, z),
                              self.rubix.cube[4][y][x]))
        self.graphic_cube.append(rects)
        # face = 6
        z = 3
        rects: list[list[Rectangle]] = [[], [], []]
        for y in range(1, 4).__reversed__():
            for x in range(0, 3):
                rects[3-y].append(
                    Rectangle(Node(x, y, z), Node(x + 1, y, z), Node(x + 1, y - 1, z), Node(x, y - 1, z),
                              self.rubix.cube[5][3-y][x]))
        self.graphic_cube.append(rects)
        for side in self.graphic_cube:
            for row in side:
                for square in row:
                    self.faces.append(square)
                    self.nodes.extend([square.a, square.b, square.c, square.d])
        self.update_colors()

    def update_colors(self):
        for f in range(len(self.graphic_cube)):
            for x in range(len(self.graphic_cube[f])):
                for y in range(len(self.graphic_cube[f][x])):
                    self.graphic_cube[f][x][y].color = self.rubix.cube[f][x][y]

    def add_faces(self, face_list: [(int, int, int, int)]):
        col = 0
        for (a, b, c, d) in face_list:
            self.faces.append(Rectangle(self.nodes[a], self.nodes[b], self.nodes[c], self.nodes[d], col))
            col += 1

    def rotate_x(self, radians):
        super().rotate_x(radians)
        self.sort_faces()

    def rotate_y(self, radians):
        super().rotate_y(radians)
        self.sort_faces()

    def sort_faces(self):
        self.faces = sorted(self.faces, key=key_z)

    def get_face_by_location(self, loc: str) -> int:
        target_square = None
        if loc == "r":
            target_square = max(self.faces, key=key_x)
        elif loc == "l":
            target_square = target_square = min(self.faces, key=key_x)
        elif loc == "f":
            target_square = target_square = max(self.faces, key=key_z)
        elif loc == "b":
            target_square = target_square = min(self.faces, key=key_z)
        elif loc == "d":
            target_square = target_square = max(self.faces, key=key_y)
        elif loc == "u":
            target_square = target_square = min(self.faces, key=key_y)
        face = 0
        for f in range(len(self.graphic_cube)):
            for row in self.graphic_cube[f]:
                for square in row:
                    if square is target_square:
                        face = f
        return face

    def rotate_cube_y(self, clockwise: bool):
        self.rotate_x(-X_ROT_VAL)
        if clockwise:
            self.rotate_y(math.pi / 2)
        else:
            self.rotate_y(-math.pi / 2)
        self.rotate_x(X_ROT_VAL)

    def rotate_cube_x(self, clockwise: bool):
        self.rotate_x(-X_ROT_VAL)
        self.rotate_y(-Y_ROT_VAL)
        if clockwise:
            self.rotate_x(math.pi/2)
        else:
            self.rotate_x(-math.pi/2)
        self.rotate_y(Y_ROT_VAL)
        self.rotate_x(X_ROT_VAL)

    def rotate_cube_z(self, clockwise: bool):
        self.rotate_x(-X_ROT_VAL)
        self.rotate_y(-Y_ROT_VAL)
        if clockwise:
            self.rotate_z(math.pi / 2)
        else:
            self.rotate_z(-math.pi / 2)
        self.rotate_y(Y_ROT_VAL)
        self.rotate_x(X_ROT_VAL)

    def make_move(self, notation: str, clockwise: bool):
        if notation not in ("m", "e", "s"):
            if clockwise:
                self.rubix.rotate_clockwise(self.get_face_by_location(notation))
            else:
                self.rubix.rotate_counter_clockwise(self.get_face_by_location(notation))
        else:
            front_face = self.get_face_by_location("f")
            top_face = self.get_face_by_location("u")
            face_num = None
            if notation == "m":
                if front_face == 0 or front_face == 2:
                    if top_face == 1 or top_face == 3:
                        face_num = 7
                    elif top_face == 4 or top_face == 5:
                        face_num = 8
                    if top_face == 1 or top_face == 5:
                        if front_face == 0:
                            clockwise = not clockwise
                    elif front_face == 2:
                        clockwise = not clockwise
                elif front_face == 1 or front_face == 3:
                    if top_face == 0 or top_face == 2:
                        face_num = 7
                    elif top_face == 4 or top_face == 5:
                        face_num = 6
                    if top_face == 2 or top_face == 4:
                        if front_face == 1:
                            clockwise = not clockwise
                    elif front_face == 3:
                        clockwise = not clockwise
                elif front_face == 4 or front_face == 5:
                    if top_face == 0 or top_face == 2:
                        face_num = 8
                    elif top_face == 1 or top_face == 3:
                        face_num = 6
                    if top_face == 2 or top_face == 1:
                        if front_face == 5:
                            clockwise = not clockwise
                    elif front_face == 4:
                        clockwise = not clockwise
            if notation == "e":
                if front_face == 0 or front_face == 2:
                    if top_face == 1 or top_face == 3:
                        face_num = 8
                    elif top_face == 4 or top_face == 5:
                        face_num = 7
                    if top_face == 4 or top_face == 1:
                        clockwise = not clockwise
                elif front_face == 1 or front_face == 3:
                    if top_face == 0 or top_face == 2:
                        face_num = 6
                    elif top_face == 4 or top_face == 5:
                        face_num = 7
                    if top_face == 0 or top_face == 4:
                        clockwise = not clockwise
                elif front_face == 4 or front_face == 5:
                    if top_face == 0 or top_face == 2:
                        face_num = 6
                    elif top_face == 1 or top_face == 3:
                        face_num = 8
                    if top_face == 0 or top_face == 1:
                        clockwise = not clockwise
            if notation == "s":
                if front_face == 0 or front_face == 2:
                    face_num = 6
                    if front_face == 2:
                        clockwise = not clockwise
                elif front_face == 1 or front_face == 3:
                    face_num = 8
                    if front_face == 3:
                        clockwise = not clockwise
                elif front_face == 4 or front_face == 5:
                    face_num = 7
                    if front_face == 5:
                        clockwise = not clockwise
            if clockwise:
                self.rubix.rotate_clockwise(face_num)
            else:
                self.rubix.rotate_counter_clockwise(face_num)


def key_z(rec: Rectangle):
    return rec.mean_z()


def key_y(rec: Rectangle):
    return rec.mean_y()


def key_x(rec: Rectangle):
    return rec.mean_x()


if __name__ == "__main__":
    cube_nodes = [(x, y, z) for x in (0, 3) for y in (0, 3) for z in (0, 3)]
    cube_edges = [(n, n + 4) for n in range(0, 4)]
    cube_edges.extend([(n, n + 1) for n in range(0, 8, 2)])
    cube_edges.extend([(n, n + 2) for n in (0, 1, 4, 5)])
    cube_edges.extend([])
    frame = Wireframe()
    frame.add_nodes(cube_nodes)
    frame.add_edges(cube_edges)
    frame.outputNodes()
    frame.outputEdges()


