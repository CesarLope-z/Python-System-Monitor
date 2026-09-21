from pathlib import Path

from monitor.pc_monitor import PCMonitor


PLANNED_MODULES = ["CPU", "Memoria RAM", "Discos", "Procesos"]

def main():
    """Punto de entrada de la aplicación."""
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

    try:
        monitor.show_project_status(PLANNED_MODULES)
        print("Sistema:", monitor.get_system_status())

        monitor.run_session()
        monitor.save_current_report()
        summary = monitor.save_session_report()

        print("\nReporte guardado en:", monitor.report_path)
        print("Contenido del reporte:")
        print(monitor.read_current_report())
        print("Resumen de la sesión:", summary)
        print("Sesión JSON guardada en:", monitor.session_path)
    except Exception as error:
        print("No se pudo ejecutar PC Monitor:", error)

if __name__ == "__main__":
    main()
