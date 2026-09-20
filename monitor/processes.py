"""Funciones relacionadas con los procesos activos."""

import psutil


def get_top_processes(limit=5):
    """Devuelve los procesos que más memoria RAM están utilizando."""
    if limit < 1:
        raise ValueError("limit debe ser mayor que cero")

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "username", "memory_percent", "cpu_percent"]
    ):
        try:
            info = process.info
            processes.append(
                {
                    "pid": info["pid"],
                    "name": info["name"] or "desconocido",
                    "username": info["username"] or "desconocido",
                    "memory_percent": round(info["memory_percent"] or 0, 2),
                    "cpu_percent": round(info["cpu_percent"] or 0, 2),
                }
            )
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return sorted(
        processes,
        key=lambda process: process["memory_percent"],
        reverse=True,
    )[:limit]
