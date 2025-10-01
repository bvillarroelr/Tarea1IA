import pandas as pd
import matplotlib.pyplot as plt

archivo_csv = "tiempos_gen15.csv"
df = pd.read_csv(archivo_csv)
df.columns = ["Tiempo"]
promedio = df["Tiempo"].mean()
print(f"\nPromedio de tiempos: {promedio:.9f} s")

plt.figure(figsize=(10,5))
plt.plot(df.index, df["Tiempo"], marker='o', label="Tiempo (s)")
plt.axhline(promedio, color='r', linestyle=':', label=f"Promedio = {promedio:.9f}s")
plt.xlabel("Medición")
plt.ylabel("Segundos")
plt.title("Tiempos y Variaciones")
plt.legend()
plt.grid(True)
plt.show()
