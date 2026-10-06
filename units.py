from math import pi

def deg_to_rad(deg: float) -> float:
    return deg / 360 * 2 * pi

def kph_to_mps(v_kph: float) -> float:
    return v_kph * 1000 / 3600

def J_to_kWh(J: float) -> float:
    return J / (1000 * 3600)

def m_to_km(m: float) -> float:
    return m / 1000

def Jpm_to_kWhpkm(Jpm: float) -> float:
    return (J_to_kWh(Jpm))*1000