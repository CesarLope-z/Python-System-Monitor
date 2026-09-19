"""Funciones para construir, guardar y leer reportes."""

import json


def build_report(snapshot):
    return (
        "PC Monitor - Reporte básico\n"
        f"Uso de CPU: {snapshot['cpu']:.1f}%\n"
        f"Uso de memoria RAM: {snapshot['memory']:.1f}%\n"
        f"Fecha y hora: {snapshot['timestamp']}\n"
    )


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
