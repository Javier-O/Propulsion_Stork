# Stork VTOL — Calculadora de rendimiento

Código en Python que realiza los cálculos de autonomía, alcance y masa

## Por qué varios archivos y no uno solo

Cada archivo representa una etapa que depende de la anterior. Esto separa
**lo que cambias seguido** (electrónica/batería) de **lo que no cambias
nunca** (geometría del avión, fórmulas físicas), así una edición no puede
romper el resto del cálculo por accidente. También hace más fácil auditar
un resultado raro: sabes en qué archivo mirar según qué número falló.

## Orden de ejecución (y de dependencia)

| Archivo | Qué hace | ¿Lo edito para una misión nueva? |
|---|---|---|
| `step1_aircraft_config.py` | Geometría fija del Stork VTOL (envergadura, superficie alar, AR) del manual oficial | No — solo si cambia el diseño del avión |
| `step2_powertrain_config.py` | Lista de componentes de electrónica, batería, eficiencia de propulsión | **Sí — este es el archivo a editar** |
| `step3_mass_budget.py` | Peso vacío, peso de batería, AUW, payload máximo | No |
| `step4_aerodynamics.py` | Fórmulas de CL, CD, arrastre, potencia requerida, mejor L/D | No |
| `step5_performance.py` | Autonomía y alcance combinando masa + aerodinámica + batería | No |
| `step6_plotting.py` | Genera las gráficas con matplotlib | No |
| `step7_main.py` | **Ejecuta todo en orden** — corre este archivo | No |

## Cómo correrlo

```bash
pip install matplotlib
python step7_main.py
```

Genera un resumen en consola y guarda dos PNG en `output/`.

## Cómo simular una misión nueva (otro motor, otra batería, etc.)

Edita únicamente `step2_powertrain_config.py`:

- **Cambiar de motor**: modifica el `mass_g` del `Component` correspondiente
  en `ELECTRONICS_COMPONENTS`.
- **Cambiar de batería**: modifica `BATTERY = Battery(capacity_mah=..., cells=..., chemistry="LiPo"|"LiIon")`.
- **Cambiar la eficiencia de propulsión** (motor/ESC/hélice más o menos
  eficiente): modifica `PROPULSION_EFFICIENCY`.
- **Actualizar el peso real de la estructura** una vez que peses tu avión
  impreso: modifica `STRUCTURE_MASS_G`.

Ningún otro archivo necesita tocarse — todos leen estos valores.
