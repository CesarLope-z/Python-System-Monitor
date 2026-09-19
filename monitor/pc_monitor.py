"""Clase principal que coordina la ejecución de PC Monitor."""

from datetime import datetime
from statistics import mean
import time

from monitor.cpu import get_cpu_usage
from monitor.memory import get_memory_usage
from monitor.report import (
    build_report,
    read_report,
    read_session,
    save_report,
    save_session,
)
from monitor.system import get_system_status


class PCMonitor:
    """Representa una ejecución del monitor del equipo."""

    def __init__(
        self,
        name,
        author,
        version,
        report_path,
        session_path,
        cpu_limit=80,
        memory_limit=80,
        samples=3,
        delay=2,
    ):
        self.name = name
        self.author = author
        self.version = version
        self.report_path = report_path
        self.session_path = session_path
        self.cpu_limit = cpu_limit
        self.memory_limit = memory_limit
        self.samples = samples
        self.delay = delay
        self.is_running = False
        self.history = []
        self._validate_configuration()

    def _validate_configuration(self):
        """Comprueba que la configuración tenga valores válidos."""
        if not 0 <= self.cpu_limit <= 100:
            raise ValueError("cpu_limit debe estar entre 0 y 100")
        if not 0 <= self.memory_limit <= 100:
            raise ValueError("memory_limit debe estar entre 0 y 100")
        if self.samples < 1:
            raise ValueError("samples debe ser mayor que cero")
        if self.delay < 0:
            raise ValueError("delay no puede ser negativo")

    def show_project_status(self, modules):
        """Muestra la información general del proyecto."""
        execution_status = "Activo" if self.is_running else "Detenido"

        print("Proyecto:", self.name)
        print("Autor:", self.author)
        print("Versión:", self.version)
        print("Estado:", execution_status)
        print("Módulos planificados:", modules)
        print("Límite de CPU:", f"{self.cpu_limit}%")
        print("Límite de memoria RAM:", f"{self.memory_limit}%")

    def collect_snapshot(self):
        """Obtiene una medición y la agrega al historial."""
        snapshot = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "cpu": get_cpu_usage(),
            "memory": get_memory_usage(),
        }
        self.history.append(snapshot)
        return snapshot

    def check_alerts(self, snapshot):
        """Devuelve las alertas activas para una medición."""
        alerts = []

        if snapshot["cpu"] >= self.cpu_limit:
            alerts.append(
                f"ALERTA: uso de CPU elevado: {snapshot['cpu']:.1f}% "
                f"(límite: {self.cpu_limit}%)"
            )

        if snapshot["memory"] >= self.memory_limit:
            alerts.append(
                f"ALERTA: uso de memoria RAM elevado: {snapshot['memory']:.1f}% "
                f"(límite: {self.memory_limit}%)"
            )

        return alerts

    def run_session(self, samples=None, delay=None):
        """Toma varias mediciones y devuelve el historial de la sesión."""
        samples = self.samples if samples is None else samples
        delay = self.delay if delay is None else delay

        if samples < 1:
            raise ValueError("samples debe ser mayor que cero")
        if delay < 0:
            raise ValueError("delay no puede ser negativo")

        self.history.clear()
        self.is_running = True
        print("Iniciando sesión de monitoreo...")

        try:
            for index in range(samples):
                snapshot = self.collect_snapshot()
                print(
                    f"\nMuestra {index + 1}/{samples}: "
                    f"CPU {snapshot['cpu']:.1f}% | "
                    f"RAM {snapshot['memory']:.1f}%"
                )

                for alert in self.check_alerts(snapshot):
                    print(alert)

                if index < samples - 1:
                    print(f"Esperando {delay} segundos...")
                    time.sleep(delay)
        finally:
            self.is_running = False
            print("Sesión de monitoreo finalizada.")

        return self.history

    def get_summary(self):
        """Calcula promedios y máximos de la sesión actual."""
        if not self.history:
            raise ValueError("No hay mediciones para resumir")

        cpu_values = [snapshot["cpu"] for snapshot in self.history]
        memory_values = [snapshot["memory"] for snapshot in self.history]

        return {
            "samples": len(self.history),
            "cpu_average": round(mean(cpu_values), 2),
            "cpu_max": round(max(cpu_values), 2),
            "memory_average": round(mean(memory_values), 2),
            "memory_max": round(max(memory_values), 2),
        }

    def save_current_report(self):
        """Guarda un reporte de texto con la última medición."""
        if not self.history:
            self.collect_snapshot()

        report = build_report(self.history[-1])
        save_report(report, self.report_path)
        return report

    def save_session_report(self):
        """Guarda el historial y el resumen en formato JSON."""
        summary = self.get_summary()
        save_session(self.history, summary, self.session_path)
        return summary

    def read_current_report(self):
        """Lee el último reporte de texto guardado."""
        return read_report(self.report_path)

    def read_session_report(self):
        """Lee la sesión JSON guardada."""
        return read_session(self.session_path)

    def get_system_status(self):
        """Consulta el estado básico del sistema."""
        return get_system_status()
