"""
step4_aerodynamics.py
PASO 4 - MODELO AERODINAMICO (depende solo del paso 1)
=======================================================================

Funciones "puras" de aerodinamica de vuelo recto y nivelado (crucero).
Se llama paso 4 y no paso 2 porque, aunque solo depende de la geometria
(paso 1), conceptualmente se necesita DESPUES de saber la masa total
que va a volar (paso 3) para tener sentido: aqui solo se definen las
formulas, en el paso 5 se combinan con la masa real del avion.

QUE SE PUEDE MODIFICAR AQUI: nada para una mision normal. Si en algun
momento quieres un modelo aerodinamico mas preciso (por ejemplo con
datos reales de tunel de viento o CFD del perfil S3021), es aqui donde
reemplazarias la formula de drag_coefficient().
"""

import math

from step1_aircraft_config import STORK_VTOL, AircraftGeometry


def lift_coefficient(
    weight_n: float,
    speed_ms: float,
    geometry: AircraftGeometry = STORK_VTOL,
) -> float:
    """Coeficiente de sustentacion (CL) necesario para sostener 'weight_n'
    (peso en Newtons) volando en linea recta a 'speed_ms' (m/s).

    Formula de sustentacion en vuelo nivelado (L = W):
        L = 0.5 * rho * V^2 * S * CL   ->   CL = 2*W / (rho * V^2 * S)
    """
    rho = geometry.air_density_kg_m3
    s = geometry.wing_area_m2
    return (2.0 * weight_n) / (rho * speed_ms**2 * s)


def drag_coefficient(
    cl: float,
    geometry: AircraftGeometry = STORK_VTOL,
) -> float:
    """Coeficiente de resistencia (CD) total, sumando:
    - CD0: resistencia parasita (friccion, forma), constante con CL
    - CDi: resistencia inducida (costo de generar sustentacion), que
      crece con el cuadrado de CL y depende del aspect ratio (AR) y de
      la eficiencia de Oswald (e)

    Formula del polar de arrastre parabolico:
        CD = CD0 + CL^2 / (pi * e * AR)
    """
    cd0 = geometry.cd0_estimate
    e = geometry.oswald_efficiency_estimate
    ar = geometry.aspect_ratio
    induced_drag_term = (cl**2) / (math.pi * e * ar)
    return cd0 + induced_drag_term


def drag_force_n(
    speed_ms: float,
    cd: float,
    geometry: AircraftGeometry = STORK_VTOL,
) -> float:
    """Fuerza de arrastre (resistencia) en Newtons.
    Formula: D = 0.5 * rho * V^2 * S * CD
    """
    rho = geometry.air_density_kg_m3
    s = geometry.wing_area_m2
    return 0.5 * rho * speed_ms**2 * s * cd


def power_required_w(
    mass_g: float,
    speed_kmh: float,
    propulsion_efficiency: float,
    geometry: AircraftGeometry = STORK_VTOL,
) -> float:
    """Potencia electrica requerida (en Watts) para volar en crucero
    nivelado a 'speed_kmh' con una masa total 'mass_g'.

    Pasos internos (encadenados, en orden):
    1. Convertir masa a peso (Newtons) y velocidad a m/s
    2. Calcular CL necesario para ese peso y velocidad
    3. Calcular CD resultante de ese CL (parasito + inducido)
    4. Calcular la fuerza de arrastre D
    5. Potencia aerodinamica = D * V (fuerza x velocidad)
    6. Dividir entre la eficiencia de propulsion, porque el motor+ESC+
       helice pierden energia como calor: la bateria debe entregar mas
       potencia de la que realmente se convierte en empuje util.
    """
    weight_n = (mass_g / 1000.0) * geometry.gravity_m_s2
    speed_ms = speed_kmh / 3.6

    cl = lift_coefficient(weight_n, speed_ms, geometry)
    cd = drag_coefficient(cl, geometry)
    drag_n = drag_force_n(speed_ms, cd, geometry)

    aerodynamic_power_w = drag_n * speed_ms
    electric_power_w = aerodynamic_power_w / propulsion_efficiency
    return electric_power_w


def lift_to_drag_ratio(
    mass_g: float,
    speed_kmh: float,
    geometry: AircraftGeometry = STORK_VTOL,
) -> float:
    """Relacion sustentacion/resistencia (L/D) a una masa y velocidad
    dadas. Un L/D mas alto significa vuelo mas eficiente (menos potencia
    por unidad de peso transportado)."""
    weight_n = (mass_g / 1000.0) * geometry.gravity_m_s2
    speed_ms = speed_kmh / 3.6
    cl = lift_coefficient(weight_n, speed_ms, geometry)
    cd = drag_coefficient(cl, geometry)
    return cl / cd


def find_best_ld_speed_kmh(
    mass_g: float,
    geometry: AircraftGeometry = STORK_VTOL,
    speed_range_kmh: tuple[float, float] = (25.0, 100.0),
    step_kmh: float = 1.0,
) -> tuple[float, float]:
    """Barre un rango de velocidades y devuelve la velocidad (km/h) a la
    que la relacion L/D es maxima, junto con ese valor maximo de L/D.
    Este barrido por fuerza bruta es intencional: es simple, facil de
    verificar a ojo, y suficientemente rapido para este rango de datos
    (no hace falta un optimizador matematico aqui)."""
    best_speed = speed_range_kmh[0]
    best_ld = 0.0
    speed = speed_range_kmh[0]
    while speed <= speed_range_kmh[1]:
        ld = lift_to_drag_ratio(mass_g, speed, geometry)
        if ld > best_ld:
            best_ld = ld
            best_speed = speed
        speed += step_kmh
    return best_speed, best_ld


if __name__ == "__main__":
    # Ejemplo rapido: potencia requerida a 60 km/h con 2000 g y 60% de
    # eficiencia de propulsion.
    p = power_required_w(mass_g=2000.0, speed_kmh=60.0, propulsion_efficiency=0.6)
    print(f"Potencia requerida a 60 km/h con 2000 g: {p:.1f} W")

    v_best, ld_best = find_best_ld_speed_kmh(mass_g=2000.0)
    print(f"Velocidad de mejor L/D: {v_best:.0f} km/h (L/D = {ld_best:.1f})")
