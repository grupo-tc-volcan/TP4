# Project modules
from app.approximators.butterworth import ButterworthApprox
from app.approximators.approximator import ApproximationErrorCode

# Third-Party modules
from matplotlib import pyplot
from scipy import signal

# Python native modules
import numpy as np


def plot_results(results):
    pyplot.figure()
    for name, h in results:
        w, m, p = signal.bode(h, n=100000)
        pyplot.semilogx(w / (2 * np.pi), m, label="{}".format(name))
    pyplot.legend()
    pyplot.show()

    input("Press to exit...")


def test_by_fixed_order():
    butter = ButterworthApprox()

    print("Testing by fixed order...")

    butter.type = "low-pass"
    butter.gain = 0
    butter.fpl = 1000
    butter.Apl = 2

    results = []
    for order in range(1, 20):
        butter.ord = order

        if butter.compute() is ApproximationErrorCode.OK:
            results.append(("Butterworth n={}".format(order), butter.h_denorm))
        else:
            input("[ERROR] => {}".format(butter.error_code))

    plot_results(results)


if __name__ == "__main__":
    pass
