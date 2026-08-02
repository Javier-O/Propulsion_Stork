"""
step7_main.py
PASO 7 - SCRIPT PRINCIPAL (orquesta todo, en orden)
=======================================================================

Este es el UNICO archivo que ejecutas directamente:

    python step7_main.py

Corre, en orden cronologico, exactamente los mismos pasos que se
explicaron en el chat:

    1. Carga la geometria del avion       (step1_aircraft_config)
    2. Carga la config de electronica     (step2_powertrain_config)
    3. Calcula el presupuesto de masa     (step3_mass_budget)
    4. (las formulas aerodinamicas ya estan listas, se usan en el 5)
    5. Calcula autonomia/alcance          (step5_performance)
    6. Genera las graficas                (step6_plotting)
    7. Imprime un resumen y guarda los PNG

PARA SIMULAR UNA MISION NUEVA (otro motor, otra bateria, etc.):
    Solo edita step2_powertrain_config.py. Este archivo no necesita
    ningun cambio: va a leer automaticamente los valores nuevos.
"""

import os

from step1_aircraft_config import STORK_VTOL
from step2_powertrain_config import BATTERY, PROPULSION_EFFICIENCY
from step3_mass_budget import compute_mass_budget
from step4_aerodynamics import find_best_ld_speed_kmh
from step5_performance import endurance_vs_payload, endurance_vs_speed
from step6_plotting import plot_payload_vs_endurance, plot_speed_vs_endurance


# EDITABLE: parametros de la corrida (no de la mision, solo de como se
# quiere ver el resultado). Cambia esto si quieres, por ejemplo, fijar
# la grafica de velocidad a otro payload distinto de 500 g.
CRUISE_SPEED_FOR_PAYLOAD_CHART_KMH = 60.0
FIXED_PAYLOAD_FOR_SPEED_CHART_G = 500.0
OUTPUT_DIR = "output"


def main():
    # --- Paso 3: presupuesto de masa ---
    budget = compute_mass_budget()

    print("=" * 60)
    print("RESUMEN - STORK VTOL - PRESUPUESTO DE MASA")
    print("=" * 60)
    print(f"Estructura (estimada):     {budget.structure_g:8.1f} g")
    print(f"Electronica:               {budget.electronics_g:8.1f} g")
    print(f"Peso vacio:                {budget.empty_weight_g:8.1f} g")
    print(f"Bateria ({BATTERY.cells}S {BATTERY.chemistry} "
          f"{BATTERY.capacity_mah:.0f}mAh): {budget.battery_g:8.1f} g")
    print(f"AUW sin payload:           {budget.auw_no_payload_g:8.1f} g")
    print(f"AUW maximo publicado:      {STORK_VTOL.auw_max_g:8.1f} g")
    print(f"Payload maximo teorico:    {budget.max_payload_g:8.1f} g")

    # --- Paso 4/5: velocidad de mejor L/D, usando la masa con un
    #     payload de referencia (el mismo que se usa en la grafica 2) ---
    reference_mass = budget.auw_no_payload_g + FIXED_PAYLOAD_FOR_SPEED_CHART_G
    v_best, ld_best = find_best_ld_speed_kmh(reference_mass)
    print(f"\nVelocidad de mejor L/D (con {FIXED_PAYLOAD_FOR_SPEED_CHART_G:.0f} g "
          f"de payload): {v_best:.0f} km/h  (L/D = {ld_best:.1f})")

    # --- Paso 5: curvas de autonomia ---
    payloads, endurances_pl = endurance_vs_payload(
        empty_weight_plus_battery_g=budget.auw_no_payload_g,
        max_payload_g=budget.max_payload_g,
        cruise_speed_kmh=CRUISE_SPEED_FOR_PAYLOAD_CHART_KMH,
        propulsion_efficiency=PROPULSION_EFFICIENCY,
        battery=BATTERY,
    )
    speeds, endurances_sp = endurance_vs_speed(
        fixed_mass_g=budget.auw_no_payload_g + FIXED_PAYLOAD_FOR_SPEED_CHART_G,
        propulsion_efficiency=PROPULSION_EFFICIENCY,
        battery=BATTERY,
    )

    print(f"\nAutonomia con 0 g de payload a "
          f"{CRUISE_SPEED_FOR_PAYLOAD_CHART_KMH:.0f} km/h: {endurances_pl[0]*60:.0f} min")
    print(f"Autonomia con payload maximo ({budget.max_payload_g:.0f} g) a "
          f"{CRUISE_SPEED_FOR_PAYLOAD_CHART_KMH:.0f} km/h: {endurances_pl[-1]*60:.0f} min")

    # --- Paso 6: graficas ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plot_payload_vs_endurance(
        payloads, endurances_pl, CRUISE_SPEED_FOR_PAYLOAD_CHART_KMH,
        save_path=os.path.join(OUTPUT_DIR, "payload_vs_autonomia.png"),
    )
    plot_speed_vs_endurance(
        speeds, endurances_sp, FIXED_PAYLOAD_FOR_SPEED_CHART_G,
        save_path=os.path.join(OUTPUT_DIR, "velocidad_vs_autonomia.png"),
    )
    print(f"\nGraficas guardadas en la carpeta '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()
