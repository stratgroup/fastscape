import xsimlab as xs

from .main_drivers import TotalErosion
from .tectonics import BlockUplift


@xs.process
class BaseIsostasy(object):
    """Base class for isostasy.

    It only defines the variable ``isostaty`` and should be
    sub-classed.

    """
    isostasy = xs.variable(dims=('y', 'x'), intent='out',
                           group='elevation_up')


@xs.process
class BaseLocalIsostasy(BaseIsostasy):
    """Base class for local isostasy.

    It only defines a local isostasic coefficient and should be
    sub-classed.

    """
    i_coef = xs.variable(description='local isostatic coefficient')


@xs.process
class LocalIsostasyErosion(BaseLocalIsostasy):
    """Local isostasic effect of erosion."""

    erosion = xs.foreign(TotalErosion, 'erosion')

    def run_step(self, dt):
        self.isostasy = self.i_coef * self.erosion


@xs.process
class LocalIsostasyUplift(BaseLocalIsostasy):
    """Local isostasic effect of rock uplift."""

    uplift = xs.foreign(BlockUplift, 'uplift')

    def run_step(self, dt):
        self.isostasy = -1. * self.i_coef * self.uplift


@xs.process
class LocalIsostasyErosionUplift(BaseLocalIsostasy):
    """Local isostatic effect of both erosion and tectonic uplift."""

    erosion = xs.foreign(TotalErosion, 'erosion')
    uplift = xs.foreign(BlockUplift, 'uplift')

    def run_step(self, dt):
        self.isostasy = self.i_coef * (self.erosion - self.rock_uplift)