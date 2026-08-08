import pytest

from sim import (
    calc_aero_drag,
    calc_cycle_consumption,
    calc_grade_force,
    calc_inertial_force,
    calc_motor_electrical_power_in,
    calc_power_at_wheels,
    calc_road_load_force,
    calc_rolling_resistance,
    calc_tractive_force,
    calc_tractive_power,
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
        velocity_mps=v_mps, rho_kgm3=rho, coeff_drag=cd, x_section_area_m2=area
    )  # N

    # Assert
    assert current_drag == pytest.approx(286.400462962963)


def test_calc_rolling_resistance():
    # Arrange
    mass = 1300  # kg
    crr = 0.008  # coefficient
    theta = deg_to_rad(10)  # rads

    # Act
    rr = calc_rolling_resistance(
        mass_kg=mass, coeff_rolling_restistance=crr, theta_rads=theta
    )

    # Assert
    assert rr == pytest.approx(100.47402619331)


def test_calc_grade_force():
    # Arrange
    mass = 1300  # kg
    pos_theta = deg_to_rad(10)  # degs converted to rads
    neg_theta = deg_to_rad(-10)  # degs converted to rads

    # Act
    pos_grade_force = calc_grade_force(mass_kg=mass, theta_rads=pos_theta)
    neg_grade_force = calc_grade_force(mass_kg=mass, theta_rads=neg_theta)

    # Assert
    assert pos_grade_force == pytest.approx(2214.535209786)
    assert pos_grade_force > neg_grade_force
    assert pos_grade_force > 0
    assert neg_grade_force < 0


def test_calc_road_load_force():
    # Arrange
    mass = 1300  # kg
    theta = deg_to_rad(10)  # degs converted to rads
    v_mps = kph_to_mps(100)  # kph converted to m/s
    rho = 1.225  # kg.m^3
    cd = 0.3  # coefficient
    area = 2.02  # m^2
    crr = 0.008  # coefficient

    # Act
    road_load_force = calc_road_load_force(
        mass_kg=mass,
        theta_rads=theta,
        v_mps=v_mps,
        rho_kgm3=rho,
        cd=cd,
        x_section_area_m2=area,
        crr=crr,
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
    road_load_force = 2601.409698942273  # N
    inertial_force = 361.11111111  # N

    # Act
    total_tractive_force = calc_tractive_force(
        road_load_force_N=road_load_force, inertial_force_N=inertial_force
    )

    # Assert
    assert total_tractive_force == pytest.approx(2962.520810052272)


def test_calc_tractive_power():
    # Arrange
    tractive_force = 2962.520810052272  # N
    mass = 1300  # kg

    # Act
    tractive_power = calc_tractive_power(
        tractive_force_N=tractive_force, vehicle_mass_kg=mass
    )

    # Assert
    assert tractive_power == pytest.approx(3851277.0530679533)


def test_basic_drive_cycle_timestep():
    # Arrange
    a_car = {
        "mass": 1300,  # kg
        "cd": 0.3,  # coeff
        "area": 2.02,  # m^2
    }
    noddy_drive_cycle = {
        "rho": 1.225,
        "cycle": [
            (0, 0),
            (1, 0.5),
            (2, 1),
            (3, 1.4),
            (4, 3),
            (5, 4.7),
            (6, 2.3),
            (7, 0.4),
            (8, 0),
        ],
    }

    # Act
    consumption = calc_cycle_consumption(vehicle=a_car, drive_cycle=noddy_drive_cycle)

    # Assert
    assert consumption == pytest.approx(1)
