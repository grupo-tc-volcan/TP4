# Third-party modules
from scipy import signal
from scipy import special

from numpy import *

# filters-tool project modules
from app.approximators.approximator import AttFilterApproximator
from app.approximators.approximator import ApproximationErrorCode

# Constant values
CONSIDERED_ZERO_LIMIT = 1e-10


class LegendreApprox(AttFilterApproximator):

    def __init__(self):
        super(LegendreApprox, self).__init__()

    # ------------------------- #
    #  Internal Public Methods  #
    # ------------------------- #

    def compute_normalised_by_order(self, ap, n) -> ApproximationErrorCode:
        """ Generates normalised transfer function prioritising the fixed order """
        # Computing needed constants from Legendre Approximation
        epsilon = LegendreApprox.compute_epsilon(ap) ** 2
        ln = LegendreApprox.compute_odd_integrated_polynomial(n) if (n % 2) else LegendreApprox.compute_even_integrated_polynomial(n)
        ln = epsilon * ln
        den = polyadd(poly1d([1]), ln)

        # Normalised transfer function
        new_gain = 1
        new_poles = []
        for pole in 1j * den.roots:
            if pole.real < 0:
                new_pole = complex(
                    pole.real if abs(pole.real) > CONSIDERED_ZERO_LIMIT else 0,
                    pole.imag if abs(pole.imag) > CONSIDERED_ZERO_LIMIT else 0
                )
                new_gain /= abs(new_pole)
                new_poles.append(new_pole)

        # Updating state of transfer function
        self.h_norm = signal.ZerosPolesGain([], new_poles, new_gain)
        return ApproximationErrorCode.OK

    # ----------------- #
    #  Private Methods  #
    # ----------------- #

    @staticmethod
    def compute_epsilon(ap):
        """ Returns the epsilon factor using Legendre approximation """
        return sqrt(10 ** (ap / 10) - 1)

    @staticmethod
    def compute_even_integrated_polynomial(n):
        """ Returns the integrated series of Legendre polynomial till the given order when is  even."""
        if (n % 2) == 0:
            # First, calculate the integration polynomial as a sum of legendre polynomials
            k = n // 2 - 1
            b0 = 1 / sqrt((k + 1) * (k + 2))
            poly = poly1d([b0 if (k % 2) == 0 else 0])

            for i in range(1, k + 1):
                if ((k % 2) == 1 and (i % 2) == 0) or ((k % 2) == 0 and (i % 2) == 1):
                    continue
                bi = b0 * (2 * i + 1)
                new_poly = bi * LegendreApprox.compute_polynomial(i)
                poly = polyadd(poly, new_poly)

            poly = polymul(poly, poly)
            poly = polymul(poly, poly1d([1, 1]))

            # Calculate the indefinite integration and upper/lower limits
            poly = polyint(poly)
            upper = poly1d([2, 0, -1])
            lower = poly1d([-1])

            # Using barrow and returning the result!
            return polysub(polyval(poly, upper), polyval(poly, lower))
        return None

    @staticmethod
    def compute_odd_integrated_polynomial(n):
        """ Returns the integrated series of Legendre polynomial till the given order when is odd """
        if n % 2:
            # First, calculate the integration polynomial as a sum of legendre polynomials
            k = (n - 1) // 2
            a0 = 1 / (sqrt(2) * (k + 1))
            poly = poly1d([a0])

            for i in range(1, k + 1):
                ai = a0 * (2 * i + 1)
                poli = LegendreApprox.compute_polynomial(i)
                new_poly = ai * poli
                poly = polyadd(poly, new_poly)

            poly = polymul(poly, poly)

            # Calculate the indefinite integration and upper/lower limits
            poly = polyint(poly)
            upper = poly1d([2, 0, -1])
            lower = poly1d([-1])

            # Using barrow and returning the result!
            return polysub(polyval(poly, upper), polyval(poly, lower))
        return None

    @staticmethod
    def compute_polynomial(n):
        """ Returns the polynomial of n-th order from Legendre """
        if n > 0:
            return special.legendre(n)
        return None
