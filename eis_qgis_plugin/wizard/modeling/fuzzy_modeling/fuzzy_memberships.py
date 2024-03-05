import numpy as np
from qgis.gui import QgsDoubleSpinBox

# sns.set_theme(style="white")
# plt.figure(figsize=(10, 6))
# plt.title('Gaussian Membership Function')
# plt.xlabel('x')
# plt.ylabel('Membership Value')
# plt.show()


class FuzzyMembership:
    
    def x_range():
        raise NotImplementedError("x_range method should be implemented in child class.")

    def membership_function():
        raise NotImplementedError("membership_function method should be implemented in child class.")

    def get_param_values(self):
        raise NotImplementedError("get_param_values method should be implemented in child class.")

    def reset_defaults(self):
        [widget.setValue(value) for widget, value in self.defaults.items()]

    def compute():
        raise NotImplementedError("get_param_values method should be implemented in child class.")


class GaussianMembership(FuzzyMembership):

    def __init__(self, c: QgsDoubleSpinBox, sigma: QgsDoubleSpinBox):
        self.c = c
        self.sigma = sigma
        self.defaults = {self.c: 10.0, self.sigma: 0.01}

    def get_param_values(self):
        return self.c.value(), self.sigma.value() 

    @staticmethod
    def x_range(c, sigma):
        return np.linspace(c - 4*sigma, c + 4*sigma, num=500)
    
    @staticmethod
    def membership_function(x, c, sigma):
        return np.exp(-((x - c) ** 2) / (2 * sigma ** 2))

    def compute(c, sigma, input_raster, output_raster):
        # TODO
        pass


class LargeMembership(FuzzyMembership):

    def __init__(self, c: QgsDoubleSpinBox, k: QgsDoubleSpinBox):
        self.c = c
        self.k = k
        self.defaults = {self.c: 50, self.k: 5}

    def get_param_values(self):
        return self.c.value(), self.k.value()

    @staticmethod
    def x_range(c, k):
        spread_factor = 1 / k * 10
        return np.linspace(c - spread_factor, c + spread_factor, num=500)

    @staticmethod
    def membership_function(x, c, k):
        return 1 / (1 + np.exp(-k * (x - c)))
    
    def compute(c, k, input_raster, output_raster):
        # TODO
        pass


class LinearMembership(FuzzyMembership):

    def __init__(self, a: QgsDoubleSpinBox, b: QgsDoubleSpinBox):
        self.a = a
        self.b = b
        self.defaults = {self.a: 0, self.b: 1}

    def get_param_values(self):
        return self.a.value(), self.b.value()

    @staticmethod
    def x_range(a, b):
        return np.linspace(a, b, num=500)

    @staticmethod
    def membership_function(x, a, b):
        return np.clip((x - a) / (b - a), 0, 1)
    
    def compute(a, b, input_raster, output_raster):
        # TODO
        pass


class NearMembership(FuzzyMembership):

    def __init__(self, c: QgsDoubleSpinBox, k: QgsDoubleSpinBox):
        self.c = c
        self.k = k
        self.defaults = {self.c: 50, self.k: 5}

    def get_param_values(self):
        return self.c.value(), self.k.value()

    @staticmethod
    def x_range(c, k):
        spread_factor = max(1 / k * 10, 0.1)  # Ensure there's always some range
        return np.linspace(c - spread_factor, c + spread_factor, num=500)

    @staticmethod
    def membership_function(x, c, k):
        return np.exp(-k * (x - c) ** 2)
    
    def compute(c, k, input_raster, output_raster):
        # TODO
        pass
    

class PowerMembership(FuzzyMembership):

    def __init__(self, a: QgsDoubleSpinBox, b: QgsDoubleSpinBox, alpha: QgsDoubleSpinBox):
        self.a = a
        self.b = b
        self.alpha = alpha
        self.defaults = {self.a: 0, self.b: 1, self.alpha: 2}

    def get_param_values(self):
        return self.a.value(), self.b.value(), self.alpha.value()

    @staticmethod
    def x_range(a, b, _):
        return np.linspace(a, b, num=500)

    @staticmethod
    def membership_function(x, a, b, alpha):
        return np.clip(1 - ((x - a) / (b - a)) ** alpha, 0, 1)
    
    def compute(a, b, input_raster, output_raster):
        # TODO
        pass


class SmallMembership(FuzzyMembership):

    def __init__(self, c: QgsDoubleSpinBox, k: QgsDoubleSpinBox):
        self.c = c
        self.k = k
        self.defaults = {self.c: 50, self.k: 5}

    def get_param_values(self):
        return self.c.value(), self.k.value(),

    @staticmethod
    def x_range(c, k):
        spread_factor = 1 / k * 10
        return np.linspace(c - spread_factor, c + spread_factor, num=500)

    @staticmethod
    def _large_membership_function(x, c, k):
        return 1 / (1 + np.exp(-k * (x - c)))

    def membership_function(self, x, c, k):
        return 1 - self._large_membership_function(x, c, k)
    
    def compute(c, k, input_raster, output_raster):
        # TODO
        pass
