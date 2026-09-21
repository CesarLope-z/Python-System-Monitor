"""Funciones relacionadas con el sistema operativo y el equipo."""

import platform
import socket
import time

import psutil

def get_system_status():
    """Devuelve un mensaje básico para comprobar que el módulo funciona."""
    return "status: OK"


def format_uptime(seconds):
    """Convierte segundos de actividad en un texto legible."""
    days, remainder = divmod(int(seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"


def get_system_info():
    """Devuelve información básica del sistema operativo y el equipo."""
    uptime_seconds = max(0, int(time.time() - psutil.boot_time()))

    return {
        "operating_system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor() or "desconocido",
        "hostname": socket.gethostname(),
        "uptime_seconds": uptime_seconds,
        "uptime": format_uptime(uptime_seconds),
    }
