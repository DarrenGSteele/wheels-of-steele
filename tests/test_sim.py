from math import pi

import pytest

from sim import aero_drag, rolling_resistance


def test_aero_drag_force():
    # Arrange
    v = 100 * 1000 / 3600  # m/s
    rho = 1.225  # kg.m^3
    cd = 0.3  # coefficient
    area = 2.02  # m^2

    # Act
    current_drag = aero_drag(v, rho, cd, area)  # N

    # Assert
    # assert(current_drag == 286.4)
    assert current_drag == pytest.approx(286.400462962963)


def test_rolling_resistance():
    # Arrange
    mass = 1300  # kg
    crr = 0.008  # coefficient
    theta = 10 / 360 * 2 * pi  # rads

    # Act
    rr = rolling_resistance(mass, crr, theta)

    # Assert
    assert rr == pytest.approx(100.47402619331)
