import pyximport
import random as rd

pyximport.install()

from ca import *


class SC(CA):

    @staticmethod
    def get_index(index, neighbours):

        # Search for empty slots indexes for indexing its positions
        if index != -1:
            try:
                index = neighbours.index(0, index + 1)
            except ValueError:
                return -1
        else:
            index = neighbours.index(0)

        return index

    '''
    0 --> There's no individual at the position
    1 --> There's an element from the N1 species
    2 --> There's an element from the N2 species
    Reproducing and moving rules are applied the same for both species
    '''
    def rule(self, x, y):

        # Control variable for empty slots
        index = -1

        # N1 and N2 birth probabilities
        n1_birth = 0.5
        n2_birth = 0.5

        # N1 and N2 moving probabilities
        n1_move = 0.4
        n2_move = 0.8

        # Generates random real number (0 to 1) to define N1 and N2 births and movimentation
        prob_n1_birth = rd.random()
        prob_n2_birth = rd.random()
        prob_n1_move = rd.random()
        prob_n2_move = rd.random()

        # Gets the position (x, y) from each neighbor of the actual individual and its ID (N1 - 1, N2 - 2 or empty - 0)
        positions = self.__neighbors8__(x, y, old=True, pos=True)
        neighbours = list(self.__neighbors8__(x, y, old=True))

        individual = self[x][y]

        if individual == 1:

            '''
            An individual from N1 species can reproduce when the following conditions happen simultaneously:
            I)   There must be at least one individual from N1 species at its neighborhood
            II)  Generated probability is high enough
            III) N1 has more individuals than N2 in the neighborhood grid (3 x 3)
            IV)  There must be an empty slot at the neighborhood for the birth of a new N1 element 
            '''
            if neighbours.count(1) >= 1 and prob_n1_birth > n1_birth and \
                    neighbours.count(1) >= neighbours.count(2) and neighbours.count(0) > 0:

                index = neighbours.index(0)
                coord = positions[index]

                new_x = coord[0]
                new_y = coord[1]

                self.add(1, [(new_x, new_y)])

            '''
            An individual from N1 species can move when the following conditions happen simultaneously:
            I)  Generated probability is high enough
            II) After reproducing process happen (or not), there must be an empty slot at the neighborhood
            '''
            if prob_n1_move > n1_move and neighbours.count(0) > 0:

                index = self.get_index(index, neighbours)

                if index == -1:
                    # There's no empty slot at the neighborhood to move --> individual stays where it was
                    return 1
                else:
                    # Gets the coordinate from the empty slot for moving
                    coord = positions[index]
                    new_x = coord[0]
                    new_y = coord[1]

                    # N1 individual moves and leaves the old position empty (can move in diagonals too)
                    self.add(1, [(new_x, new_y)])
                    return 0

            # If the actual individual can't reproduce or move, no changes are made in the grid
            return 1

        elif individual == 2:

            if neighbours.count(2) >= 1 and prob_n2_birth > n2_birth and \
                    neighbours.count(2) >= neighbours.count(1) and neighbours.count(0) > 0:

                index = neighbours.index(0)
                coord = positions[index]

                new_x = coord[0]
                new_y = coord[1]

                self.add(2, [(new_x, new_y)])

            if prob_n2_move > n2_move and neighbours.count(0) > 0:

                index = self.get_index(index, neighbours)

                if index == -1:
                    return 2
                else:
                    coord = positions[index]

                    new_x = coord[0]
                    new_y = coord[1]

                    self.add(2, [(new_x, new_y)])
                    return 0

            return 2

        else:
            # If the actual element is not from N1 or N2 (empty), nothing happens
            return 0


if __name__ == '__main__':

    # Creates a 40 x 40 grid with random values ranging from 0 to 2
    simulation = SC(40, values=3)
    plot(simulation)
