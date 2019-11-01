# Third-party modules
from scipy import prod, asarray, amin
from numpy import unwrap
from numpy import diff
from numpy import log
from numpy import divide
from numpy import where
from numpy import pi
from numpy import amax
from numpy import angle
import scipy.signal as ss
import numpy as np
from scipy.special import factorial

# filters-tool project modules
from app.approximators.approximator import GroupDelayFilterApproximator
from app.approximators.approximator import ApproximationErrorCode


class GaussApprox(GroupDelayFilterApproximator):

    def __init__(self):
        super(GaussApprox, self).__init__()

    # -------------------------#
    # Internal Public Methods #
    # -------------------------#

    def compute_normalised_by_order(self, gdn, wfn, order) -> ApproximationErrorCode:
        z, p, k = self._gauss_norm(order)
        self.h_norm = ss.ZerosPolesGain(z, p, k)
        self.adjust_function_gain(self.h_norm, 1)
        return ApproximationErrorCode.OK

    # -----------------#
    # Private Methods #
    # -----------------#

    def _denormalised_transfer_function(self):
        z, p, k = self._gauss_des(self.h_norm.zeros, self.h_norm.poles)
        self.h_denorm = ss.ZerosPolesGain(z, p, k)
        self.adjust_function_gain(self.h_denorm, np.float_power(10, np.divide(self.gain,20)))
        return ApproximationErrorCode.OK

    def _gauss_norm(self, n: int):
        """ Returns zeros, poles and gain of Gauss normalized approximation """
        transfer_function = self._get_tf(n)
        trans_zpk = transfer_function.to_zpk()
        z, p, k = trans_zpk.zeros, trans_zpk.poles, trans_zpk.gain
        w, h = ss.freqs_zpk(z, p, k)
        norm_gd = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
        trans_zpk.poles = trans_zpk.poles * norm_gd[0]
        trans_zpk.gain = np.prod(abs(trans_zpk.poles))
        return trans_zpk.zeros, trans_zpk.poles, trans_zpk.gain

    def _gauss_des(self, z_n, p_n):
        """ Returns zeros, poles and gain of Gauss denormalized approximation """

        p = p_n / (self.group_delay * 1e-3)  # user's group delay in ms
        k = prod(abs(p))
        w, h = ss.freqs_zpk([], p, k)
        #norm_gd = -diff(unwrap(angle(h))) / diff(w)
        #f_n = w / (2 * pi)
        #plt.semilogx(f_n[:-1], norm_gd)
        #plt.show()
        return z_n, p, k



    def _get_tf(self, n: int):
        """
        Returns the normalized transfer function of the Gauss Approximation
        :param n: Order of the gauss polynomial
        :return: Scipy signal transfer function
        """
        z, p, k = self._get_zpk(n)
        transfer_function = ss.ZerosPolesGain(z, p, k)
        return transfer_function

    @staticmethod
    def _get_zpk(n: int):
        """
        :param n: Gauss approximation order. N_MIN = 2
        :return: The Gauss Approximation Zeros, Poles and Gain
        """
        num = [1.]
        den = []
        for k in range(n, 0, -1):
            # den.append((-1)**k*gamma**k/factorial(k))
            den.append((-1) ** k / factorial(k, exact = True))  # normalizamos con gamma=1
            den.append(0)
        den.append(1.)
        transfer_function = ss.TransferFunction(num, den)  # tengo la transferencia al cuadrado
        p = transfer_function.poles
        p = p[np.where(
            p.real < -1e-10)]  # me quedo con los polos del semiplano izquierdo. -1e-10 xq sino n=7 me quedaba inestable, problema: queda de un orden menos para n impar!!!!!
        k = np.prod(abs(p))  # para que la ganancia sea 1
        return [], p, k
