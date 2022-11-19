import random
from copy import deepcopy


class RubixCube:
    def __init__(self, length: int = 3):
        self.length = length
        self.cube = [[], [], [], [], [], []]
        num = 1
        for face in self.cube:
            for r in range(self.length):
                face.append([num]*self.length)
            num += 1


    def rotate_counter_clockwise(self, face: int):
        # Consider all squares one by one
        for i in range(3):
            self.rotate_clockwise(face)

    def rotate_clockwise(self, face: int):
        if face < 6:
            mat = self.cube[face]
            for x in range(0, int(self.length / 2)):
                # Consider elements in group
                # of 4 in current square
                for y in range(x, self.length - x - 1):
                    # store current cell in temp variable
                    temp = mat[x][y]
                    # move values from right to top
                    mat[x][y] = mat[y][self.length - 1 - x]
                    # move values from bottom to right
                    mat[y][self.length - 1 - x] = mat[self.length - 1 - x][self.length - 1 - y]
                    # move values from left to bottom
                    mat[self.length - 1 - x][self.length - 1 - y] = mat[self.length - 1 - y][x]
                    # assign temp to left
                    mat[self.length - 1 - y][x] = temp

        """
        if 0: 4 -> 1 -> 5 -> 3 -> 4
        if 1: 2 -> 5 -> 0 -> 4 -> 2
        if 2: 3 -> 5 -> 1 -> 4 -> 3
        if 3: 2 -> 5 -> 0 -> 4 -> 2
        if 4: 0 -> 1 -> 2 -> 3 -> 0
        """
        if face == 0:
            temp = [self.cube[4][i][0] for i in range(self.length)]
            for i in range(self.length):
                self.cube[4][i][0] = self.cube[1][i][0]
                self.cube[1][i][0] = self.cube[5][i][0]
                self.cube[5][i][0] = self.cube[3][self.length - 1 - i][2]
                self.cube[3][self.length - 1 - i][2] = temp[i]
        elif face == 1:
            temp = [self.cube[4][self.length-1][i] for i in range(self.length)]
            for i in range(self.length):
                self.cube[4][self.length-1][i] = self.cube[2][i][0]
                self.cube[2][i][0] = self.cube[5][0][self.length - 1 - i]
                self.cube[5][0][self.length - 1 - i] = self.cube[0][self.length - 1 - i][self.length - 1]
                self.cube[0][self.length - 1 - i][self.length - 1] = temp[i]
        elif face == 2:
            temp = [self.cube[5][i][2] for i in range(self.length)]
            for i in range(self.length):
                self.cube[5][i][2] = self.cube[1][i][2]
                self.cube[1][i][2] = self.cube[4][i][2]
                self.cube[4][i][2] = self.cube[3][self.length - 1 - i][0]
                self.cube[3][self.length - 1 - i][0] = temp[i]
        elif face == 3:
            temp = [self.cube[4][0][i] for i in range(self.length)]
            for i in range(self.length):
                self.cube[4][0][i] = self.cube[0][self.length - 1 - i][0]
                self.cube[0][self.length - 1 - i][0] = self.cube[5][self.length-1][self.length - 1 - i]
                self.cube[5][self.length-1][self.length - 1 - i] = self.cube[2][i][self.length-1]
                self.cube[2][i][self.length-1] = temp[i]
        elif face == 4:
            temp = [self.cube[0][0][i] for i in range(self.length)]
            for i in range(self.length):
                self.cube[0][0][i] = self.cube[3][0][i]
                self.cube[3][0][i] = self.cube[2][0][i]
                self.cube[2][0][i] = self.cube[1][0][i]
                self.cube[1][0][i] = temp[i]
        elif face == 5:
            temp = [self.cube[0][self.length-1][i] for i in range(self.length)]
            for i in range(self.length):
                self.cube[0][self.length-1][i] = self.cube[1][self.length-1][i]
                self.cube[1][self.length-1][i] = self.cube[2][self.length-1][i]
                self.cube[2][self.length-1][i] = self.cube[3][self.length-1][i]
                self.cube[3][self.length-1][i] = temp[i]
        elif face == 6:
            temp = [self.cube[4][i][1] for i in range(self.length)]
            for i in range(self.length):
                self.cube[4][i][1] = self.cube[1][i][1]
                self.cube[1][i][1] = self.cube[5][i][1]
                self.cube[5][i][1] = self.cube[3][self.length - 1 - i][1]
                self.cube[3][self.length - 1 - i][1] = temp[i]
        elif face == 7:
            temp = [self.cube[0][1][i] for i in range(self.length)]
            for i in range(self.length):
                self.cube[0][1][i] = self.cube[3][1][i]
                self.cube[3][1][i] = self.cube[2][1][i]
                self.cube[2][1][i] = self.cube[1][1][i]
                self.cube[1][1][i] = temp[i]
        elif face == 8:
            temp = [self.cube[4][1][i] for i in range(self.length)]
            for i in range(self.length):
                self.cube[4][1][i] = self.cube[2][i][1]
                self.cube[2][i][1] = self.cube[5][1][self.length - 1 - i]
                self.cube[5][1][self.length - 1 - i] = self.cube[0][self.length - 1 - i][1]
                self.cube[0][self.length - 1 - i][1] = temp[i]

    def __str__(self) -> str:
        string = ""
        for i in range(self.length):
            string += " " * (self.length + 1)
            for num in self.cube[4][i]:
                string += str(num)
            string += "\n"
        for i in range(self.length):
            for face in range(4):
                for num in self.cube[face][i]:
                    string += str(num)
                string += " "
            string += "\n"
        for i in range(self.length):
            string += " " * (self.length + 1)
            for num in self.cube[5][i]:
                string += str(num)
            string += "\n"
        return string.rstrip()

    def is_solved(self) -> bool:
        for face in self.cube:
            num = face[0][0]
            for row in face:
                for n in row:
                    if n != num:
                        return False
        return True

    def scramble(self):
        for i in range(40):
            is_clock = random.choice([True, False])
            face = random.randint(0, 6)
            if is_clock:
                self.rotate_clockwise(face)
            else:
                self.rotate_counter_clockwise(face)

    def next_states(self) -> []:
        next_cubes = []
        for i in range(9):
            new_cube = deepcopy(self)
            new_cube.rotate_clockwise(i)
            next_cubes.append(new_cube)
            new_cube = deepcopy(self)
            new_cube.rotate_counter_clockwise(i)
            next_cubes.append(new_cube)
        return next_cubes

    def step(self, new_cube):
        self.cube = deepcopy(new_cube.cube)


if __name__ == "__main__":
    c = RubixCube()
    c.cube[0] = [[1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]]
    # c.cube[4] = [[1, 2, 3],
    #             [4, 5, 6],
    #             [7, 8, 9]]
    # c.cube[2] = [[1, 2, 3],
    #              [4, 5, 6],
    #              [7, 8, 9]]
    # c.cube[3] = [[1, 2, 3],
    #              [4, 5, 6],
    #              [7, 8, 9]]
    # c.cube[4] = [[1, 2, 3],
    #              [4, 5, 6],
    #              [7, 8, 9]]
    # c.cube[5] = [[1, 2, 3],
    #              [4, 5, 6],
    #              [7, 8, 9]]



    print(c)
    print()
    c.rotate_clockwise(6)
    # c.scramble()
    # print(c.is_solved())
    # for x in range(4):
    #     # c.rotate_middle_clockwise(1)
    #     # c.rotate_middle_counter_clockwise(1)
    #     c.rotate_clockwise(3)
    #     print(c)
    #     print()
    print(c)
    # print(c.is_solved())