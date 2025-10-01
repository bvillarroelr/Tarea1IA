# Tarea1IA

## Descripción
Este proyecto permite que un agente resuelva un laberinto usando dos métodos:


1. LRTA* (Learning Real-Time A*)  

2. Algoritmo Genético

El laberinto puede cambiar dinámicamente durante la simulación.


## Requisitos
- Python 3.10 o superior

- Módulos:

pip install numpy

##  Cambiar parametros
Para cambiar el tamaño del laberinto hay que cambiar el valor de X dentro de cada uno de los metodos en el main

lab = maze.Maze(X) 

Para cambiar las probabilidades de dinamismo en el laberinto 

Cambiar X en el método 1

if random_num <= X

Cambiar X en el método 2

if random.uniform(0, 1) <= X

## Ejecución

### Desde Visual Studio Code

1. Abrir la carpeta del proyecto.

2. Abrir el archivo principal (`main.py`).

3. Ejecutar:

   - Presionar `F5` para depuración, o  
   - Click derecho → **Run Python File in Terminal**.

4. Elegir método (1 = LRTA*, 2 = Algoritmo Genético).

### Desde terminal de Linux
1. Abrir la terminal y navegar al directorio del proyecto:

cd /ruta/al/proyecto

2. Ejecutar el comando:

python3 main.py
