import random


class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.hits = []

    def hit(self, coordinate):
        self.hits.append(coordinate)

    def is_sunk(self):
        return all(coordinate in self.hits for coordinate in self.coordinates)


class Board:
    def __init__(self, size):
        self.size = size
        self.ships = []
        self.grid = [['О' for _ in range(size)] for _ in range(size)]
        self.hits = []
        self.misses = []

    @staticmethod
    def valid_enter(x, y, coordinates):
        x1, y1 = x, y
        if (x, y) in coordinates:
            raise ValueError("Вы уже выбрали эту координату")
        if not player_board.is_valid_coordinate((x, y)):
            raise ValueError("Неверное расположение корабля")
        if player_board.grid[x][y] == '■':
            raise ValueError("В этом месте уже есть корабль")
        for x, y in player_board.get_adjacent_coordinates(x, y):
            if player_board.is_valid_coordinate((x, y)) and player_board.grid[x][y] == '■':  #
                raise ValueError("Корабль должен находиться на расстоянии одной клетки")
        coordinates.append((x1, y1))

    @staticmethod
    def valid_enter_comp(x, y):
        if not computer_board.is_valid_coordinate((x, y)):
            return False
        if player_board.grid[x][y] == '■':
            return False
        for x, y in computer_board.get_adjacent_coordinates(x, y):
            if computer_board.is_valid_coordinate((x, y)) and computer_board.grid[x][y] == '■':
                return False
        return True

    def add_ship(self, ship):
        try:
            for coordinate in ship.coordinates:
                self.grid[coordinate[0]][coordinate[1]] = '■'
            self.ships.append(ship)
        except ValueError:
            raise ValueError("Так располагать нельзя")

    def is_valid_coordinate(self, coordinate):
        x, y = coordinate
        return 0 <= x < self.size and 0 <= y < self.size

    @staticmethod
    def get_adjacent_coordinates(x, y):
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    def is_hit(self, coordinate):
        return coordinate in self.hits

    def is_miss(self, coordinate):
        return coordinate in self.misses

    def record_hit(self, coordinate):
        self.grid[coordinate[0]][coordinate[1]] = 'X'
        self.hits.append(coordinate)

    def record_miss(self, coordinate):
        self.grid[coordinate[0]][coordinate[1]] = 'T'
        self.misses.append(coordinate)

    def display(self):
        print("    | " + " | ".join(str(i + 1) for i in range(self.size)) + " |")
        for i in range(self.size):
            row = "| " + " | ".join(self.grid[i]) + " |"
            print(f"{i + 1} | {row}")


player_board = Board(6)
computer_board = Board(6)


def play_game():
    player_board.display()
    print("Расположите свои корабли:")
    numb_ship = 1
    for ship_size in [3, 2, 2, 1, 1, 1, 1]:
        while True:
            if ship_size == 2 or ship_size == 3:
                try:
                    vert_or_hor = int(input("Вы хотите расположить корабль вертикально (1) или горизонтально (2)?: "))
                    if vert_or_hor == 1:
                        coordinates = []
                        y = int(input(f"Enter Y coordinate for ship {numb_ship} of size {ship_size}: ")) - 1
                        if 0 <= y < 6:
                            for i in range(ship_size):
                                x = int(input(f"Введите X координату для {numb_ship} корабля размером {ship_size}: ")) - 1
                                if 0 <= x < 6:
                                    player_board.valid_enter(x, y, coordinates)
                                else:
                                    print("Введите корректное число")
                            ship = Ship(coordinates)
                            player_board.add_ship(ship)
                            numb_ship += 1
                            player_board.display()
                            break
                        else:
                            print("Введите корректное число")
                    elif vert_or_hor == 2:
                        coordinates = []
                        x = int(input(f"Введите Y координату для {numb_ship} корабля размером {ship_size}: ")) - 1
                        if 0 <= x < 6:
                            for i in range(ship_size):
                                y = int(input(f"Enter Y coordinate for ship {numb_ship} of size {ship_size}: ")) - 1
                                if 0 <= y < 6:
                                    player_board.valid_enter(x, y, coordinates)
                                else:
                                    print("Введите корректное число")
                            ship = Ship(coordinates)
                            player_board.add_ship(ship)
                            numb_ship += 1
                            player_board.display()
                            break
                        else:
                            print("Введите корректное число")
                    else:
                        print("Введите корректное число")
                except ValueError as e:
                    print(e)
            else:
                try:
                    coordinates = []
                    x = int(input(f"Введите X координату для {numb_ship} корабля размером {ship_size}: ")) - 1
                    y = int(input(f"Введите Y координату для {numb_ship} корабля размером {ship_size}: ")) - 1
                    if player_board.grid[x][y] == '■':
                        raise ValueError("В этом месте уже есть корабль")
                    coordinates.append((x, y))
                    ship = Ship(coordinates)
                    player_board.add_ship(ship)
                    numb_ship += 1
                    player_board.display()
                    break
                except ValueError as e:
                    print(e)

    print("Компьютер расставляет корабли")
    for ship_size in [3, 2, 2, 1, 1, 1, 1]:
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            direction = random.choice(['horizontal', 'vertical'])
            if computer_board.valid_enter_comp(x, y):
                coordinates = [(x, y)]
            else:
                continue
            if direction == 'horizontal':
                for i in range(1, ship_size):
                    if computer_board.is_valid_coordinate((x, y + i)):
                        if computer_board.valid_enter_comp(x, y):
                            coordinates.append((x, y + i))
                        else:
                            ship_size += 1
                    else:
                        if computer_board.is_valid_coordinate((x, y - i)):
                            if computer_board.valid_enter_comp(x, y):
                                coordinates.append((x, y - i))
                            else:
                                ship_size += 1
            else:
                for i in range(1, ship_size):
                    if computer_board.is_valid_coordinate((x + i, y)):
                        if computer_board.valid_enter_comp(x, y):
                            coordinates.append((x + i, y))
                        else:
                            ship_size += 1
                    else:
                        if computer_board.is_valid_coordinate((x - i, y)):
                            if computer_board.valid_enter_comp(x, y):
                                coordinates.append((x - i, y))
                            else:
                                ship_size += 1
            try:
                ship = Ship(coordinates)
                computer_board.add_ship(ship)
                break
            except ValueError:
                continue

    while True:
        print("Поле игрока: ")
        player_board.display()
        print("Ход игрока :")
        x = int(input("Введите X координату для атаки: ")) - 1
        y = int(input("Введите Y координату для атаки ")) - 1
        if 0 <= y < 6 and 0 <= x < 6:
            if computer_board.is_hit((x, y)) or computer_board.is_miss((x, y)):
                print("Вы уже атаковали данную координату. Введите другие координаты")
                continue
            if computer_board.grid[x][y] == '■':
                print("Попадание!")
                computer_board.record_hit((x, y))
                for ship in computer_board.ships:
                    if (x, y) in ship.coordinates:
                        ship.hit((x, y))
                        if ship.is_sunk():
                            print("Вы потопили корабль!")
                            computer_board.ships.remove(ship)
                        break
            else:
                print("Промах!")
                computer_board.record_miss((x, y))
        else:
            print("Введите корректное число")
            continue
            
        if not computer_board.ships:
            print("Поздравляю! Вы победили!")
            break

        print("Ход компьютера:")
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            if (x, y) not in player_board.hits and (x, y) not in player_board.misses:
                break
        if player_board.grid[x][y] == '■':
            print("В ваш корабль попали!")
            for ship in player_board.ships:
                if (x, y) in ship.coordinates:
                    ship.hit((x, y))
                    if ship.is_sunk():
                        print("Компьютер потопил ваш корабль!")
                        player_board.ships.remove(ship)
                    break
        else:
            print("Компьютер промахнулся!")
            player_board.record_miss((x, y))

        if not player_board.ships:
            print("Игра завершена. Вы проиграли.")
            break


if __name__ == "__main__":
    play_game()
