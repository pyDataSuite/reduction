import numpy as np

class Boundary:
    def __init__( self, xmin, xmax, ymin, ymax, zmin=np.nan, zmax=np.nan ):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax