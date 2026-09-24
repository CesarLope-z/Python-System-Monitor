"""Interfaz gráfica sencilla para PC Monitor."""

import tkinter as tk
from tkinter import messagebox, ttk


class PCMonitorApp:
    """Ventana principal de la aplicación."""

    def __init__(self, root, monitor, database):
        self.root = root
        self.monitor = monitor
        self.database = database
        self.latest_snapshot = None

        self.root.title("PC Monitor")
        self.root.geometry("850x560")
        self.root.minsize(700, 450)

        self.status_text = tk.StringVar(value="Listo")
        self.metric_values = {
            "Sistema": tk.StringVar(),
            "Hostname": tk.StringVar(),
            "Uptime": tk.StringVar(),
            "IP local": tk.StringVar(),
            "CPU": tk.StringVar(),
            "Memoria RAM": tk.StringVar(),
            "Disco": tk.StringVar(),
        }

        self._build_layout()
        self.refresh_metrics()

    def _build_layout(self):
        """Crea los controles visibles de la ventana."""
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="PC Monitor",
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            container,
            text="Estado actual del equipo",
        ).pack(anchor="w", pady=(0, 12))

        metrics_frame = ttk.LabelFrame(container, text="Resumen", padding=10)
        metrics_frame.pack(fill="x")

        for row, (label, variable) in enumerate(self.metric_values.items()):
            ttk.Label(metrics_frame, text=f"{label}:").grid(
                row=row // 2,
                column=(row % 2) * 2,
                sticky="w",
                padx=(0, 8),
                pady=4,
            )
            ttk.Label(metrics_frame, textvariable=variable).grid(
                row=row // 2,
                column=(row % 2) * 2 + 1,
                sticky="w",
                padx=(0, 24),
                pady=4,
            )

        processes_frame = ttk.LabelFrame(
            container,
            text="Procesos principales por memoria",
            padding=10,
        )
        processes_frame.pack(fill="both", expand=True, pady=12)

        columns = ("pid", "name", "memory", "cpu")
        self.process_tree = ttk.Treeview(
            processes_frame,
            columns=columns,
            show="headings",
        )
        headings = {
            "pid": "PID",
            "name": "Proceso",
            "memory": "Memoria %",
            "cpu": "CPU %",
        }
        widths = {"pid": 80, "name": 300, "memory": 120, "cpu": 100}
        for column in columns:
            self.process_tree.heading(column, text=headings[column])
            self.process_tree.column(column, width=widths[column])

        scrollbar = ttk.Scrollbar(
            processes_frame,
            orient="vertical",
            command=self.process_tree.yview,
        )
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        self.process_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        buttons = ttk.Frame(container)
        buttons.pack(fill="x")
        ttk.Button(
            buttons,
            text="Actualizar métricas",
            command=self.refresh_metrics,
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            buttons,
            text="Guardar en SQL Server",
            command=self.save_to_database,
        ).pack(side="left")
        ttk.Label(buttons, textvariable=self.status_text).pack(
            side="right"
        )

    def refresh_metrics(self):
        """Obtiene una medición y actualiza la interfaz."""
        try:
            snapshot = self.monitor.collect_snapshot()
            self.latest_snapshot = snapshot
            self._display_snapshot(snapshot)
            self.status_text.set("Métricas actualizadas")
        except Exception as error:
            self.status_text.set("Error al actualizar")
            messagebox.showerror("Error", str(error))

    def _display_snapshot(self, snapshot):
        """Coloca los valores de una medición en los controles."""
        system = snapshot["system"]
        network = snapshot["network"]
        disk = snapshot["disk"]

        self.metric_values["Sistema"].set(
            f"{system['operating_system']} {system['release']}"
        )
        self.metric_values["Hostname"].set(system["hostname"])
        self.metric_values["Uptime"].set(system["uptime"])
        self.metric_values["IP local"].set(network["local_ip"])
        self.metric_values["CPU"].set(f"{snapshot['cpu']:.1f}%")
        self.metric_values["Memoria RAM"].set(f"{snapshot['memory']:.1f}%")
        self.metric_values["Disco"].set(
            f"{disk['percent']:.1f}% usado / {disk['free_gb']:.2f} GB libres"
        )

        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

        for process in snapshot["processes"]:
            self.process_tree.insert(
                "",
                "end",
                values=(
                    process["pid"],
                    process["name"],
                    f"{process['memory_percent']:.2f}",
                    f"{process['cpu_percent']:.2f}",
                ),
            )

    def save_to_database(self):
        """Guarda la última medición en SQL Server."""
        if self.latest_snapshot is None:
            messagebox.showwarning("Sin datos", "Actualiza las métricas primero")
            return

        try:
            reading_id = self.database.save_snapshot(self.latest_snapshot)
            self.status_text.set(f"Guardado en SQL: #{reading_id}")
            messagebox.showinfo(
                "Guardado",
                f"La medición se guardó con el ID {reading_id}.",
            )
        except Exception as error:
            self.status_text.set("Error de base de datos")
            messagebox.showerror("SQL Server", str(error))
