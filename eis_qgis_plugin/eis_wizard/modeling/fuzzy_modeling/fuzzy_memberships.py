from typing import Tuple

import numpy as np
from qgis import processing
from qgis.core import QgsRasterLayer
from qgis.gui import QgsDoubleSpinBox


class FuzzyMembership:
    """Parent class for fuzzy memberships."""
    
    def x_range_static():
        """Generate x-coordinate values for plotting based on membership and parameters."""
        raise NotImplementedError("x_range_static method should be implemented in child class.")
    
    @staticmethod
    def x_range_dynamic(min: float, max: float) -> np.ndarray:
        """Generate x-coordinate values for plotting based on given min and max values."""
        return np.linspace(min, max, num=500)

    def membership_function():
        """Fuzzy membership function."""
        raise NotImplementedError("membership_function method should be implemented in child class.")

    def get_param_values(self):
        """Get current parameter values from linked widgets."""
        raise NotImplementedError("get_param_values method should be implemented in child class.")

    def reset_defaults(self):
        """Reset linked widgets to default values."""
        [widget.setValue(value) for widget, value in self.defaults.items()]

    def compute():
        """Compute fuzzy membership for selected input data."""
        raise NotImplementedError("get_param_values method should be implemented in child class.")


class GaussianMembership(FuzzyMembership):

    def __init__(self, c: QgsDoubleSpinBox, sigma: QgsDoubleSpinBox):
        self.c = c
        self.sigma = sigma
        self.defaults = {self.c: 10.0, self.sigma: 0.01}

    def get_param_values(self) -> Tuple[float, float]:
        return self.c.value(), self.sigma.value() 

    @staticmethod
    def x_range_static(c: float, sigma: float) -> np.ndarray:
        return np.linspace(c - 4*sigma, c + 4*sigma, num=500)
    
    @staticmethod
    def membership_function(x: np.ndarray, c: float, sigma: float) -> np.ndarray:
        return np.exp(-((x - c) ** 2) / (2 * sigma ** 2))

    @staticmethod
    def compute(c: float, sigma: float, input_raster: QgsRasterLayer, output_raster: str):
        # NOTE: We are using QGIS native algorithm here before EIS Toolkit includes fuzzy memberships
        processing.runAndLoadResults(
            "native:fuzzifyrastergaussianmembership",
            {
                'INPUT': input_raster,
                'BAND': 1,
                'FUZZYMIDPOINT': c,
                'FUZZYSPREAD': sigma,
                'OUTPUT': output_raster
            }
        )



class LargeMembership(FuzzyMembership):

    def __init__(self, c: QgsDoubleSpinBox, k: QgsDoubleSpinBox):
        self.c = c
        self.k = k
        self.defaults = {self.c: 50, self.k: 5}

    def get_param_values(self) -> Tuple[float, float]:
        return self.c.value(), self.k.value()

    @staticmethod
    def x_range_static(c: float, k: float) -> np.ndarray:
        spread_factor = 1 / k * 10
        return np.linspace(c - spread_factor, c + spread_factor, num=500)

    @staticmethod
    def membership_function(x: np.ndarray, c: float, k: float) -> np.ndarray:
        return 1 / (1 + np.exp(-k * (x - c)))
    
    @staticmethod
    def compute(c: float, k: float, input_raster: QgsRasterLayer, output_raster: str):
        # NOTE: We are using QGIS native algorithm here before EIS Toolkit includes fuzzy memberships
        processing.runAndLoadResults(
            "native:fuzzifyrasterlargemembership",
            {
                'INPUT': input_raster,
                'BAND': 1,
                'FUZZYMIDPOINT': c,
                'FUZZYSPREAD': k,
                'OUTPUT': output_raster
            }
        )


class LinearMembership(FuzzyMembership):

    def __init__(self, a: QgsDoubleSpinBox, b: QgsDoubleSpinBox):
        self.a = a
        self.b = b
        self.defaults = {self.a: 0, self.b: 1}

    def get_param_values(self) -> Tuple[float, float]:
        return self.a.value(), self.b.value()

    @staticmethod
    def x_range_static(a: float, b: float) -> np.ndarray:
        return np.linspace(a, b, num=500)

    @staticmethod
    def membership_function(x: np.ndarray, a: float, b: float) -> np.ndarray:
        return np.clip((x - a) / (b - a), 0, 1)
    
    @staticmethod
    def compute(a: float, b: float, input_raster: QgsRasterLayer, output_raster: str):
        # NOTE: We are using QGIS native algorithm here before EIS Toolkit includes fuzzy memberships
        processing.runAndLoadResults(
            "native:fuzzifyrasterlinearmembership",
            {
                'INPUT': input_raster,
                'BAND': 1,
                'FUZZYLOWBOUND': a,
                'FUZZYHIGHBOUND': b,
                'OUTPUT': output_raster
            }
        )


class NearMembership(FuzzyMembership):

    def __init__(self, c: QgsDoubleSpinBox, k: QgsDoubleSpinBox):
        self.c = c
        self.k = k
        self.defaults = {self.c: 50, self.k: 0.01}

    def get_param_values(self) -> Tuple[float, float]:
        return self.c.value(), self.k.value()

    @staticmethod
    def x_range_static(c: float, k: float) -> np.ndarray:
        spread_factor = max(1 / k * 10, 0.1)
        return np.linspace(c - spread_factor, c + spread_factor, num=500)


    @staticmethod
    def membership_function(x: np.ndarray, c: float, k: float) -> np.ndarray:
        return np.exp(-k * (x - c) ** 2)
    
    @staticmethod
    def compute(c: float, k: float, input_raster: QgsRasterLayer, output_raster: str):
        # NOTE: We are using QGIS native algorithm here before EIS Toolkit includes fuzzy memberships
        processing.runAndLoadResults(
            "native:fuzzifyrasternearmembership",
            {
                'INPUT': input_raster,
                'BAND': 1,
                'FUZZYMIDPOINT': c,
                'FUZZYSPREAD': k,
                'OUTPUT': output_raster
            }
        )
    

class PowerMembership(FuzzyMembership):

    def __init__(self, a: QgsDoubleSpinBox, b: QgsDoubleSpinBox, alpha: QgsDoubleSpinBox):
        self.a = a
        self.b = b
        self.alpha = alpha
        self.defaults = {self.a: 0, self.b: 1, self.alpha: 2}

    def get_param_values(self) -> Tuple[float, float, float]:
        return self.a.value(), self.b.value(), self.alpha.value()

    @staticmethod
    def x_range_static(a: float, b: float, _) -> np.ndarray:
        return np.linspace(a, b, num=500)

    @staticmethod
    def membership_function(x: np.ndarray, a: float, b: float, alpha: float) -> np.ndarray:
        return np.clip(1 - ((x - a) / (b - a)) ** alpha, 0, 1)
    
    @staticmethod
    def compute(a: float, b: float, alpha: float, input_raster: QgsRasterLayer, output_raster: str):
        # NOTE: We are using QGIS native algorithm here before EIS Toolkit includes fuzzy memberships
        processing.runAndLoadResults(
            "native:fuzzifyrasterpowermembership",
            {
                'INPUT': input_raster,
                'BAND': 1,
                'FUZZYLOWBOUND': a,
                'FUZZYHIGHBOUND': b,
                'FUZZYEXPONENT': alpha,
                'OUTPUT': output_raster
            }
        )


class SmallMembership(FuzzyMembership):

    def __init__(self, c: QgsDoubleSpinBox, k: QgsDoubleSpinBox):
        self.c = c
        self.k = k
        self.defaults = {self.c: 50, self.k: 5}

    def get_param_values(self) -> Tuple[float, float]:
        return self.c.value(), self.k.value(),

    @staticmethod
    def x_range_static(c: float, k: float) -> np.ndarray:
        spread_factor = 1 / k * 10
        return np.linspace(c - spread_factor, c + spread_factor, num=500)

    @staticmethod
    def _large_membership_function(x: np.ndarray, c: float, k: float) -> np.ndarray:
        return 1 / (1 + np.exp(-k * (x - c)))

    def membership_function(self, x: np.ndarray, c: float, k: float) -> np.ndarray:
        return 1 - self._large_membership_function(x, c, k)
    
    @staticmethod
    def compute(c: float, k: float, input_raster: QgsRasterLayer, output_raster: str):
        # NOTE: We are using QGIS native algorithm here before EIS Toolkit includes fuzzy memberships
        processing.runAndLoadResults(
            "native:fuzzifyrastersmallmembership",
            {
                'INPUT': input_raster,
                'BAND': 1,
                'FUZZYMIDPOINT': c,
                'FUZZYSPREAD': k,
                'OUTPUT': output_raster
            }
        )
