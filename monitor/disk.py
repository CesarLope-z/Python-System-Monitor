"""Funciones relacionadas con discos y almacenamiento."""

import psutil


BYTES_PER_GIGABYTE = 1024 ** 3


def get_disk_usage(path="."):
    """Devuelve el espacio del disco que contiene la ruta indicada."""
    usage = psutil.disk_usage(str(path))

    return {
        "path": str(path),
        "total_gb": round(usage.total / BYTES_PER_GIGABYTE, 2),
        "used_gb": round(usage.used / BYTES_PER_GIGABYTE, 2),
        "free_gb": round(usage.free / BYTES_PER_GIGABYTE, 2),
        "percent": usage.percent,
    }
