from math import cos, sin


def aero_drag(velocity: float, rho: float, coeff_drag: float, x_section_area) -> float:
    return (rho / 2) * velocity**2 * coeff_drag * x_section_area


def rolling_resistance(
    mass: float, coeff_rolling_restistance: float, theta: float, g: float = 9.81
) -> float:
    # slope up is +ve theta
    return coeff_rolling_restistance * mass * g * cos(theta)


def grade_force(mass: float, theta: float, g: float = 9.81) -> float:
    return sin(theta) * mass * g
