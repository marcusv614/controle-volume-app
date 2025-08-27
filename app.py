import tkinter as tk
import subprocess
import sys
import os

def iniciar_visao():
    # Executa o script ControleMao.py
    caminho = os.path.join(os.path.dirname(__file__), "ControleMao.py")
    subprocess.Popen([sys.executable, caminho])

# Janela
root = tk.Tk()
root.title("Controle de Volume por Gestos")
root.geometry("400x200")

label = tk.Label(root, text="Controle de Volume com a Mão", font=("Arial", 14))
label.pack(pady=20)

btn = tk.Button(root, text="Iniciar", command=iniciar_visao, width=15, height=2)
btn.pack(pady=10)

root.mainloop()
