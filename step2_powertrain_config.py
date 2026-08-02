"""
step2_powertrain_config.py
PASO 2 - CONFIGURACION DE ELECTRONICA (el archivo que SI vas a editar)
=======================================================================

Este es el UNICO archivo que deberias tocar para simular una mision o
configuracion nueva: otro motor, otra bateria, otra camara FPV, etc.
Los pasos siguientes (3 en adelante) solo leen estos numeros, nunca los
definen, asi que cambiar algo aqui no puede romper la fisica del modelo.

QUE SE PUEDE MODIFICAR AQUI:
- La lista ELECTRONICS_COMPONENTS: agrega, quita o cambia el peso de
  cualquier componente (motor, ESC, camara, etc.)
- BATTERY: capacidad, numero de celdas (voltaje) y quimica.
- PROPULSION_EFFICIENCY: eficiencia global motor+ESC+helice (0 a 1).
- STRUCTURE_MASS_G: peso estimado de la estructura impresa (ajustalo
  cuando peses tu avion real ya impreso, sera mas preciso que la
  estimacion generica que trae por defecto).
"""

from dataclasses import dataclass, field


@dataclass
class Component:
    """Un componente individual de electronica: nombre + peso en gramos.
    'source' indica si el peso es un dato de fabricante confirmado o una
    estimacion (importante para saber cuanto confiar en el resultado)."""
    name: str
    mass_g: float
    source: str = "estimado"   # "fabricante" o "estimado"


# ---------------------------------------------------------------------
# LISTA DE ELECTRONICA (todo lo que va montado en el avion, EXCEPTO la
# bateria, que se maneja aparte porque su peso depende de la capacidad
# elegida, no es un valor fijo). Corresponde al pack recomendado del
# Excel de presupuesto (motores VTOL + pusher + FC + servos + etc).
# ---------------------------------------------------------------------
ELECTRONICS_COMPONENTS: list[Component] = [
    # EDITABLE: para cambiar de motor VTOL, cambia mass_g y el nombre.
    # Si cambias de 4 a otra cantidad de motores de sustentacion, agrega
    # o quita lineas repetidas como esta.
    Component("Motor VTOL T-Motor F90 1300KV #1", 46.6, "fabricante"),
    Component("Motor VTOL T-Motor F90 1300KV #2", 46.6, "fabricante"),
    Component("Motor VTOL T-Motor F90 1300KV #3", 46.6, "fabricante"),
    Component("Motor VTOL T-Motor F90 1300KV #4", 46.6, "fabricante"),
    Component("Motor pusher BrotherHobby Avenger 2812 V5", 85.0, "estimado"),
    Component("Helices VTOL 7 pulgadas (x4)", 40.0, "estimado"),
    Component("Helice pusher 10x6", 15.0, "estimado"),
    Component("Controladora de vuelo Speedybee F405 Wing", 35.0, "fabricante"),
    Component("GPS Matek M10Q", 10.0, "estimado"),
    Component("Servos EMAX ES08MAII (x4)", 36.0, "estimado"),
    Component("ESC 4en1 Velox V50A", 35.0, "estimado"),
    Component("ESC Lumenier 51A BLHeli32", 25.0, "estimado"),
    Component("Receptor Matek R24-D ELRS", 4.0, "estimado"),
    Component("Camara + VTX Walksnail Avatar Pro", 30.0, "estimado"),
    Component("Cableado y conectores varios", 50.0, "estimado"),
]


@dataclass
class Battery:
    """Configuracion de la bateria. El peso NO se pone a mano: se calcula
    en el paso 3 a partir de capacidad x voltaje x densidad energetica,
    para que sea imposible que quede desincronizado si cambias un dato."""
    capacity_mah: float = 5000.0     # EDITABLE: capacidad en mAh
    cells: int = 6                   # EDITABLE: numero de celdas (4S, 6S...)
    chemistry: str = "LiPo"          # EDITABLE: "LiPo" o "LiIon"
    depth_of_discharge: float = 0.8  # Fraccion de la bateria que se usa
                                      # de forma segura (80% es estandar,
                                      # dejar 20% de reserva)

    # Densidad energetica tipica por quimica (Wh por kg de bateria).
    # Fuente: valores tipicos de mercado, no de un fabricante especifico.
    ENERGY_DENSITY_WH_KG = {
        "LiPo": 165.0,   # Alta descarga (C-rating alto), mas pesada
        "LiIon": 230.0,  # Mayor densidad energetica, pero menor C-rating
                          # -> revisar que soporte la corriente pico de
                          # los 4 motores VTOL + pusher en despegue
    }

    @property
    def voltage_v(self) -> float:
        """Voltaje nominal aproximado: 3.7V por celda (LiPo/LiIon)."""
        return self.cells * 3.7

    @property
    def energy_density_wh_kg(self) -> float:
        return self.ENERGY_DENSITY_WH_KG[self.chemistry]


# Instancia de bateria que usan los pasos siguientes.
# EDITABLE: cambia estos valores para simular otra bateria.
BATTERY = Battery(capacity_mah=5000.0, cells=6, chemistry="LiPo")

# EDITABLE: eficiencia global del sistema de propulsion (motor + ESC +
# helice combinados). 0.55-0.70 es un rango tipico para motores/helices
# eficientes de largo alcance como los de este pack. Una helice de paso
# mas bajo o un motor menos eficiente baja este numero.
PROPULSION_EFFICIENCY: float = 0.60

# EDITABLE: peso estimado de la estructura impresa + tubos de carbono +
# tornilleria (todo lo que NO es electronica ni bateria). Actualiza este
# valor pesando tu avion real una vez impreso: es el dato con mayor
# margen de error de todo el modelo.
STRUCTURE_MASS_G: float = 650.0


if __name__ == "__main__":
    total = sum(c.mass_g for c in ELECTRONICS_COMPONENTS)
    print(f"Peso total electronica (sin bateria): {total:.1f} g")
    print(f"Bateria: {BATTERY.capacity_mah} mAh, {BATTERY.cells}S, "
          f"{BATTERY.chemistry} -> {BATTERY.voltage_v:.1f} V")
