"""Funciones para construir, guardar y leer reportes."""

import json


def build_report(snapshot):
    disk = snapshot["disk"]
    system = snapshot["system"]
    network = snapshot["network"]
    report_lines = [
        "PC Monitor - Reporte básico",
        f"Sistema operativo: {system['operating_system']} {system['release']}",
        f"Hostname: {system['hostname']}",
        f"Uptime: {system['uptime']}",
        f"IP local: {network['local_ip']}",
        f"Uso de CPU: {snapshot['cpu']:.1f}%",
        f"Uso de memoria RAM: {snapshot['memory']:.1f}%",
        (
            f"Disco ({disk['path']}): {disk['percent']:.1f}% usado | "
            f"{disk['free_gb']:.2f} GB libres de {disk['total_gb']:.2f} GB"
        ),
        f"Fecha y hora: {snapshot['timestamp']}",
        (
            f"Red: {len(network['interfaces'])} interfaces | "
            f"Enviados: {network['bytes_sent']} bytes | "
            f"Recibidos: {network['bytes_received']} bytes"
        ),
        "Interfaces de red:",
    ]

    for interface in network["interfaces"]:
        addresses = interface["ipv4"] + interface["ipv6"]
        report_lines.append(
            f"- {interface['name']}: {', '.join(addresses) or 'sin IP'}"
        )

    report_lines.append("Procesos principales por uso de memoria:")

    for process in snapshot["processes"]:
        report_lines.append(
            f"- {process['name']} (PID {process['pid']}): "
            f"RAM {process['memory_percent']:.2f}% | "
            f"CPU {process['cpu_percent']:.2f}%"
        )

    return "\n".join(report_lines) + "\n"


def save_report(content, file_path):
    """Crea la carpeta necesaria y guarda el contenido en un archivo."""
    file_path.parent.mkdir(exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def read_report(file_path):
    """Lee y devuelve el contenido de un archivo de reporte."""
    return file_path.read_text(encoding="utf-8")


def save_session(history, summary, file_path):
    """Guarda el historial y su resumen en formato JSON."""
    payload = {
        "samples": history,
        "summary": summary,
    }
    file_path.parent.mkdir(exist_ok=True)
    file_path.write_text(
        json.dumps(payload, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )


def read_session(file_path):
    """Lee una sesión JSON y la convierte nuevamente en datos Python."""
    return json.loads(file_path.read_text(encoding="utf-8"))
