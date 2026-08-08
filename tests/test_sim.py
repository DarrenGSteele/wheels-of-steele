import pytest

from sim import (
    calc_aero_drag,
    calc_grade_force,
    calc_inertial_force,
    calc_motor_electrical_power_in,
    calc_power_at_wheels,
    calc_road_load_force,
    calc_rolling_resistance,
    calc_tractive_force,
)
from units import deg_to_rad, kph_to_mps


def test_calc_aero_drag_force():
    # Arrange
    v_mps = kph_to_mps(100)  # kph converted to m/s
    rho = 1.225  # kg.m^3
    cd = 0.3  # coefficient
    area = 2.02  # m^2

    # Act
    current_drag = calc_aero_drag(
        velocity_mps=v_mps, rho=rho, coeff_drag=cd, x_section_area=area
    )  # N

    # Assert
    # assert(current_drag == 286.4)
    assert current_drag == pytest.approx(286.400462962963)


def test_calc_rolling_resistance():
    # Arrange
    mass = 1300  # kg
    crr = 0.008  # coefficient
    theta = deg_to_rad(10)  # rads

    # Act
    rr = calc_rolling_resistance(mass, crr, theta)

    # Assert
    assert rr == pytest.approx(100.47402619331)


def test_calc_grade_force():
    # Arrange
    mass = 1300  # kg
    pos_theta = deg_to_rad(10)  # degs converted to rads
    neg_theta = deg_to_rad(-10)  # degs converted to rads

    # Act
    pos_grade_force = calc_grade_force(mass, pos_theta)
    neg_grade_force = calc_grade_force(mass, neg_theta)

    # Assert
    assert pos_grade_force == pytest.approx(2214.535209786)
    assert pos_grade_force > neg_grade_force
    assert pos_grade_force > 0
    assert neg_grade_force < 0


def test_calc_road_load_force():
    # Arrange
    grade_force = 2214.535209786  # N
    aero_drag = 286.400462962963  # N
    rolling_resistance = 100.47402619331  # N

    # Act
    road_load_force = calc_road_load_force(
        grade_force=grade_force,
        aero_drag=aero_drag,
        rolling_resistance=rolling_resistance,
    )

    # Assert
    assert road_load_force == pytest.approx(2601.409698942273)


def test_calc_power_at_wheels():
    # Arrange
    road_load_force = 2601.409698942273  # N
    velocity = kph_to_mps(100)  # m/s

    # Act
    power_at_wheels = calc_power_at_wheels(
        road_load_force_N=road_load_force, velocity_mps=velocity
    )

    # Assert
    assert power_at_wheels == pytest.approx(72261.38052617425)


def test_calc_motor_electrical_power_in():
    # Arrange
    power_at_wheels = 72261.38052617425  # Watts
    effy = 98  # percentage

    # Act
    elec_power_into_motor = calc_motor_electrical_power_in(
        mech_power_out_W=power_at_wheels, efficiency_percent=effy
    )

    # Assert
    assert elec_power_into_motor == pytest.approx(73736.1025777288)


@pytest.mark.parametrize(
    "v1_kph, v2_kph",
    [
        (100, 101),
        (10, 11),
        (150, 151),
    ],
)
def test_calc_inertial_force_independent_of_speed(v1_kph, v2_kph):
    # Arrange
    mass = 1300  # kg
    dt = 1  # sec

    # Act
    force = calc_inertial_force(
        vehicle_mass_kg=mass,
        initial_velocity_mps=kph_to_mps(v1_kph),
        final_velocity_mps=kph_to_mps(v2_kph),
        time_delta_secs=dt,
    )

    # Assert
    assert force == pytest.approx(361.11111111)


def test_calc_tractive_force():
    # Arrange
    road_load_force = 2601.409698942273
    inertial_force = 361.11111111  # N

    # Act
    total_tractive_force = calc_tractive_force(
        road_load_force_N=road_load_force, inertial_force_N=inertial_force
    )

    # Assert
    assert total_tractive_force == pytest.approx(2962.520810052272)
