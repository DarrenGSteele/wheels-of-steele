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


def calc_power_at_wheels(road_load_force: float, velocity: float) -> float:
    return road_load_force * velocity


def calc_electrical_power(mech_power: float, efficiency_percent: float) -> float:
    return mech_power * efficiency_percent / 100
