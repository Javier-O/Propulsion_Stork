"""
step1_aircraft_config.py
PASO 1 - CONFIGURACION DEL AVION (datos que NO cambian entre misiones)
=======================================================================

Este archivo va primero porque todo lo demas depende de estos numeros:
son la geometria fisica del Stork VTOL, tomados del manual oficial
(STORK-USER-MANUAL-VTOL.pdf) y de la ficha de producto en flightory.com.

QUE SE PUEDE MODIFICAR AQUI:
- CD0 y OSWALD_EFFICIENCY son ESTIMACIONES aerodinamicas (no publicadas
  por el fabricante). Ajustalos si haces pruebas de vuelo reales y mides
  un consumo distinto al que predice el modelo.
- Todo lo demas (envergadura, superficie alar, AR) es geometria fija del
  diseño 3D impreso: NO se debe tocar a menos que modifiques el archivo
  STL/STEP del avion en si.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AircraftGeometry:
    """
    Agrupa toda la geometria y datos aerodinamicos del Stork VTOL.
    'frozen=True' significa que estos valores no se pueden cambiar por
    accidente en tiempo de ejecucion (son constantes de diseño).
    """

    # --- Dimensiones (fuente: manual oficial, pagina 5 "GENERAL AIRCRAFT DATA") ---
    wingspan_mm: float = 1620.0          # Envergadura (b)
    length_mm: float = 1000.0            # Longitud del fuselaje
    wing_area_dm2: float = 31.0          # Superficie alar (S), en decimetros cuadrados
    aspect_ratio: float = 8.3            # Relacion de aspecto (AR = b^2 / S)
    root_chord_mm: float = 230.0         # Cuerda en la raiz del ala
    mac_mm: float = 195.0                # Cuerda aerodinamica media (MAC)
    airfoil: str = "Selig S3021"         # Perfil alar usado en el diseño

    # --- Pesos operativos publicados (rango, no un numero fijo) ---
    auw_min_g: float = 1800.0            # AUW minimo publicado (config VTOL)
    auw_max_g: float = 3100.0            # AUW maximo publicado (config VTOL)

    # --- Velocidades publicadas ---
    optimal_speed_min_kmh: float = 50.0  # Rango de velocidad de crucero optima
    optimal_speed_max_kmh: float = 70.0

    # --- Coeficientes aerodinamicos ESTIMADOS (no publicados por Flightory) ---
    # CD0: resistencia parasita del fuselaje/alas a sustentacion cero.
    #   0.025-0.035 es tipico para un ala/fuselaje FPV de este tipo bien
    #   terminado (impresion lijada). Subelo si el acabado es rugoso.
    cd0_estimate: float = 0.03
    # Factor de eficiencia de Oswald (que tan cerca esta el ala de una
    # distribucion de sustentaciOn eliptica ideal). 0.75-0.85 es tipico.
    oswald_efficiency_estimate: float = 0.8

    # --- Constantes fisicas (no dependen del avion, pero se agrupan aqui
    #     porque las usan las formulas aerodinamicas del paso 4) ---
    air_density_kg_m3: float = 1.225     # Densidad del aire a nivel del mar, 15 C
    gravity_m_s2: float = 9.81           # Aceleracion de la gravedad

    @property
    def wing_area_m2(self) -> float:
        """Convierte la superficie alar de dm^2 (como la da el manual) a m^2
        (unidad que usan las formulas de sustentacion/resistencia)."""
        return self.wing_area_dm2 * 0.01   # 1 dm^2 = 0.01 m^2


# Instancia unica que van a importar el resto de los archivos.
# No crear otra instancia distinta: mantiene un solo "source of truth".
STORK_VTOL = AircraftGeometry()


if __name__ == "__main__":
    # Esto solo se ejecuta si corres este archivo directamente
    # (util para verificar rapido que los datos se cargaron bien).
    g = STORK_VTOL
    print(f"Superficie alar: {g.wing_area_m2:.3f} m^2")
    print(f"Aspect ratio: {g.aspect_ratio}")
    print(f"AUW publicado: {g.auw_min_g:.0f}-{g.auw_max_g:.0f} g")
