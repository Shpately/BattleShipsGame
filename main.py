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

    def add_ship(self, ship):
        for coordinate in ship.coordinates:
            if not self.is_valid_coordinate(coordinate):
                raise ValueError("Invalid ship placement")
            for x, y in self.get_adjacent_coordinates(coordinate):
                if self.is_valid_coordinate((x, y)) and self.grid[x][y] == '■':
                    raise ValueError("Ships must be at least one cell apart")
            self.grid[coordinate[0]][coordinate[1]] = '■'
        self.ships.append(ship)

    def is_valid_coordinate(self, coordinate):
        x, y = coordinate
        return 0 <= x < self.size and 0 <= y < self.size

    def get_adjacent_coordinates(self, coordinate):
        x, y = coordinate
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    def is_hit(self, coordinate):
        return coordinate in self.hits

    def is_miss(self, coordinate):
        return coordinate in self.misses

    def record_hit(self, coordinate):
        self.hits.append(coordinate)

    def record_miss(self, coordinate):
        self.misses.append(coordinate)

    def display(self):
        print("  | " + " | ".join(str(i + 1) for i in range(self.size)) + " |")
        for i in range(self.size):
            row = "| " + " | ".join(self.grid[i]) + " |"
            print(f"{i + 1} | {row}")


player_board = Board(6)
computer_board = Board(6)


def play_game():
    # Place ships on player board
    print("Place your ships:")
    for ship_size in [3, 2, 2, 1, 1, 1, 1]:
        while True:
            try:
                numb_ship = 1
                coordinates = []
                for i in range(ship_size):
                    x = int(input(f"Enter X coordinate for ship {numb_ship} of size {ship_size}: ")) - 1
                    y = int(input(f"Enter Y coordinate for ship {numb_ship} of size {ship_size}: ")) - 1
                    coordinates.append((x, y))
                ship = Ship(coordinates)
                player_board.add_ship(ship)
                numb_ship += 1
                break
            except ValueError as e:
                print(e)

    # Place ships on computer board
    for ship_size in [3, 2, 2, 1, 1, 1, 1]:
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            direction = random.choice(['horizontal', 'vertical'])
            coordinates = [(x, y)]
            if direction == 'horizontal':
                for i in range(1, ship_size):
                    coordinates.append((x + i, y))
            else:
                for i in range(1, ship_size):
                    coordinates.append((x, y + i))
                    try:
                        ship = Ship(coordinates)
                        computer_board.add_ship(ship)
                        break
                    except ValueError:
                        continue

    while True:
        print("Player's turn:")
        player_board.display()
        x = int(input("Enter X coordinate for your attack: ")) - 1
        y = int(input("Enter Y coordinate for your attack: ")) - 1
        if player_board.is_hit((x, y)) or player_board.is_miss((x, y)):
            print("You've already attacked that coordinate. Try again.")
            continue
        if computer_board.grid[x][y] == '■':
            print("Hit!")
            player_board.record_hit((x, y))
            for ship in computer_board.ships:
                if (x, y) in ship.coordinates:
                    ship.hit((x, y))
                    if ship.is_sunk():
                        print("You sank a ship!")
                        computer_board.ships.remove(ship)
                    break
        else:
            print("Miss.")
            player_board.record_miss((x, y))

        if not computer_board.ships:
            print("Congratulations! You won!")
            break

        print("Computer's turn:")
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            if (x, y) not in player_board.hits and (x, y) not in player_board.misses:
                break
        if player_board.grid[x][y] == '■':
            print("You were hit!")
            for ship in player_board.ships:
                if (x, y) in ship.coordinates:
                    ship.hit((x, y))
                    if ship.is_sunk():
                        print("Computer sank one of your ships!")
                        player_board.ships.remove(ship)
                    break
        else:
            print("Computer missed.")
            player_board.record_miss((x, y))

        if not player_board.ships:
            print("Game over. You lost.")
            break


if __name__ == "__main__":
    print("Hello")
    play_game()
