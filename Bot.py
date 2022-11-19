
from RubixCube import RubixCube
import random

num_inputs = 54
num_outputs = 18
episodes = 1000

def random_move(cube: RubixCube):
    return random.choice(cube.next_states())


opposite = {0: 2, 1: 3, 2: 1, 3: 1, 4: 5, 5: 4}


def white_cross_eval(rubix: RubixCube):
    score = 0
    white_face = 0
    while rubix.cube[white_face][1][1] != 5:
        white_face += 1
    for row in rubix.cube[white_face]:
        for val in row:
            if val == 5:
                score += 5
    for row in rubix.cube[opposite[white_face]]:
        for val in row:
            if val == 5:
                score -= 1
    return score


class WhiteCrossBot:
    def white_cross_move(self, rubix: RubixCube):
        next_ones = rubix.next_states()
        random.shuffle(next_ones)
        # second_states = []
        # for a in range(num_outputs):
        #     next_twos = next_ones[a].next_states()
        #     random.shuffle(next_twos)
        #     second_states.append(next_twos)

        max_eval = -10
        best_index = 0
        for i in range(num_outputs):
            eval = white_cross_eval(next_ones[i])
            if eval > max_eval:
                max_eval = eval
                best_index = i
            for s2 in next_ones[i].next_states():
                eval = white_cross_eval(s2)
                if eval > max_eval:
                    best_index = i
                for s3 in s2.next_states():
                    eval = white_cross_eval(s3)
                    if eval > max_eval:
                        best_index = i

        print(max_eval)
        return next_ones[best_index]

if __name__ == "__main__":
    rc = RubixCube()
    print(rc)
    # print(white_cross_eval())
    print(white_cross_eval(rc))
