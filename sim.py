from math import cos, sin


def calc_aero_drag(
    velocity_mps: float, rho: float, coeff_drag: float, x_section_area: float
) -> float:
    return (rho / 2) * velocity_mps**2 * coeff_drag * x_section_area


def calc_rolling_resistance(
    mass: float, coeff_rolling_restistance: float, theta: float, g: float = 9.81
) -> float:
    # slope up is +ve theta
    return coeff_rolling_restistance * mass * g * cos(theta)


def calc_grade_force(mass: float, theta: float, g: float = 9.81) -> float:
    return sin(theta) * mass * g


def calc_road_load_force(
    grade_force: float, rolling_resistance: float, aero_drag: float
) -> float:
    return grade_force + rolling_resistance + aero_drag


def calc_power_at_wheels(road_load_force_N: float, velocity_mps: float) -> float:
    return road_load_force_N * velocity_mps


def calc_motor_electrical_power_in(
    mech_power_out_W: float, efficiency_percent: float
) -> float:
    return mech_power_out_W / efficiency_percent * 100


def calc_vehicle_acceleration_force(
    vehicle_mass_kg: float,
    initial_velocity_mps: float,
    final_velocity_mps: float,
    time_delta_secs: float,
):
    return (
        vehicle_mass_kg * (final_velocity_mps - initial_velocity_mps) / time_delta_secs
    )
