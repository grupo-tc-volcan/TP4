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


def test_by_fixed_order():
    butter = ButterworthApprox()

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


def test_by_max_q():
    butter = ButterworthApprox()

    butter.type = "low-pass"
    butter.gain = 0
    butter.fpl = 1000
    butter.Apl = 2

    results = []
    for max_q in np.linspace(0.1, 0.6, 20):
        butter.q = max_q

        print("Using MaxQ={} and Order={}".format(max_q, butter.ord))
        if butter.compute() is ApproximationErrorCode.OK:
            for pole in butter.get_zpk()[1]:
                print("fo: {} Q: {}".format(
                    butter.calculate_frequency(pole),
                    butter.calculate_selectivity(pole)
                ))
            print("\n")
            results.append(("Butterworth MaxQ={}".format(max_q), butter.h_denorm))
        else:
            input("[ERROR] => {}".format(butter.error_code))

    plot_results(results)


def test_by_template_denorm():
    butter = ButterworthApprox()

    butter.type = "low-pass"
    butter.gain = 0

    butter.fpl = 1000
    butter.Apl = 2
    butter.fal = 10000
    butter.Aal = 20

    results = []
    for denorm in range(0, 101, 10):
        butter.denorm = denorm if denorm != 0 else 1

        if butter.compute() is ApproximationErrorCode.OK:
            results.append(("Butterworth Denorm={}".format(denorm), butter.h_denorm))
        else:
            input("[ERROR] => {}".format(butter.error_code))

    plot_results(results)


def test_by_template(
        filter_type,
        fpl=0, fpr=0,
        apl=0, apr=0,
        fal=0, far=0,
        aal=0, aar=0
):
    butter = ButterworthApprox()

    butter.type = filter_type
    butter.gain = 0

    butter.fpl = fpl
    butter.fpr = fpr
    butter.fal = fal
    butter.far = far

    butter.Apl = apl
    butter.Apr = apr

    butter.Aal = aal
    butter.Aar = aar

    results = []
    if butter.compute() is ApproximationErrorCode.OK:
        results.append(
            ("Butterworth fp={} fa={} Ap={} Aa={}".format(
                butter.fpl,
                butter.fal,
                butter.Apl,
                butter.Aal
            ),
             butter.h_denorm)
        )
    else:
        input("[ERROR] => {}".format(butter.error_code))
    plot_results(results)


if __name__ == "__main__":

    test_by_template(
        "band-pass",
        fpl=4000,
        fpr=6000,
        apl=2,
        apr=2,
        fal=1000,
        far=10000,
        aal=10,
        aar=10
    )

    test_by_template(
        "band-stop",
        fal=2500,
        far=4000,
        apl=2,
        apr=2,
        fpl=1000,
        fpr=10000,
        aal=10,
        aar=10
    )

    test_by_template(
        "high-pass",
        fpl=3000,
        apl=2,
        fal=1000,
        aal=10
    )

    test_by_template(
        "low-pass",
        fpl=1000,
        apl=2,
        fal=3000,
        aal=10
    )

    test_by_template_denorm()

    test_by_fixed_order()

    test_by_max_q()
