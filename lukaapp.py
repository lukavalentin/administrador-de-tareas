import tkinter as tk
from tkinter import ttk, messagebox
import psutil

class ProcessManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrador de Procesos")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f0f0")  # Fondo gris claro

        # Frame para el título y el botón de ayuda
        title_frame = tk.Frame(root, bg="#f0f0f0")
        title_frame.pack(pady=10)

        # Etiqueta principal
        self.label = tk.Label(title_frame, text="Procesos en ejecución", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        self.label.pack(side=tk.LEFT, padx=10)

        # Botón de ayuda
        self.help_button = tk.Button(title_frame, text="Help", command=self.show_help, bg="#0078D4", fg="white", relief=tk.FLAT)
        self.help_button.pack(side=tk.RIGHT)

        # Frame para la tabla y barra de desplazamiento
        table_frame = tk.Frame(root)
        table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Barra de desplazamiento vertical
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Definir columnas para la tabla
        self.tree = ttk.Treeview(table_frame, columns=("PID", "Nombre", "CPU", "Memoria"), show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("PID", text="PID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("CPU", text="Uso CPU (%)")
        self.tree.heading("Memoria", text="Uso Memoria (MB)")

        # Ajustar tamaños de las columnas
        self.tree.column("PID", width=60, anchor=tk.CENTER)
        self.tree.column("Nombre", width=250)
        self.tree.column("CPU", width=100, anchor=tk.CENTER)
        self.tree.column("Memoria", width=100, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Estilo para Treeview (tabla)
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 10), background="white", foreground="black", rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#f0f0f0", foreground="black")

        # Botones
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=5)

        self.refresh_button = tk.Button(button_frame, text="Actualizar", command=self.update_process_list, bg="#28A745", fg="white", relief=tk.FLAT, width=15)
        self.refresh_button.pack(side=tk.LEFT, padx=10)

        self.kill_button = tk.Button(button_frame, text="Terminar Proceso", command=self.kill_process, bg="#DC3545", fg="white", relief=tk.FLAT, width=15)
        self.kill_button.pack(side=tk.LEFT, padx=10)

        # Inicializar la lista de procesos
        self.update_process_list()

    def update_process_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)  # Limpiar la tabla antes de actualizar
        
        added_processes = set()  # Crear un conjunto para almacenar los nombres únicos de procesos
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            pid = proc.info['pid']
            name = proc.info['name']
            cpu_usage = proc.info['cpu_percent']
            memory_usage = proc.info['memory_info'].rss / (1024 * 1024)  # Convertir bytes a MB
            
            if name not in added_processes:  # Verificar si el proceso ya ha sido añadido
                self.tree.insert("", tk.END, values=(pid, name, cpu_usage, f"{memory_usage:.2f}"))
                added_processes.add(name)  # Añadir el nombre del proceso al conjunto

    def kill_process(self):
        try:
            selected_item = self.tree.selection()[0]
            selected_process = self.tree.item(selected_item)["values"]
            pid = int(selected_process[0])
            process = psutil.Process(pid)
            process.terminate()  # Terminar el proceso
            self.update_process_list()  # Actualizar la lista de procesos después de terminar
        except IndexError:
            messagebox.showwarning("Advertencia", "Debes seleccionar un proceso para terminar.")
        except psutil.NoSuchProcess:
            messagebox.showwarning("Advertencia", "El proceso ya no existe.")

    def show_help(self):
        # Crear una ventana emergente con el mensaje de ayuda
        help_window = tk.Toplevel(self.root)
        help_window.title("Ayuda")
        help_window.geometry("400x300")
        help_window.configure(bg="#f0f0f0")

        help_text = (
            "Administrador de Procesos:\n\n"
            "1. Actualizar: Presiona el botón 'Actualizar' para refrescar la lista de procesos.\n"
            "2. Selección: Haz clic en un proceso para seleccionarlo.\n"
            "3. Terminar Proceso: Selecciona un proceso y presiona 'Terminar Proceso' para cerrarlo.\n"
            "4. Uso: En la tabla se muestran el PID, nombre, uso de CPU y memoria de cada proceso.\n"
            "\nPrecaución: Ten cuidado al terminar procesos del sistema, ya que puede afectar "
            "el funcionamiento de tu equipo."
        )

        label = tk.Label(help_window, text=help_text, justify=tk.LEFT, padx=10, pady=10, font=("Helvetica", 12), bg="#f0f0f0")
        label.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessManager(root)
    root.mainloop()
