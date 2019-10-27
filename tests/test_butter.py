# Project modules
from app.approximators.butterworth import ButterworthApprox
from app.approximators.approximator import ApproximationErrorCode

# Third-Party modules
from matplotlib import pyplot
from scipy import signal

# Python native modules


def test_butter_by_template():
    butter = ButterworthApprox()

    butter.type = "low-pass"
    butter.gain = 0
    butter.fpl = 1000
    butter.Apl = 2
    butter.ord = 3
    
    test_compute(butter)


def test_compute(approximator):
    error = approximator.compute()
    if error is ApproximationErrorCode.OK:
        plot_transfer_function(approximator.h_denorm)
    else:
        print("[ERROR] -> {}".format(error))


def plot_transfer_function(h):
    pyplot.figure()
    w, m, p = signal.bode(h, n=100000)
    pyplot.semilogx(w, m)
    pyplot.show()

    input("Press to exit...")


if __name__ == "__main__":

    test_butter_by_template()
