import pytest

from sim import aero_drag, grade_force, road_load_force, rolling_resistance
from units import deg_to_rad


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
    theta = deg_to_rad(10)  # rads

    # Act
    rr = rolling_resistance(mass, crr, theta)

    # Assert
    assert rr == pytest.approx(100.47402619331)


def test_grade_force():
    # Arrange
    mass = 1300  # kg
    pos_theta = deg_to_rad(10)  # degs converted to rads
    neg_theta = deg_to_rad(-10)  # degs converted to rads

    # Act
    pos_grade_force = grade_force(mass, pos_theta)
    neg_grade_force = grade_force(mass, neg_theta)

    # Assert
    assert pos_grade_force == pytest.approx(2214.535209786)
    assert pos_grade_force > neg_grade_force
    assert pos_grade_force > 0
    assert neg_grade_force < 0


def test_road_load_force():
    # Arrange
    grade_force = 2214.535209786
    aero_drag = 286.400462962963
    rolling_resistance = 100.47402619331

    # Act
    rl_force = road_load_force(grade_force, aero_drag, rolling_resistance)

    # Assert
    assert rl_force == pytest.approx(2601.409698942273)
