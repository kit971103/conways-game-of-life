from dataclasses import dataclass
from enum import IntEnum
from typing import NamedTuple, Optional


class Status(IntEnum):
    ALIVE = 1
    DEAD = 0


@dataclass
class Style:
    left: str = "["
    right: str = "]"
    live: str = "X"
    dead: Optional[str] = None
    _name: str = "Basic"

    def __post_init__(self) -> None:
        if self.dead is None:
            # self.dead = ' ' * len(self.live)
            self.dead = ' '


@dataclass
class Rule:
    comfort_zone: tuple[int, ...] = (2, 3)  # live -> live, else live -> dead
    zombie_zone: tuple[int, ...] = (3,)  # dead -> live, else still dead
    _name: str = "Basic"


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        return self.__add__(other)
