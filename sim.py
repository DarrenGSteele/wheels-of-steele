from math import cos, sin


def calc_aero_drag(
    velocity_mps: float, rho_kgm3: float, coeff_drag: float, x_section_area_m2: float
) -> float:
    return (rho_kgm3 / 2) * velocity_mps**2 * coeff_drag * x_section_area_m2


def calc_rolling_resistance(
    mass_kg: float, coeff_rolling_restistance: float, theta_rads: float, g: float = 9.81
) -> float:
    # slope up is +ve theta
    return coeff_rolling_restistance * mass_kg * g * cos(theta_rads)


def calc_grade_force(mass_kg: float, theta_rads: float, g: float = 9.81) -> float:
    return sin(theta_rads) * mass_kg * g


def calc_road_load_force(
    mass_kg: float,
    theta_rads: float,
    v_mps: float,
    rho_kgm3: float,
    cd: float,
    x_section_area_m2: float,
    crr: float,
) -> float:
    return (
        calc_grade_force(mass_kg, theta_rads)
        + calc_rolling_resistance(
            mass_kg=mass_kg, coeff_rolling_restistance=crr, theta_rads=theta_rads
        )
        + calc_aero_drag(
            velocity_mps=v_mps,
            rho_kgm3=rho_kgm3,
            coeff_drag=cd,
            x_section_area_m2=x_section_area_m2,
        )
    )


def calc_steady_state_power_at_wheels(
    road_load_force_N: float, velocity_mps: float
) -> float:
    return road_load_force_N * velocity_mps


def calc_motor_electrical_power_in(
    mech_power_out_W: float, efficiency_percent: float
) -> float:
    return mech_power_out_W / efficiency_percent * 100


def calc_inertial_force(
    vehicle_mass_kg: float,
    initial_velocity_mps: float,
    final_velocity_mps: float,
    time_delta_secs: float,
) -> float:
    return (
        vehicle_mass_kg * (final_velocity_mps - initial_velocity_mps) / time_delta_secs
    )


def calc_tractive_force(inertial_force_N: float, road_load_force_N: float) -> float:
    return inertial_force_N + road_load_force_N


def calc_tractive_power(velocity_mps: float, tractive_force_N: float) -> float:
    return tractive_force_N * velocity_mps


def calc_cycle_consumption(vehicle: dict, drive_cycle: dict) -> float:
    consumption_j = 0
    for dt in drive_cycle["cycle"]:
        consumption_j += calc_tractive_power(
            vehicle["mass"],
        )
    return consumption_j
