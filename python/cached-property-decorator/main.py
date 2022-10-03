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

# %%
import contextlib
from random import random
from time import perf_counter, sleep

# %%
def cached_property(func):
    """decorator used to cache expensive object attribute lookup"""
    name = f"_cached_{func.__name__}"

    @property
    def lookup(instance):
        if hasattr(instance, name):
            return getattr(instance, name)
        value = func(instance)
        setattr(instance, name, value)
        return value

    return lookup


class Planet:
    """the nicest little orb this side of Orion's Belt"""

    GRAVITY_CONSTANT = 42
    TEMPORAL_SHIFT = 0.12345
    SOLAR_MASS_UNITS = "M\N{SUN}"

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.color)})"

    @cached_property
    def mass(self):
        scale_factor = random()
        sleep(self.TEMPORAL_SHIFT)
        return (
            f"{round(scale_factor * self.GRAVITY_CONSTANT, 4)} "
            f"{self.SOLAR_MASS_UNITS}"
        )


# %%
blue = Planet("blue")

start_time = perf_counter()
for _ in range(5):
    blue.mass
end_time = perf_counter()
elapsed_time = end_time - start_time
assert elapsed_time < 0.5

with contextlib.suppress(AttributeError):
    blue.mass = 42


# %%
