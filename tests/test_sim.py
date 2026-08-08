import pytest

from sim import (
    Vehicle,
    calc_aero_drag_force_N,
    calc_cycle_consumption_J,
    calc_grade_force_N,
    calc_inertial_force_N,
    calc_motor_electrical_power_in_W,
    calc_road_load_force_N,
    calc_rolling_resistance_force_N,
    calc_steady_state_power_at_wheels_W,
    calc_tractive_force_N,
    calc_tractive_power_W,
)
from units import deg_to_rad, kph_to_mps


@pytest.fixture
def a_car() -> Vehicle:
    return Vehicle(
        mass_kg=1300,
        drag_coeff=0.3,
        x_sectional_area_m2=2.02,
        rolling_resistance_coeff=0.008,
    )


def test_calc_aero_drag_force(a_car):
    # Arrange
    v_mps = kph_to_mps(100)  # kph converted to m/s
    rho = 1.225  # kg.m^3

    # Act
    current_drag = calc_aero_drag_force_N(
        velocity_mps=v_mps,
        rho_kgm3=rho,
        drag_coeff=a_car.drag_coeff,
        x_sectional_area_m2=a_car.x_sectional_area_m2,
    )  # N

    # Assert
    assert current_drag == pytest.approx(286.400462962963)


def test_calc_rolling_resistance_force(a_car):
    # Arrange
    theta = deg_to_rad(10)  # rads

    # Act
    rr = calc_rolling_resistance_force_N(
        rolling_resistance_coeff=a_car.rolling_resistance_coeff,
        mass_kg=a_car.mass_kg,
        theta_rads=theta,
    )

    # Assert
    assert rr == pytest.approx(100.47402619331)


def test_calc_grade_force(a_car):
    # Arrange
    mass = a_car.mass_kg  # kg
    pos_theta = deg_to_rad(10)  # degs converted to rads
    neg_theta = deg_to_rad(-10)  # degs converted to rads

    # Act
    pos_grade_force = calc_grade_force_N(mass_kg=mass, theta_rads=pos_theta)
    neg_grade_force = calc_grade_force_N(mass_kg=mass, theta_rads=neg_theta)

    # Assert
    assert pos_grade_force == pytest.approx(2214.535209786)
    assert pos_grade_force > neg_grade_force
    assert pos_grade_force > 0
    assert neg_grade_force < 0


def test_calc_road_load_force(a_car):
    # Arrange
    theta = deg_to_rad(10)  # degs converted to rads
    v_mps = kph_to_mps(100)  # kph converted to m/s
    rho = 1.225  # kg.m^3

    # Act
    road_load_force = calc_road_load_force_N(
        vehicle=a_car,
        theta_rads=theta,
        v_mps=v_mps,
        rho_kgm3=rho,
    )

    # Assert
    assert road_load_force == pytest.approx(2601.409698942273)


def test_calc_steady_state_power_at_wheels(a_car):
    # Arrange
    theta = deg_to_rad(10)  # degs converted to rads
    v_mps = kph_to_mps(100)  # kph converted to m/s
    rho = 1.225  # kg.m^3

    # Act
    power_at_wheels = calc_steady_state_power_at_wheels_W(
        vehicle=a_car,
        theta_rads=theta,
        rho_kgm3=rho,
        velocity_mps=v_mps,
    )

    # Assert
    assert power_at_wheels == pytest.approx(72261.38052617425)


def test_calc_motor_electrical_power_in(a_car):
    # Arrange
    power_at_wheels = 72261.38052617425  # Watts
    effy = 98  # percentage

    # Act
    elec_power_into_motor = calc_motor_electrical_power_in_W(
        vehicle=a_car, mech_power_out_W=power_at_wheels, efficiency_percent=effy
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
def test_calc_inertial_force_independent_of_speed(a_car, v1_kph, v2_kph):
    # Arrange
    dt = 1  # sec

    # Act
    force = calc_inertial_force_N(
        vehicle_mass_kg=a_car.mass_kg,
        initial_velocity_mps=kph_to_mps(v1_kph),
        final_velocity_mps=kph_to_mps(v2_kph),
        time_delta_secs=dt,
    )

    # Assert
    assert force == pytest.approx(361.11111111)


def test_calc_tractive_force(a_car):
    # Arrange
    initial_velocity_mps = kph_to_mps(100)  # kph converted to m/s
    final_velocity_mps = kph_to_mps(101)  # kph converted to m/s
    time_delta_secs = 1  # secs
    theta = deg_to_rad(10)  # degs converted to rads
    rho = 1.225  # kg.m^3

    # Act
    total_tractive_force = calc_tractive_force_N(
        vehicle=a_car,
        initial_velocity_mps=initial_velocity_mps,
        final_velocity_mps=final_velocity_mps,
        time_delta_secs=time_delta_secs,
        theta_rads=theta,
        rho_kgm3=rho,
    )

    # Assert
    assert total_tractive_force == pytest.approx(2962.520810052272)


def test_calc_tractive_power(a_car):
    # Arrange
    initial_velocity_mps = kph_to_mps(100)  # kph converted to m/s
    final_velocity_mps = kph_to_mps(101)  # kph converted to m/s
    time_delta_secs = 1  # secs
    theta = deg_to_rad(10)  # degs converted to rads
    rho = 1.225  # kg.m^3

    # Act
    tractive_power = calc_tractive_power_W(
        vehicle=a_car,
        initial_velocity_mps=initial_velocity_mps,
        final_velocity_mps=final_velocity_mps,
        time_delta_secs=time_delta_secs,
        theta_rads=theta,
        rho_kgm3=rho,
    )

    # Assert
    assert tractive_power == pytest.approx(82292.24472367422)


def test_basic_drive_cycle_timestep(a_car):
    # Arrange
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
    consumption = calc_cycle_consumption_J(vehicle=a_car, drive_cycle=noddy_drive_cycle)

    # Assert
    assert consumption == pytest.approx(1)
