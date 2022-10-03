# %% [markdown]
# # Cached property decorator
# Given the sample class Planet, computing the mass attribute of an instance is a
# computationally expensive and time consuming operation. Ideally you'd like
# this attribute to be a cached_property that only gets computed once and is then
# stored for future access, not having to be recalculated over (and over and over).
#
# ## Tasks
#
# Complete cached_property(func) as a decorator function, so that asking
# "What was the mass of Planet('red') again?" is consistent and quick.

from random import random
from time import sleep, perf_counter


def cached_property(func):
    """decorator used to cache expensive object attribute lookup"""
    
    def wrapper(self):
        """wrapper function"""
        if not hasattr(self, "_cache"):
            self._cache = {}
        if func.__name__ not in self._cache:
            self._cache[func.__name__] = func(self)
        return self._cache[func.__name__]

    return wrapper


class Planet:
    """the nicest little orb this side of Orion's Belt"""

    GRAVITY_CONSTANT = 42
    TEMPORAL_SHIFT = 0.12345
    SOLAR_MASS_UNITS = "M\N{SUN}"

    def __init__(self, color):
        self.color = color
        self._mass = None

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.color)})"

    @property
    @cached_property
    def mass(self):
        scale_factor = random()
        sleep(self.TEMPORAL_SHIFT)
        self._mass = (
            f"{round(scale_factor * self.GRAVITY_CONSTANT, 4)} "
            f"{self.SOLAR_MASS_UNITS}"
        )
        return self._mass
    
    @mass.setter
    def mass(self, _):
        raise AttributeError("can't set attribute")

if __name__ == "__main__":
    blue = Planet('blue')

    start_time = perf_counter()
    for _ in range(5):
        blue.mass
    end_time = perf_counter()
    elapsed_time = end_time - start_time
    assert elapsed_time < .5