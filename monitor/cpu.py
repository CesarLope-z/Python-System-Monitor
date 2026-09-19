"""Funciones relacionadas con el uso del procesador."""

import psutil


def get_cpu_usage():
    """Devuelve el uso actual de CPU como porcentaje."""
    return psutil.cpu_percent(interval=1)
