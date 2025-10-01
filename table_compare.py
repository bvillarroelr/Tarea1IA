# LRTA 15 7.81637368421053E-05
# LRTA 20 0.0001132935
# LRTA  25 0.000124412411764706
# LRTA 30  0.00015831
# LRTA 35  0.000215355666666667

# gen 15  0.004233554
# gen 20  0.00462269775
# gen 25  0.00890745428571429
# gen 30  0.0104662821538462
# gen 35  0.0055885115
import matplotlib.pyplot as plt
import pandas as pd

# Datos
datos = {
    "Tamaño": [15, 20, 25, 30, 35],
    "LRTA": [7.81637368421053E-05, 0.0001132935, 0.000124412411764706, 0.00015831, 0.000215355666666667],
    "Genético": [0.004233554, 0.00462269775, 0.00890745428571429, 0.0104662821538462, 0.0055885115]
}

df = pd.DataFrame(datos)
"""
# Crear figura
fig, ax = plt.subplots(figsize=(10,6))

# Graficar LRTA y Genético
ax.plot(df["Tamaño"], df["LRTA"], marker='o', label="LRTA")
ax.plot(df["Tamaño"], df["Genético"], marker='s', label="Genético")

# Configurar gráfica
ax.set_title("Comparación de Tiempos: LRTA vs Genético")
ax.set_xlabel("Tamaño del Laberinto")
ax.set_ylabel("Tiempo Promedio (s)")
ax.legend()
ax.grid(True)

"""

fig, ax = plt.subplots(figsize=(8, 3))
ax.axis('off')
tabla = ax.table(
    cellText=df.round(8).values,
    colLabels=df.columns,
    loc='center',
    cellLoc='center'
)

tabla.scale(1.5, 1.5)

plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

# plt.subplots_adjust(left=0.1, bottom=0.2)
plt.show()
