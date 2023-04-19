import numpy as np

def snap_to_grid( grid_start: float, grid_scale: float, values: np.ndarray ) -> np.ndarray:
    grid_values = ( values - grid_start ) * grid_scale
    return grid_values
