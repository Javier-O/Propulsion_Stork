"""
step5_performance.py
PASO 5 - RENDIMIENTO: AUTONOMIA Y ALCANCE (depende de los pasos 2, 3 y 4)
=======================================================================

Aqui es donde se combina todo lo anterior:
- La masa total que vuela (paso 3: peso vacio + bateria + payload)
- La potencia que esa masa necesita a cada velocidad (paso 4)
- La energia disponible en la bateria elegida (paso 2)

...para obtener autonomia (horas de vuelo) y alcance (km recorridos).

QUE SE PUEDE MODIFICAR AQUI: nada normalmente. Es el ultimo eslabon de
calculo puro antes de graficar (paso 6/7). Si cambias resultados aqui,
en realidad deberias estar cambiando datos en step2_powertrain_config.py.
"""

from step2_powertrain_config import BATTERY, PROPULSION_EFFICIENCY, Battery
from step4_aerodynamics import power_required_w


def usable_energy_wh(battery: Battery = BATTERY) -> float:
    """Energia UTILIZABLE de la bateria en Watt-hora, aplicando el
    'depth of discharge' (DoD): no se debe descargar una LiPo/Li-ion al
    100% en vuelo, se deja un margen de seguridad (tipicamente 20%).

    Formula: energia_util = capacidad(Ah) x voltaje(V) x DoD
    """
    capacity_ah = battery.capacity_mah / 1000.0
    total_energy_wh = capacity_ah * battery.voltage_v
    return total_energy_wh * battery.depth_of_discharge


def endurance_hours(
    mass_g: float,
    speed_kmh: float,
    propulsion_efficiency: float = PROPULSION_EFFICIENCY,
    battery: Battery = BATTERY,
) -> float:
    """Autonomia en horas: cuanto dura la bateria volando a masa y
    velocidad constantes.

    Formula: autonomia_h = energia_utilizable_Wh / potencia_requerida_W
    """
    power_w = power_required_w(mass_g, speed_kmh, propulsion_efficiency)
    if power_w <= 0:
        return 0.0
    energy_wh = usable_energy_wh(battery)
    return energy_wh / power_w


def range_km(
    mass_g: float,
    speed_kmh: float,
    propulsion_efficiency: float = PROPULSION_EFFICIENCY,
    battery: Battery = BATTERY,
) -> float:
    """Alcance en km: autonomia (h) x velocidad (km/h).
    Nota: esto es alcance SIN viento. Con viento en contra el alcance
    real de ida sera menor; con viento a favor, mayor."""
    hours = endurance_hours(mass_g, speed_kmh, propulsion_efficiency, battery)
    return hours * speed_kmh


def endurance_vs_payload(
    empty_weight_plus_battery_g: float,
    max_payload_g: float,
    cruise_speed_kmh: float = 60.0,
    propulsion_efficiency: float = PROPULSION_EFFICIENCY,
    battery: Battery = BATTERY,
    n_points: int = 12,
) -> tuple[list[float], list[float]]:
    """Genera los puntos (payload_g, autonomia_h) para graficar la curva
    de carga util vs autonomia, a velocidad de crucero fija.

    Recorre el payload desde 0 hasta max_payload_g en 'n_points' pasos
    iguales, y para cada uno calcula la autonomia con la masa total
    correspondiente (peso vacio + bateria + ese payload).
    """
    payloads = [max_payload_g * i / (n_points - 1) for i in range(n_points)]
    endurances = [
        endurance_hours(
            empty_weight_plus_battery_g + payload,
            cruise_speed_kmh,
            propulsion_efficiency,
            battery,
        )
        for payload in payloads
    ]
    return payloads, endurances


def endurance_vs_speed(
    fixed_mass_g: float,
    speed_min_kmh: float = 30.0,
    speed_max_kmh: float = 100.0,
    step_kmh: float = 7.0,
    propulsion_efficiency: float = PROPULSION_EFFICIENCY,
    battery: Battery = BATTERY,
) -> tuple[list[float], list[float]]:
    """Genera los puntos (velocidad_kmh, autonomia_h) para graficar la
    curva de velocidad vs autonomia, a masa total fija (payload fijo).
    """
    speeds: list[float] = []
    endurances: list[float] = []
    speed = speed_min_kmh
    while speed <= speed_max_kmh:
        speeds.append(speed)
        endurances.append(
            endurance_hours(fixed_mass_g, speed, propulsion_efficiency, battery)
        )
        speed += step_kmh
    return speeds, endurances


if __name__ == "__main__":
    h = endurance_hours(mass_g=2000.0, speed_kmh=60.0)
    print(f"Autonomia a 2000 g y 60 km/h: {h:.2f} h ({h*60:.0f} min)")
    print(f"Alcance equivalente: {range_km(2000.0, 60.0):.1f} km")
