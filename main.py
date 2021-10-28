import math
import random as r


class Glass:
    waters = []
    max_length = 4

    def define_waters(self, waters):
        self.waters = waters
        return self

    def upper_water(self):
        if len(self.waters) == 0:
            return None
        else:
            return self.waters[-1]

    def upper_water_length(self):
        length = 0
        for i in range(1, 1 + len(self.waters)):
            if self.waters[-i] == self.upper_water():
                length += 1
            else:
                return length
        return length

    def empty_layer_length(self):
        return self.max_length - len(self.waters)

    def is_pure(self):
        if len(self.waters) == 0:
            return True
        elif len(self.waters) < self.max_length:
            return False
        else:
            previous = self.upper_water()
            for color in self.waters:
                if color == previous:
                    previous = color
                else:
                    return False
            return True


class Table:

    def __init__(self, glasses=None):
        self.glasses = []
        self.append(glasses)

    def append(self, new_glasses):
        if new_glasses is not None:
            for glass in new_glasses:
                self.glasses.append(glass)

    def _move_check(self, source_glass_index, target_glass_index, internal):

        source_glass = self.glasses[source_glass_index]
        target_glass = self.glasses[target_glass_index]

        if source_glass_index == target_glass_index:
            if not internal:
                print('source and target cannot be the same')
            return 1

        if source_glass.upper_water() is None:
            if not internal:
                print('source glass is empty')
            return 2

        if source_glass.upper_water() != target_glass.upper_water() and target_glass.upper_water() is not None:
            if not internal:
                print('colors are not matching')
            return 3

        return 0

    def fill(self, source_glass_index, target_glass_index, internal=True):

        source_glass = self.glasses[source_glass_index]
        target_glass = self.glasses[target_glass_index]

        if self._move_check(source_glass_index, target_glass_index, internal) == 0:
            transfer_water = [source_glass.upper_water() for _ in range(source_glass.upper_water_length())]
            transfer_water = transfer_water[0:target_glass.empty_layer_length()]
            for water in transfer_water:
                source_glass.waters.pop(-1)
                target_glass.waters.append(water)
            return 0

    def _is_finished(self):
        finished = True
        for glass in self.glasses:
            if not glass.is_pure():
                finished = False
        return finished

    def _possible_moves(self):
        possible_moves = []
        for source_index in range(len(self.glasses)):
            for target_index in range(len(self.glasses)):
                if self._move_check(source_index, target_index, True) == 0:
                    possible_moves.append([source_index, target_index])
        return possible_moves

    def solve_one_iteration(self):
        import ai
        datas = []
        solved = False
        for move in self._possible_moves():
            new_table = Table([Glass().define_waters(
                [water for water in self.glasses[i].waters]) for i in range(len(self.glasses))])
            new_table.fill(move[0], move[1])
            priority = ai.guess(new_table)
            if new_table._is_finished():
                solved = True
                return [new_table, move, priority], solved
            datas.append([new_table, move, priority])
        return datas, solved

    def solve(self):
        def find_lowest_priority(datas):
            lowest_indexes = []
            temp_lowest_priority = math.inf
            for index in range(len(datas)):
                temp_priority = datas[index][2]
                if temp_priority <= temp_lowest_priority:
                    temp_lowest_priority = temp_priority
            for index in range(len(datas)):
                temp_priority = datas[index][2]
                if temp_priority == temp_lowest_priority:
                    lowest_indexes.append(index)
            if len(lowest_indexes) == 1:
                temp_lowest_index = lowest_indexes[0]
            else:
                temp_lowest_index = lowest_indexes[r.randint(0, len(lowest_indexes)-1)]
            return temp_lowest_index, temp_lowest_priority

        main_datas = [[self, [], -1]]
        for i in range(100):
            lowest_index, lowest_priority = find_lowest_priority(main_datas)
            prioritized_data = main_datas[lowest_index]
            table, move, priority = prioritized_data
            print(move)

            generated_datas, solved = table.solve_one_iteration()
            main_datas.pop(lowest_index)
            if solved:
                generated_move_full = move.copy()
                generated_move_full.append(generated_datas[1])
                print(generated_move_full)
                return generated_move_full

            for generated_data in generated_datas:
                generated_table, generated_move, generated_priority = generated_data
                generated_move_full = move.copy()
                generated_move_full.append(generated_move)
                main_datas.append([generated_table, generated_move_full, generated_priority])

    def _shuffle_move_check_reverse(self, source_glass_index, target_glass_index):

        source_glass = self.glasses[source_glass_index]
        target_glass = self.glasses[target_glass_index]

        if source_glass_index == target_glass_index:
            return 1

        if source_glass.upper_water() is None:
            return 2

        if target_glass.empty_layer_length() == 0:
            return 3

        if source_glass.upper_water_length() == 1:
            return 4

        return 0

    def _shuffle_fill_reverse(self, source_glass_index, target_glass_index):

        source_glass = self.glasses[source_glass_index]
        target_glass = self.glasses[target_glass_index]

        if self._shuffle_move_check_reverse(source_glass_index, target_glass_index) == 0:
            transfer_water = [source_glass.upper_water() for _ in range(source_glass.upper_water_length() - 1)]
            transfer_water = transfer_water[0:target_glass.empty_layer_length()]
            if len(transfer_water) > 1:
                transfer_water = transfer_water[0: r.randint(1, len(transfer_water) - 1)]

            for water in transfer_water:
                source_glass.waters.pop(-1)
                target_glass.waters.append(water)
            return 0

    def _shuffle_get_random_glass_pair(self):
        for i in range(300):
            source_index = r.randint(0, len(self.glasses) - 1)
            target_index = r.randint(0, len(self.glasses) - 1)
            if self._shuffle_move_check_reverse(source_index, target_index) == 0:
                return source_index, target_index
        return None, None

    def shuffle(self, move_amount):
        moves = []
        for i in range(move_amount):
            source_index, target_index = self._shuffle_get_random_glass_pair()
            if source_index is None:
                break
            moves.append([target_index, source_index])
            self._shuffle_fill_reverse(source_index, target_index)
        inverted_moves = []
        for i in range(len(moves)):
            inverted_moves.append(moves[-i - 1])
        return inverted_moves

    def get_glasses(self):
        return [glass.waters for glass in self.glasses]

    def set_default_table(self):
        self.glasses = [
            Glass().define_waters([1, 1, 1, 1]),
            Glass().define_waters([2, 2, 2, 2]),
            Glass().define_waters([3, 3, 3, 3]),
            Glass().define_waters([4, 4, 4, 4]),
            Glass().define_waters([5, 5, 5, 5]),
            Glass().define_waters([6, 6, 6, 6]),
            Glass().define_waters([7, 7, 7, 7]),
            Glass().define_waters([8, 8, 8, 8]),
            Glass().define_waters([9, 9, 9, 9]),
            Glass().define_waters([10, 10, 10, 10]),
            Glass().define_waters([]),
            Glass().define_waters([])]

    def display(self, moves=None):
        x = []
        for glass in self.get_glasses():
            x.append(glass.copy())
        for glass in x:
            for _ in range(4 - len(glass)):
                glass.append('.')

        for not_inverted_i in range(4):
            i = 3 - not_inverted_i
            layer = []
            for j in range(len(self.glasses)):
                if type(x[j][i]) is int:
                    x[j][i] -= 1
                layer.append(str(x[j][i]))
            print(layer)

        print('____________________________________________________________')
        print([str(i) for i in range(len(self.glasses))])
        if moves is not None:
            for move in moves:
                print(move)
                for i in range(2):
                    print()
                self.fill(move[0], move[1])
                self.display()
            print('____________________________________________________________')


if("__main__" == __name__):
    my_table = Table()
    my_glasses = [
        Glass().define_waters([1, 1, 1, 1]),
        Glass().define_waters([2, 2, 2, 2]),
        Glass().define_waters([3, 3, 3, 3]),
        Glass().define_waters([4, 4, 4, 4]),
        Glass().define_waters([5, 5, 5, 5]),
        Glass().define_waters([6, 6, 6, 6]),
        Glass().define_waters([7, 7, 7, 7]),
        Glass().define_waters([8, 8, 8, 8]),
        Glass().define_waters([9, 9, 9, 9]),
        Glass().define_waters([]),
        Glass().define_waters([10, 10, 10, 10]),
        Glass().define_waters([])
    ]
    #my_table.glasses = my_glasses
    my_table.set_default_table()
    my_table.display()
    print(my_table.shuffle(6))
    my_table.display()
    print(my_table.solve())
    my_table.display()
