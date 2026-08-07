from math import cos


def aero_drag(v, rho, cd, area):
    return (rho / 2) * v**2 * cd * area


def rolling_resistance(mass, crr, theta, g: float = 9.81):
    return crr * mass * g * cos(theta)
