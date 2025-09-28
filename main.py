import lrta
import maze
from time import sleep
import time
#Iniciamos el laberinto y el agente LRTA*
lab=maze.Maze(20)
lab.laberinto_estatico()
search=lrta.Lrta()
goal=(17,3)
pos = lab.agent_start_position() # Posición inicial del agente
#agent.set_maze_and_goal(lab, goal)  # Meta fija en (17,3)
lab.update_visual_matrix()
lab.printMaze()
print("\n")

"""
# Simulación del agente LRTA*
lab.mover_laberinto()
lab.update_visual_matrix()
lab.printMaze()
"""

#Bucle de LRTA*
max_steps = 300
for step in range(max_steps):

    current_goal = search.find_closest_goal(pos, lab)

    # Verificar si ya llegó a la meta
    if pos == goal:
        print(f"\n El agente llegó a la meta en {step} pasos")
        break

    # Elegir acción con LRTA*
    decision = search.lrta_agent(pos, lab)
    if decision is None:
        print("\n Meta alcanzada (None devuelto)")
        break

    action, next_pos = decision

    # Mover agente en la matriz lógica
    old_i, old_j = pos
    new_i, new_j = next_pos

    # Limpia posición anterior y actualiza nueva
    lab.logical_matrix[old_i, old_j] = 0
    lab.logical_matrix[new_i, new_j] = 1
    pos = next_pos

    # Cambiar dinámicamente el laberinto
    # lab.mover_laberinto()

    # Mouestra el estado actual
    print(f"\nPaso {step} → Acción {action} → Nueva posición {pos}")
    lab.update_visual_matrix()
    lab.printMaze()
    time.sleep(0.1)
else:
    print("\n Límite de pasos alcanzado sin llegar a la meta.")