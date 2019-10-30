# Project modules
from app.approximators.butterworth import ButterworthApprox
from app.approximators.chebyshev_i import ChebyshevIApprox
from app.approximators.chebyshev_ii import ChebyshevIIApprox
from app.approximators.legendre import LegendreApprox
from app.approximators.cauer import CauerApprox

from app.approximators.approximator import ApproximationErrorCode

# Third-Party modules
from matplotlib import pyplot
from scipy import signal
import pytest

# Python native modules
import numpy as np


# --------------------------- #
#  DECLARING USEFUL ELEMENTS  #
# --------------------------- #

@pytest.fixture
def approximator():
    # Change the returning approximation to test it!
    return ChebyshevIIApprox()


def run_by_template(
        approximator,
        filter_type,
        fpl=0, fpr=0,
        apl=0, apr=0,
        fal=0, far=0,
        aal=0, aar=0,
        gain=0,
        graph="bode"    # other case should be zpk
):
    approximator.type = filter_type
    approximator.gain = gain

    approximator.fpl = fpl
    approximator.fpr = fpr
    approximator.fal = fal
    approximator.far = far

    approximator.Apl = apl
    approximator.Apr = apr

    approximator.Aal = aal
    approximator.Aar = aar

    results = []
    if approximator.compute() is ApproximationErrorCode.OK:
        results.append(("Denormalised", approximator.h_denorm))
        results.append(("Normalised", approximator.h_norm))
    else:
        input("[ERROR] => {}".format(approximator.error_code))

    if graph == "bode":
        plot_bode_results(results)
    elif graph == "zpk":
        plot_zpk_results(results)


def plot_bode_results(results):
    pyplot.figure()
    for name, h in results:
        w, m, p = signal.bode(h, n=100000)
        pyplot.semilogx(w / (2 * np.pi), m, label="{}".format(name))
    pyplot.legend()
    pyplot.show()


def plot_zpk_results(results):
    colors = ["red", "blue", "green"]

    fig, (poles_plot, zeros_plot) = pyplot.subplots(1, 2)
    fig.suptitle('Diagrama de polos y ceros')

    for index, (name, transfer) in enumerate(results):
        zeros = transfer.zeros
        poles = transfer.poles
        gain = transfer.gain

        x_poles = [pole.real for pole in poles]
        y_poles = [pole.imag for pole in poles]
        x_zeros = [zero.real for zero in zeros]
        y_zeros = [zero.imag for zero in zeros]

        poles_plot.scatter(x_poles, y_poles, label=name, marker='x', c=colors[index])
        zeros_plot.scatter(x_zeros, y_zeros, label=name, marker='o', c=colors[index])

    poles_plot.set_xlabel('Parte real σ (Np)')
    poles_plot.set_ylabel('Parte imaginaria jω (Hz)')
    poles_plot.set_title('Polos')
    poles_plot.ticklabel_format(axis='both', scilimits=(-2, 2))
    poles_plot.grid()
    poles_plot.autoscale()

    zeros_plot.set_xlabel('Parte real σ (Np)')
    zeros_plot.set_ylabel('Parte imaginaria jω (Hz)')
    zeros_plot.set_title('Ceros')
    zeros_plot.ticklabel_format(axis='both', scilimits=(-2, 2))
    zeros_plot.grid()
    zeros_plot.autoscale()

    pyplot.legend()
    pyplot.show()


# ------------ #
# TEST MODULES #
# ------------ #
def test_by_fixed_order(approximator):
    approximator.type = "low-pass"
    approximator.gain = 0
    approximator.fpl = 1000
    approximator.Apl = 3.5
    approximator.Aal = 10

    results = []
    for order in range(1, 6):
        approximator.ord = order

        if approximator.compute() is ApproximationErrorCode.OK:
            results.append(("Denormalised n={}".format(order), approximator.h_denorm))
            results.append(("Normalised n={}".format(order), approximator.h_norm))
        else:
            print("[ERROR] => {}".format(approximator.error_code))

    plot_bode_results(results)
    plot_zpk_results(results)


def test_by_max_q(approximator):
    approximator.type = "low-pass"
    approximator.gain = 0
    approximator.fpl = 1000
    approximator.fal = 10000
    approximator.Aal = 20
    approximator.Apl = 2

    results = []
    for max_q in np.linspace(0.1, 10, 20):
        approximator.q = max_q

        if approximator.compute() is ApproximationErrorCode.OK:
            print("Using MaxQ={} and Order={}".format(max_q, len(approximator.get_zpk().poles)))
            for pole in approximator.get_zpk().poles:
                print("fo: {} Q: {}".format(
                    approximator.calculate_frequency(pole),
                    approximator.calculate_selectivity(pole)
                ))
            print("\n")
            results.append(("Approximation MaxQ={}".format(max_q), approximator.h_denorm))
        else:
            print("[ERROR] => {}".format(approximator.error_code))

    plot_bode_results(results)


def test_by_template_denorm(approximator):
    approximator.type = "low-pass"
    approximator.gain = 0

    approximator.fpl = 1000
    approximator.Apl = 2
    approximator.fal = 10000
    approximator.Aal = 20

    results = []
    for denorm in [0, 100]:
        approximator.denorm = denorm if denorm != 0 else 1

        if approximator.compute() is ApproximationErrorCode.OK:
            results.append(("Approximation Denorm={}".format(denorm), approximator.h_denorm))
            results.append(("Approximation Norm={}".format(denorm), approximator.h_norm))
        else:
            print("[ERROR] => {}".format(approximator.error_code))

    plot_bode_results(results)


def test_band_pass(approximator):
    run_by_template(
        approximator,
        "band-pass",
        fpl=4000,
        fpr=6000,
        apl=2,
        apr=2,
        fal=1000,
        far=10000,
        aal=10,
        aar=10,
        gain=0,
        graph="bode"
    )

    run_by_template(
        approximator,
        "band-pass",
        fpl=4000,
        fpr=6000,
        apl=2,
        apr=2,
        fal=1000,
        far=10000,
        aal=10,
        aar=10,
        gain=0,
        graph="zpk"
    )


def test_band_stop(approximator):
    run_by_template(
        approximator,
        "band-stop",
        fal=2500,
        far=4000,
        apl=2,
        apr=2,
        fpl=2300,
        fpr=4200,
        aal=10,
        aar=10,
        graph="bode"
    )

    run_by_template(
        approximator,
        "band-stop",
        fal=2500,
        far=4000,
        apl=2,
        apr=2,
        fpl=2300,
        fpr=4200,
        aal=10,
        aar=10,
        graph="zpk"
    )


def test_high_pass(approximator):
    run_by_template(
        approximator,
        "high-pass",
        fpl=1500,
        apl=2,
        fal=1000,
        aal=30,
        graph="bode"
    )

    run_by_template(
        approximator,
        "high-pass",
        fpl=1500,
        apl=2,
        fal=1000,
        aal=30,
        graph="zpk"
    )


def test_low_pass(approximator):
    run_by_template(
        approximator,
        "low-pass",
        fpl=1000,
        apl=2,
        fal=1500,
        aal=50,
        graph="bode"
    )

    run_by_template(
        approximator,
        "low-pass",
        fpl=1000,
        apl=2,
        fal=1500,
        aal=50,
        graph="zpk"
    )
