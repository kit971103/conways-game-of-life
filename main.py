import time

from basic import Style, Rule, Status
from campus import Campus


class GameOfLive:
    def __init__(self, campus: Campus, style: Style, rule: Rule) -> None:
        self.style: Style = style
        self.rule: Rule = rule
        self.campus: Campus = campus
        self.gen_n: int = 0

    def step(self) -> None:
        self.gen_n += 1
        next_campus = self.campus.new_campus()
        for point in self.campus.all_points():
            neighbours_cells: int = self.campus.get_alive_count(point)
            if self.campus[point] is Status.ALIVE:
                next_campus[point] = Status(neighbours_cells in self.rule.comfort_zone)
            else:
                next_campus[point] = Status(neighbours_cells in self.rule.zombie_zone)
        self.campus = next_campus

    def display(self) -> None:
        print(f"Gen: {self.gen_n}")
        self.campus.display(self.style)
        print('')

    def clear(self) -> None:
        for _ in range(self.campus._size + 3):
            print('\033[F\r\033[K', end='')


def get_standard_game():
    return GameOfLive(Campus().ramdom_campus(), Style(), Rule())

def main(fps: int = 5, time_s: int = 30):
    style = Style(live='\u001b[31mX\u001b[0m')
    classic_rule = Rule()
    random_map = Campus(20).ramdom_campus(odd = 3)
    game = GameOfLive(random_map, style, classic_rule)

    for _ in range(time_s * fps):
        game.display()
        time.sleep(1/fps)
        game.clear()
        game.step()
    game.display()
    print('Endeddddddddddddddddddddddddddddddddd')


def get_int_input(msg: str) -> int:
    while True:
        
        n = input(msg)
        try:
            n = int(n)
        except ValueError:
            print("enter an integer!")
            continue
        
        if isinstance(n, int) and n != 0:
            print(f"got {n}")
            return n
        

if __name__ == "__main__":
    duration = get_int_input("Enter time: ")
    fps = get_int_input("Enter fps: ")
    main(fps, duration)
