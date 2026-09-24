"""Punto de entrada de la interfaz gráfica de PC Monitor."""

from pathlib import Path
import tkinter as tk

from monitor.database import DatabaseRepository
from monitor.gui import PCMonitorApp
from monitor.pc_monitor import PCMonitor


def main():
    monitor = PCMonitor(
        name="PC Monitor",
        author="Cesar Lopez",
        version=1,
        report_path=Path("reports") / "system_report.txt",
        session_path=Path("reports") / "session.json",
        disk_path=".",
        process_limit=5,
        cpu_limit=80,
        memory_limit=80,
        disk_limit=90,
        samples=3,
        delay=2,
    )
    database = DatabaseRepository()

    root = tk.Tk()
    PCMonitorApp(root, monitor, database)
    root.mainloop()


if __name__ == "__main__":
    main()
