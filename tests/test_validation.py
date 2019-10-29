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
    pass


def test_high_pass_template():
    pass


def test_band_pass_template():
    pass


def test_band_stop_template():
    pass


def test_fixed_order():
    pass


def test_max_q():
    pass