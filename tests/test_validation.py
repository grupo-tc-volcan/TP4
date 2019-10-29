""" 
    Testing functions to verify correct validation of the class
    AttFilterApproximator.

    1) Verify if filter types are detected correctly.
    2) Verify the designing mode is correct... by
    setting the value of order, q or just the template.
    3) For every mode of design, and filter type, cases.

    TargetClass: AttFilterApproximator
    Testing: Validation of the template data
"""

# Importing modules
from app.approximators.approximator import AttFilterApproximator
from app.approximators.approximator import ApproximationErrorCode


def test_invalid_types():

    def try_test(filter_type):
        app = AttFilterApproximator()
        app.type = filter_type
        return app.compute()

    assert try_test("low-pass") is not ApproximationErrorCode.INVALID_TYPE
    assert try_test("high-pass") is not ApproximationErrorCode.INVALID_TYPE
    assert try_test("band-pass") is not ApproximationErrorCode.INVALID_TYPE
    assert try_test("band-stop") is not ApproximationErrorCode.INVALID_TYPE
    assert try_test("kevin-dewald") is ApproximationErrorCode.INVALID_TYPE


def test_invalid_gain():
    
    def try_gain(gain_value):
        app = AttFilterApproximator()
        app.type = "low-pass"
        app.gain = gain_value
        return app.compute()
    
    assert try_gain(20) is not ApproximationErrorCode.INVALID_GAIN
    assert try_gain(0) is not ApproximationErrorCode.INVALID_GAIN
    assert try_gain(-20) is ApproximationErrorCode.INVALID_GAIN
    assert try_gain("A") is ApproximationErrorCode.INVALID_GAIN
    assert try_gain(None) is ApproximationErrorCode.INVALID_GAIN


def test_denormalisation():

    def try_denormalisation(denorm):
        app = AttFilterApproximator()
        app.type = "low-pass"
        app.gain = 0
        app.denorm = denorm
        return app.compute()

    assert try_denormalisation(-20) is ApproximationErrorCode.INVALID_DENORM
    assert try_denormalisation(0) is not ApproximationErrorCode.INVALID_DENORM
    assert try_denormalisation(50) is not ApproximationErrorCode.INVALID_DENORM
    assert try_denormalisation(100) is not ApproximationErrorCode.INVALID_DENORM
    assert try_denormalisation(110) is ApproximationErrorCode.INVALID_DENORM
    assert try_denormalisation("A") is ApproximationErrorCode.INVALID_DENORM
    assert try_denormalisation(None) is ApproximationErrorCode.INVALID_DENORM


def test_order():

    def try_order(order):
        app = AttFilterApproximator()
        app.type = "low-pass"
        app.gain = 0
        app.denorm = 0
        app.ord = order
        return app.compute()

    assert try_order(-2) is ApproximationErrorCode.INVALID_ORDER
    assert try_order(0) is not ApproximationErrorCode.INVALID_ORDER
    assert try_order(2) is not ApproximationErrorCode.INVALID_ORDER
    assert try_order(50) is ApproximationErrorCode.INVALID_ORDER
    assert try_order(None) is ApproximationErrorCode.INVALID_ORDER
    assert try_order("A") is ApproximationErrorCode.INVALID_ORDER


def test_low_pass_template():

    def try_low_pass(gain, denorm, fp, ap, fa, aa):
        app = AttFilterApproximator()
        app.type = "low-pass"
        app.gain = gain
        app.denorm = denorm
        app.fpl = fp
        app.fal = fa
        app.Apl = ap
        app.Aal = aa
        return app.compute()

    assert try_low_pass(gain=0, denorm=0, fp=100, ap=3, fa=1000, aa=20) is ApproximationErrorCode.UNDEFINED_APPROXIMATION
    assert try_low_pass(gain=-5, denorm=0, fp=100, ap=3, fa=1000, aa=20) is ApproximationErrorCode.INVALID_GAIN
    assert try_low_pass(gain=0, denorm=600, fp=100, ap=3, fa=1000, aa=20) is ApproximationErrorCode.INVALID_DENORM

    assert try_low_pass(gain=0, denorm=0, fp=-10, ap=3, fa=1000, aa=20) is ApproximationErrorCode.INVALID_FREQ
    assert try_low_pass(gain=0, denorm=0, fp=-15, ap=3, fa=-10, aa=20) is ApproximationErrorCode.INVALID_FREQ
    assert try_low_pass(gain=0, denorm=0, fp=10, ap=3, fa=-10, aa=20) is ApproximationErrorCode.INVALID_FREQ
    assert try_low_pass(gain=0, denorm=0, fp=100, ap=3, fa=10, aa=20) is ApproximationErrorCode.INVALID_FREQ

    assert try_low_pass(gain=0, denorm=0, fp=100, ap=-3, fa=1000, aa=20) is ApproximationErrorCode.INVALID_ATTE
    assert try_low_pass(gain=0, denorm=0, fp=100, ap=3, fa=1000, aa=-20) is ApproximationErrorCode.INVALID_ATTE
    assert try_low_pass(gain=0, denorm=0, fp=100, ap=-3, fa=1000, aa=-20) is ApproximationErrorCode.INVALID_ATTE
    assert try_low_pass(gain=0, denorm=0, fp=100, ap=30, fa=1000, aa=20) is ApproximationErrorCode.INVALID_ATTE
    assert try_low_pass(gain=0, denorm=0, fp=100, ap=0, fa=1000, aa=20) is ApproximationErrorCode.INVALID_ATTE
    assert try_low_pass(gain=0, denorm=0, fp=100, ap=10, fa=1000, aa=0) is ApproximationErrorCode.INVALID_ATTE


def test_high_pass_template():

    def try_high_pass(gain, denorm, fp, ap, fa, aa):
        app = AttFilterApproximator()
        app.type = "high-pass"
        app.gain = gain
        app.denorm = denorm
        app.fpl = fp
        app.fal = fa
        app.Apl = ap
        app.Aal = aa
        return app.compute()

    assert try_high_pass(gain=0, denorm=0, fp=1000, ap=3, fa=100, aa=20) is ApproximationErrorCode.UNDEFINED_APPROXIMATION
    assert try_high_pass(gain=-5, denorm=0, fp=100, ap=3, fa=1000, aa=20) is ApproximationErrorCode.INVALID_GAIN
    assert try_high_pass(gain=0, denorm=600, fp=100, ap=3, fa=1000, aa=20) is ApproximationErrorCode.INVALID_DENORM

    assert try_high_pass(gain=0, denorm=0, fp=-1000, ap=3, fa=100, aa=20) is ApproximationErrorCode.INVALID_FREQ
    assert try_high_pass(gain=0, denorm=0, fp=1000, ap=3, fa=-100, aa=20) is ApproximationErrorCode.INVALID_FREQ
    assert try_high_pass(gain=0, denorm=0, fp=-1000, ap=3, fa=-100, aa=20) is ApproximationErrorCode.INVALID_FREQ
    assert try_high_pass(gain=0, denorm=0, fp=1000, ap=3, fa=1100, aa=20) is ApproximationErrorCode.INVALID_FREQ

    assert try_high_pass(gain=0, denorm=0, fp=1000, ap=-3, fa=100, aa=20) is ApproximationErrorCode.INVALID_ATTE
    assert try_high_pass(gain=0, denorm=0, fp=1000, ap=3, fa=100, aa=-20) is ApproximationErrorCode.INVALID_ATTE
    assert try_high_pass(gain=0, denorm=0, fp=1000, ap=-3, fa=100, aa=-20) is ApproximationErrorCode.INVALID_ATTE
    assert try_high_pass(gain=0, denorm=0, fp=1000, ap=30, fa=100, aa=20) is ApproximationErrorCode.INVALID_ATTE
    assert try_high_pass(gain=0, denorm=0, fp=1000, ap=0, fa=100, aa=20) is ApproximationErrorCode.INVALID_ATTE
    assert try_high_pass(gain=0, denorm=0, fp=1000, ap=10, fa=100, aa=0) is ApproximationErrorCode.INVALID_ATTE


def test_band_pass_template():

    def try_band_pass(gain, denorm, fpl, fpr, apl, apr, fal, far, aal, aar):
        app = AttFilterApproximator()
        app.type = "band-pass"
        app.gain = gain
        app.denorm = denorm
        app.fpl = fpl
        app.fpr = fpr
        app.fal = fal
        app.far = far
        app.Apl = apl
        app.Apr = apr
        app.Aal = aal
        app.Aar = aar
        return app.compute()

    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.UNDEFINED_APPROXIMATION
    assert try_band_pass(gain=-5, denorm=0, fpl=3000, fpr=5000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_GAIN
    assert try_band_pass(gain=0, denorm=110, fpl=3000, fpr=5000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_DENORM

    assert try_band_pass(gain=0, denorm=0, fpl=-3000, fpr=5000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=-5000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=3, apr=3, fal=-1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=3, apr=3, fal=1000, far=-7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ

    assert try_band_pass(gain=0, denorm=0, fpl=5000, fpr=3000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=3, apr=3, fal=7000, far=1000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=8000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ
    assert try_band_pass(gain=0, denorm=0, fpl=100, fpr=5000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ

    assert try_band_pass(gain=0, denorm=0, fpl=0, fpr=5000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=0, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=3, apr=3, fal=0, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=3, apr=3, fal=1000, far=0, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ

    assert try_band_pass(gain=0, denorm=0, fpl=1000, fpr=5000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=7000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_FREQ

    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=-3, apr=3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_ATTE
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=3, apr=-3, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_ATTE
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=3, apr=3, fal=1000, far=7000, aal=-30, aar=30) is ApproximationErrorCode.INVALID_ATTE
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=3, apr=3, fal=1000, far=7000, aal=30, aar=-30) is ApproximationErrorCode.INVALID_ATTE
    assert try_band_pass(gain=0, denorm=0, fpl=3000, fpr=5000, apl=33, apr=33, fal=1000, far=7000, aal=30, aar=30) is ApproximationErrorCode.INVALID_ATTE


def test_band_stop_template():
    pass


def test_fixed_order():
    pass


def test_max_q():
    pass
