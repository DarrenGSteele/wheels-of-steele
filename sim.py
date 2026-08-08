from dataclasses import dataclass
from itertools import pairwise
from math import cos, sin


@dataclass(frozen=True)
class Vehicle:
    mass_kg: float
    drag_coeff: float
    x_sectional_area_m2: float
    rolling_resistance_coeff: float


@dataclass(frozen=True)
class DriveCycle:
    rho_kgpm3: float
    speed_trace: list[tuple]


def calc_aero_drag_force_N(
    velocity_mps: float, rho_kgpm3: float, drag_coeff: float, x_sectional_area_m2: float
) -> float:
    return (rho_kgpm3 / 2) * velocity_mps**2 * drag_coeff * x_sectional_area_m2


def calc_rolling_resistance_force_N(
    rolling_resistance_coeff: float, mass_kg: float, theta_rads: float, g: float = 9.81
) -> float:
    # slope up is +ve theta
    return rolling_resistance_coeff * mass_kg * g * cos(theta_rads)


def calc_grade_force_N(mass_kg: float, theta_rads: float, g: float = 9.81) -> float:
    return sin(theta_rads) * mass_kg * g


def calc_inertial_force_N(
    vehicle_mass_kg: float,
    initial_velocity_mps: float,
    final_velocity_mps: float,
    time_delta_secs: float,
) -> float:
    return (
        vehicle_mass_kg * (final_velocity_mps - initial_velocity_mps) / time_delta_secs
    )


def calc_road_load_force_N(
    vehicle: Vehicle,
    theta_rads: float,
    v_mps: float,
    rho_kgpm3: float,
) -> float:
    return (
        calc_grade_force_N(mass_kg=vehicle.mass_kg, theta_rads=theta_rads)
        + calc_rolling_resistance_force_N(
            rolling_resistance_coeff=vehicle.rolling_resistance_coeff,
            mass_kg=vehicle.mass_kg,
            theta_rads=theta_rads,
        )
        + calc_aero_drag_force_N(
            velocity_mps=v_mps,
            rho_kgpm3=rho_kgpm3,
            drag_coeff=vehicle.drag_coeff,
            x_sectional_area_m2=vehicle.x_sectional_area_m2,
        )
    )


def calc_steady_state_power_at_wheels_W(
    vehicle: Vehicle, theta_rads: float, rho_kgpm3: float, velocity_mps: float
) -> float:
    return (
        calc_road_load_force_N(
            vehicle=vehicle,
            theta_rads=theta_rads,
            v_mps=velocity_mps,
            rho_kgpm3=rho_kgpm3,
        )
        * velocity_mps
    )


def calc_motor_electrical_power_in_W(
    vehicle: Vehicle, mech_power_out_W: float, efficiency_percent: float
) -> float:
    return mech_power_out_W / efficiency_percent * 100


def calc_tractive_force_N(
    vehicle: Vehicle,
    initial_velocity_mps: float,
    final_velocity_mps: float,
    time_delta_secs: float,
    theta_rads: float,
    rho_kgpm3: float,
) -> float:

    total_tractive_force_N = calc_inertial_force_N(
        vehicle_mass_kg=vehicle.mass_kg,
        initial_velocity_mps=initial_velocity_mps,
        final_velocity_mps=final_velocity_mps,
        time_delta_secs=time_delta_secs,
    ) + calc_road_load_force_N(
        vehicle=vehicle,
        theta_rads=theta_rads,
        v_mps=initial_velocity_mps,
        rho_kgpm3=rho_kgpm3,
    )

    return total_tractive_force_N


def calc_tractive_power_W(
    vehicle: Vehicle,
    initial_velocity_mps: float,
    final_velocity_mps: float,
    time_delta_secs: float,
    theta_rads: float,
    rho_kgpm3: float,
) -> float:
    return (
        calc_tractive_force_N(
            vehicle=vehicle,
            initial_velocity_mps=initial_velocity_mps,
            final_velocity_mps=final_velocity_mps,
            time_delta_secs=time_delta_secs,
            theta_rads=theta_rads,
            rho_kgpm3=rho_kgpm3,
        )
        * initial_velocity_mps
    )


def calc_cycle_consumption_J(vehicle: Vehicle, drive_cycle: dict) -> float:
    consumption_j = 0
    for (t0, v0), (t1, v1) in pairwise(drive_cycle.speed_trace):
        energy_J = calc_tractive_power_W(
            vehicle=vehicle,
            initial_velocity_mps=v0,
            final_velocity_mps=v1,
            time_delta_secs=t1 - t0,
            theta_rads=0,  # TODO: implement road profile later
            rho_kgpm3=drive_cycle.rho_kgpm3,
        ) * (t1 - t0)
        consumption_j += max(
            energy_J, 0
        )  # TODO: clamping to 0 until braking/regen implemented
    return consumption_j
