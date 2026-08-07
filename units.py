from math import pi


def deg_to_rad(deg: float) -> float:
    return deg / 360 * 2 * pi


def kph_to_mps(v_kph: float) -> float:
    return v_kph * 1000 / 3600
