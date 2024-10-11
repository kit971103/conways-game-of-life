from dataclasses import dataclass
from typing import Callable, Optional


def step_fun_factory(multulier: int) -> Callable[[int], int]:
    def step_fun(n: int) -> int:
        return multulier * n + 1 if n % 2 else n // 2
    return step_fun


def inv_fun_factory(multulier: int) -> Callable[[int], tuple[int] | tuple[int, int]]:
    def inv_func(n: int) -> tuple[int] | tuple[int, int]:
        if (n-1) % multulier or n == 1:
            return (n*2, )
        return (n*2, (n-1)//multulier)
    return inv_func


def is_natural_num(n: int) -> bool:
    return isinstance(n, int) and n > 0


def is_odd_natural_num(n: int) -> bool:
    return is_natural_num(n) and n % 2 == 1


@dataclass()
class CollatzNode:
    val: int
    tree: 'CollatzDict'

    def __post_init__(self) -> None:
        if not is_natural_num(self.val):
            raise ValueError(f'Expected natural number, but got{self.val}')

        self.step_count: int = (self.next.step_count + 1) if self.val != 1 else 0
        self.peak: int = max(self.val, self.next.peak) if self.val != 1 else 1

    @property
    def next(self) -> 'CollatzNode':
        new_val = self.tree.step_func(self.val)
        return self.tree[new_val]

    @property
    def prev(self) -> tuple['CollatzNode', ...]:
        prev_vals = self.tree.inv_func(self.val)
        return tuple(self.tree[val] for val in prev_vals)

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        val, step, peak = self.val, self.step_count, self.peak
        return f"{cls_name}({val=}, rule={self.tree.multulier}n+1, {step=}, {peak=})"


class CollatzDict:
    def __init__(self, odd_multulier: int = 3) -> None:
        self.nodes: dict[int, CollatzNode] = {}
        self.set_rule(odd_multulier)

    def clear_cache(self) -> None:
        self.nodes.clear()

    def set_rule(self, odd_multulier: int) -> None:
        if not is_odd_natural_num(odd_multulier):
            raise ValueError(f'Expected odd number, but got{odd_multulier}')
        self.clear_cache()
        self.multulier: int = odd_multulier
        self.step_func: Callable[[int], int] = step_fun_factory(odd_multulier)
        self.inv_func: Callable[[int], tuple[int, ...]] = inv_fun_factory(odd_multulier)

    def __getitem__(self, n: int) -> CollatzNode:
        if n not in self.nodes:
            self.nodes[n] = CollatzNode(n, self)
        return self.nodes[n]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(para={self.multulier}, {len(self.nodes)} nodes)"

    def __eq__(self, value: object) -> bool:
        return isinstance(value, self.__class__) and (self.multulier == value.multulier)


def main(max_range: int):
    max_step_key, max_step = 1, 0
    max_peak_key, max_peak = 1, 1
    collatz_tree = CollatzDict()
    for n in range(1, max_range+1):
        node = collatz_tree[n]
        if node.step_count > max_step:
            max_step = node.step_count
            max_step_key = n
        if node.peak > max_peak:
            max_peak = node.peak
            max_peak_key = n
    print(f"In range of  [1, {max_range}]")
    print(f"\tmax step is {max_step} at {max_step_key}")
    print(f"\tthe peak is {max_peak} at {max_peak_key}")


def test_default():
    collatz_tree = CollatzDict()
    assert collatz_tree[3].next == collatz_tree[10]
    assert collatz_tree[10].next == collatz_tree[5]
    assert collatz_tree[3].prev == (collatz_tree[6], )
    assert collatz_tree[27].peak == 9232

    collatz_tree = CollatzDict(5)
    assert collatz_tree[3].next == collatz_tree[16]
    assert collatz_tree[16].next == collatz_tree[8]
    assert collatz_tree[8].next == collatz_tree[4]
    assert collatz_tree[16].prev == (collatz_tree[32], collatz_tree[3])
    print("Passed all test")


if __name__ == '__main__':
    test_default()
    print(CollatzDict()[27])
