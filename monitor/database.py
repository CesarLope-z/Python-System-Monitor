"""Persistencia opcional de mediciones en SQL Server."""

from datetime import datetime
import os

from dotenv import load_dotenv


load_dotenv()


class DatabaseRepository:
    """Guarda snapshots de PC Monitor en una base de datos SQL Server."""

    def __init__(self, connection_string=None):
        self.connection_string = (
            connection_string
            or os.getenv("PC_MONITOR_DB_CONNECTION")
        )

    @property
    def is_configured(self):
        """Indica si existe una cadena de conexión configurada."""
        return bool(self.connection_string)

    def _connect(self):
        """Crea una conexión usando el driver ODBC instalado en Windows."""
        if not self.is_configured:
            raise RuntimeError(
                "Configura la variable PC_MONITOR_DB_CONNECTION primero"
            )

        try:
            import pyodbc
        except ImportError as error:
            raise RuntimeError(
                "Instala pyodbc con: pip install -r requirements.txt"
            ) from error

        return pyodbc.connect(self.connection_string, timeout=5)

    def test_connection(self):
        """Comprueba que SQL Server acepta la conexión."""
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            return cursor.fetchone()[0] == 1
        finally:
            connection.close()

    def save_snapshot(self, snapshot):
        """Guarda una medición y sus procesos asociados."""
        connection = self._connect()

        try:
            system = snapshot["system"]
            network = snapshot["network"]
            disk = snapshot["disk"]
            cursor = connection.cursor()
            captured_at = datetime.fromisoformat(snapshot["timestamp"])

            cursor.execute(
                """
                INSERT INTO dbo.monitor_readings (
                    captured_at, hostname, operating_system, os_release,
                    machine, uptime_seconds, local_ip, cpu_percent,
                    memory_percent, disk_percent, disk_total_gb,
                    disk_used_gb, disk_free_gb, bytes_sent, bytes_received
                )
                OUTPUT INSERTED.reading_id
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                captured_at,
                system["hostname"],
                system["operating_system"],
                system["release"],
                system["machine"],
                system["uptime_seconds"],
                network["local_ip"],
                snapshot["cpu"],
                snapshot["memory"],
                disk["percent"],
                disk["total_gb"],
                disk["used_gb"],
                disk["free_gb"],
                network["bytes_sent"],
                network["bytes_received"],
            )
            reading_id = cursor.fetchone()[0]

            for process in snapshot["processes"]:
                cursor.execute(
                    """
                    INSERT INTO dbo.process_snapshots (
                        reading_id, pid, process_name, username,
                        memory_percent, cpu_percent
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    reading_id,
                    process["pid"],
                    process["name"],
                    process["username"],
                    process["memory_percent"],
                    process["cpu_percent"],
                )

            connection.commit()
            return reading_id
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
