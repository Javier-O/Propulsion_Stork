"""
step6_plotting.py
PASO 6 - GRAFICAS (depende del paso 5)
=======================================================================

Convierte los numeros calculados en el paso 5 en las dos graficas que
se pidieron: carga util vs autonomia, y velocidad vs autonomia.

QUE SE PUEDE MODIFICAR AQUI: los parametros de estilo (colores, tamano
de figura) y los valores fijos que se usan en cada grafica (velocidad
de crucero fija para la grafica 1, payload fijo para la grafica 2) se
pasan como argumentos a main.py (paso 7) -- no hace falta editar este
archivo para eso.
"""

import matplotlib.pyplot as plt


def plot_payload_vs_endurance(
    payloads_g: list[float],
    endurances_h: list[float],
    cruise_speed_kmh: float,
    save_path: str = None,
):
    """Grafica de linea: eje X = carga util (g), eje Y = autonomia (h).
    Titulo indica a que velocidad de crucero se fijo el calculo."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(payloads_g, endurances_h, color="#2a78d6", marker="o", linewidth=2)
    ax.fill_between(payloads_g, endurances_h, color="#2a78d6", alpha=0.1)
    ax.set_xlabel("Carga util / payload (g)")
    ax.set_ylabel("Autonomia (h)")
    ax.set_title(f"Carga util vs autonomia (crucero fijo a {cruise_speed_kmh:.0f} km/h)")
    ax.grid(True, linewidth=0.4, alpha=0.5)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig


def plot_speed_vs_endurance(
    speeds_kmh: list[float],
    endurances_h: list[float],
    fixed_payload_g: float,
    save_path: str = None,
):
    """Grafica de linea: eje X = velocidad (km/h), eje Y = autonomia (h).
    Titulo indica a que payload fijo se hizo el calculo."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(speeds_kmh, endurances_h, color="#1baf7a", marker="o", linewidth=2)
    ax.fill_between(speeds_kmh, endurances_h, color="#1baf7a", alpha=0.1)
    ax.set_xlabel("Velocidad de crucero (km/h)")
    ax.set_ylabel("Autonomia (h)")
    ax.set_title(f"Velocidad vs autonomia (payload fijo {fixed_payload_g:.0f} g)")
    ax.grid(True, linewidth=0.4, alpha=0.5)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig
