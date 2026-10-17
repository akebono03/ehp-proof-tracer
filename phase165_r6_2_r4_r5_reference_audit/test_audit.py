from dataclasses import dataclass
from audit import walk

@dataclass(frozen=True)
class Inner:
    x: int

@dataclass(frozen=True)
class Outer:
    child: Inner
    items: tuple[int, ...]

def test_walk_top():
    assert list(walk(3)) == [('content', 3)]

def test_walk_nested():
    result = dict(walk(Outer(Inner(2),(3,))))
    assert result['content.child.x'] == 2
    assert result['content.items[0]'] == 3

def test_walk_empty_tuple():
    assert len(list(walk(()))) == 1

def test_walk_depth_limit():
    assert len(list(walk(Outer(Inner(2),(3,)), depth=8))) == 1
