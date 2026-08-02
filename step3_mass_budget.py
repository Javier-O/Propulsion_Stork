"""
step3_mass_budget.py
PASO 3 - PRESUPUESTO DE MASA (depende de los pasos 1 y 2)
=======================================================================

Aqui se combinan los datos de geometria (paso 1, para el limite de AUW
publicado) con los de electronica/bateria (paso 2) para obtener:
- Peso vacio (estructura + electronica, sin bateria ni carga)
- Peso de la bateria (calculado, no puesto a mano)
- AUW sin payload
- Payload maximo disponible antes de llegar al AUW maximo publicado

QUE SE PUEDE MODIFICAR AQUI: nada normalmente. Este archivo es "motor de
calculo": si quieres otro resultado, cambia los datos de entrada en
step2_powertrain_config.py, no las formulas de aqui.
"""

from dataclasses import dataclass

from step1_aircraft_config import STORK_VTOL, AircraftGeometry
from step2_powertrain_config import (
    ELECTRONICS_COMPONENTS,
    BATTERY,
    STRUCTURE_MASS_G,
    Battery,
    Component,
)


@dataclass
class MassBudget:
    """Resultado del presupuesto de masa: todo en gramos."""
    structure_g: float
    electronics_g: float
    empty_weight_g: float      # estructura + electronica, SIN bateria
    battery_g: float
    auw_no_payload_g: float    # empty_weight + bateria
    max_payload_g: float       # margen hasta el AUW maximo publicado


def compute_electronics_mass(components: list[Component]) -> float:
    """Suma el peso de todos los componentes de electronica de la lista.
    Recorre cada Component y acumula su mass_g."""
    return sum(c.mass_g for c in components)


def compute_battery_mass_g(battery: Battery) -> float:
    """Calcula el peso de la bateria a partir de su energia util y de la
    densidad energetica de su quimica (Wh/kg).

    Formula: peso_kg = energia_wh / densidad_wh_por_kg
    """
    capacity_ah = battery.capacity_mah / 1000.0          # mAh -> Ah
    energy_wh = capacity_ah * battery.voltage_v           # Ah x V = Wh
    # Nota: aqui se usa la energia TOTAL (no la utilizable con DoD)
    # porque el peso fisico de la bateria depende de toda su capacidad,
    # se use o no se use en vuelo.
    mass_kg = energy_wh / battery.energy_density_wh_kg
    return mass_kg * 1000.0                               # kg -> g


def compute_mass_budget(
    geometry: AircraftGeometry = STORK_VTOL,
    components: list[Component] = None,
    battery: Battery = None,
    structure_mass_g: float = None,
) -> MassBudget:
    """Arma el presupuesto de masa completo, en el orden logico:
    1. Peso de estructura (dato fijo/estimado del paso 2)
    2. Peso de electronica (suma de componentes)
    3. Peso vacio = estructura + electronica
    4. Peso de bateria (calculado a partir de capacidad/voltaje/quimica)
    5. AUW sin payload = peso vacio + bateria
    6. Payload maximo = AUW maximo publicado - AUW sin payload
    """
    # Si no se pasan argumentos, usa los valores por defecto del paso 2.
    # Esto permite llamar compute_mass_budget() sin parametros para el
    # caso normal, o pasarle una bateria/lista distinta para comparar
    # configuraciones sin editar el archivo.
    components = components if components is not None else ELECTRONICS_COMPONENTS
    battery = battery if battery is not None else BATTERY
    structure_mass_g = structure_mass_g if structure_mass_g is not None else STRUCTURE_MASS_G

    electronics_g = compute_electronics_mass(components)
    empty_weight_g = structure_mass_g + electronics_g
    battery_g = compute_battery_mass_g(battery)
    auw_no_payload_g = empty_weight_g + battery_g

    # El payload maximo no puede ser negativo: si la bateria+estructura ya
    # superan el AUW maximo publicado, el resultado se limita a 0 con max().
    max_payload_g = max(0.0, geometry.auw_max_g - auw_no_payload_g)

    return MassBudget(
        structure_g=structure_mass_g,
        electronics_g=electronics_g,
        empty_weight_g=empty_weight_g,
        battery_g=battery_g,
        auw_no_payload_g=auw_no_payload_g,
        max_payload_g=max_payload_g,
    )


if __name__ == "__main__":
    budget = compute_mass_budget()
    print(f"Estructura:            {budget.structure_g:8.1f} g")
    print(f"Electronica:           {budget.electronics_g:8.1f} g")
    print(f"Peso vacio:             {budget.empty_weight_g:8.1f} g")
    print(f"Bateria:                {budget.battery_g:8.1f} g")
    print(f"AUW sin payload:        {budget.auw_no_payload_g:8.1f} g")
    print(f"Payload maximo teorico: {budget.max_payload_g:8.1f} g")
