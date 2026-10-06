import tkinter as tk

def click_boton(valor):
    pantalla.insert(tk.END, valor)

def limpiar():
    pantalla.delete(0, tk.END)

def calcular():
    try:
        resultado = eval(pantalla.get())
        pantalla.delete(0, tk.END)
        pantalla.insert(0, str(resultado))
    except Exception:
        pantalla.delete(0, tk.END)
        pantalla.insert(0, "Error")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora")
ventana.resizable(False, False)

# Pantalla de entrada de números
pantalla = tk.Entry(ventana, font=("Arial", 20), bd=5, relief=tk.RIDGE, justify="right")
pantalla.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)

# Botones
botones = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
]

for (texto, fila, col) in botones:
    if texto == '=':
        btn = tk.Button(ventana, text=texto, width=5, height=2, font=("Arial", 14), bg="#4CAF50", fg="white", command=calcular)
    else:
        btn = tk.Button(ventana, text=texto, width=5, height=2, font=("Arial", 14), command=lambda t=texto: click_boton(t))
    btn.grid(row=fila, column=col, padx=3, pady=3)

# Botón para borrar (C)
btn_clear = tk.Button(ventana, text="C", width=22, height=2, font=("Arial", 12), bg="#f44336", fg="white", command=limpiar)
btn_clear.grid(row=5, column=0, columnspan=4, padx=3, pady=5)

ventana.mainloop()