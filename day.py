import threading
import random
import time
from collections import defaultdict
import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk

tickets = [None] * 100
tickets_lock = threading.Lock()
num_usuarios = 125
contador_usuarios = 0
resumen_mostrado = False

def comprar_ticket(usuario_id, log_callback, actualizar_label):
    global tickets, resumen_mostrado
    cantidad = random.randint(1, 5)

    while True:
        with tickets_lock:
            disponibles = tickets.count(None)

            if disponibles == 0:
                log_callback(f"Usuario {usuario_id} no pudo comprar: No quedan tickets")
                
                if not resumen_mostrado:
                    resumen_mostrado = True
                    messagebox.showinfo("Tickets agotados", "Ya no quedan tickets disponibles.")
                    
                    resumen = defaultdict(int)
                    for dueño in tickets:
                        if dueño is not None:
                            resumen[dueño] += 1
                    log_callback("\n Resumen final de tickets por usuario:\n")
                    for usuario, cantidad in sorted(resumen.items()):
                        log_callback(f"Usuario {usuario} tiene {cantidad} ticket(s)")
                break

            if disponibles < cantidad:
                log_callback(f"Usuario {usuario_id} quería {cantidad} tickets, pero solo quedaban {disponibles}. No pudo comprar.")
                break

            indices_libres = [i for i, v in enumerate(tickets) if v is None]
            elegidos = random.sample(indices_libres, cantidad)

            for idx in elegidos:
                tickets[idx] = usuario_id

            log_callback(f"Usuario {usuario_id} compró {cantidad} ticket(s): {', '.join(str(x+1) for x in elegidos)}")
            break

        time.sleep(random.uniform(0.5, 1.5))

    actualizar_label(len([t for t in tickets if t is None]))

def iniciar_simulacion(log_box, lbl_restantes):
    global contador_usuarios
    actualizar_label = lambda restantes: lbl_restantes.config(text=f"Tickets restantes: {restantes}")
    hilos = []

    for i in range(10):
        contador_usuarios += 1
        if contador_usuarios > num_usuarios:
            log_box.insert(tk.END, "Ya no hay más usuarios para simular.\n")
            break
        usuario_id = contador_usuarios
        t = threading.Thread(
            target=comprar_ticket,
            args=(usuario_id, lambda msg: log_box.insert(tk.END, msg + "\n"), actualizar_label)
        )
        hilos.append(t)
        t.start()

class TicketSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎟️ Simulación Venta de Tickets")
        self.root.geometry("650x450")
        self.root.configure(bg="#f8fafc")

        self.frame_encabezado = tk.Frame(root, bg="#f8fafc")
        self.frame_encabezado.pack(fill="x")

        self.frame_encabezado.grid_columnconfigure(0, weight=1)
        self.frame_encabezado.grid_columnconfigure(1, weight=0)

        self.lbl_titulo = tk.Label(self.frame_encabezado, text="Simulador de Tickets",
                                   font=("Segoe UI", 16, "bold"), bg="#f8fafc", fg="black")
        self.lbl_titulo.grid(row=0, column=0, sticky="n", pady=5)

        imagen = Image.open(r"C:\Users\Harold\Downloads\logo.png")
        imagen = imagen.resize((100, 50), Image.Resampling.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(imagen)
        self.lbl_imagen = tk.Label(self.frame_encabezado, image=self.img_tk, bg="#f8fafc")
        self.lbl_imagen.grid(row=0, column=1, sticky="e", padx=20, pady=5)

        self.lbl_restantes = tk.Label(self.frame_encabezado, text=f"Tickets restantes: {len(tickets)}",
                                      font=("Segoe UI", 13, "bold"), bg="#f8fafc", fg="#2563eb")
        self.lbl_restantes.grid(row=1, column=0, pady=5)

        self.btn_simular = tk.Button(self.frame_encabezado, text="▶ Simular",
                                     font=("Segoe UI", 11, "bold"), bg="#2563eb", fg="white",
                                     activebackground="#3b82f6", activeforeground="white",
                                     command=lambda: iniciar_simulacion(self.lst_log, self.lbl_restantes))
        self.btn_simular.grid(row=2, column=0, pady=10)

        self.frame_log = tk.Frame(root, bg="#f1f5f9")
        self.frame_log.pack(fill="both", expand=True, padx=55, pady=10)
        self.lst_log = scrolledtext.ScrolledText(self.frame_log, bg="#f1f5f9", fg="black", font=("Consolas", 11))
        self.lst_log.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketSimulator(root)
    root.mainloop()