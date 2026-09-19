"""Funciones relacionadas con la memoria RAM."""

import psutil


def get_memory_usage():
    """Devuelve el uso actual de memoria RAM como porcentaje."""
    memory = psutil.virtual_memory()
    return memory.percent
