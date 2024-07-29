from itertools import product
from typing import Optional, Iterator, Self
from random import seed, randint

from basic import Point, Status, Style


class Campus:
    def __init__(self, size: int = 10) -> None:
        # top left is Point(0,0), down and right are positive
        self._size: int = size
        self.campus: list[list[Status]]
        self.init_campus()                 
    
    def __getitem__(self, key: Point) -> Status:
        # _check_is_Point(key)
        in_bound = 0 <= key.x < self._size and 0 <= key.y < self._size
        return self.campus[key.y][key.x] if in_bound else Status.DEAD

    def __setitem__(self, key: Point, newvalue: Status):
        # _check_is_Point(key)
        self.campus[key.y][key.x] = newvalue

    def __iter__(self) -> Iterator:
        return self.all_points()
    
    def all_points(self) -> Iterator:
        return map(lambda p: Point(*p), product(range(0, self._size), repeat=2))

    def new_campus(self, size: Optional[int] = None) -> 'Campus':
        return Campus(size or self._size)

    def init_campus(self) -> Self:
        self.campus = [[Status.DEAD] * self._size for _ in range(self._size)]
        return self

    def set_campus(self, setting: list[Point]) -> Self:
        self.init_campus()
        for point in setting:
            self[point] = Status.ALIVE
        return self

    def ramdom_campus(self, r_seed: Optional[int] = None, odd: int = 3) -> Self:
        self.init_campus()
        if r_seed is not None:
            seed(r_seed)
        for point in self:
            self[point] = Status(randint(1, odd) == 1)
        return self

    def get_alive_count(self, center: Point) -> int:
        steps = product((-1, 0, 1), repeat=2)
        return sum(self[center + step] for step in steps) - self[center]

    def display(self, style: Style) -> None:
        left = style.left
        right = style.right
        live = style.live
        dead = style.dead
        index_length = len(str(self._size-1))
        print(f"{'':>{index_length}} {''.join(f'{n:^3}' for n in range(self._size))}")
        for i, row in enumerate(self.campus):
            # Left + R(content)L + Right
            content = (live if status else dead for status in row)
            print(f"{i:>{index_length}} {left}{(right+left).join(content)}{right}") # type: ignore


def _check_is_Point(para) -> None:
    if not isinstance(para, Point):
        raise TypeError(f"expected a Point but got {type(para)}")


def main():
    c = Campus(size = 42)
    c.display(Style())


if __name__ == "__main__":
    main()
