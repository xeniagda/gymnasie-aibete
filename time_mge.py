import timeit

from multiGameEngine import MultiGameEngine
from gameEngine import GameEngine
from graphics import UI
from util import Actions
from levelGenerator import NenaGenerator

TIME_TIMES = 1000

N_MULTI = 1000

ui = UI(False, 0)

lvl = NenaGenerator(1).generate(100)

ge = GameEngine(ui, lvl)
mge = MultiGameEngine([lvl] * N_MULTI)

t_ge = 1 / TIME_TIMES * timeit.timeit("ge.performTick(Actions.RIGHT)", globals=globals(), number=TIME_TIMES)
print("One normal gameEngine:", t_ge)

t_ges = 1 / (TIME_TIMES * N_MULTI) * timeit.timeit("mge.performTick([Actions.RIGHT] * N_MULTI)", globals=globals(), number=TIME_TIMES)
print("One of", N_MULTI, " parallel gameEngines:", t_ges)

print(t_ge / t_ges, "x faster")
