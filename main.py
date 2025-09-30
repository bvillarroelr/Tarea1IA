import random
import lrta
import maze
import genetico
import agent
from time import sleep
import time

# opcion 1: lrta*. 
# opción 2: algoritmo genético

print("Elige el método para que el agente resuelva el laberinto:")
print("1: LRTA* (Learning Real-Time A*)")
print("2: Algoritmo Genético")
metodo = int(input())

while metodo not in [1, 2]:
    print("Opción no válida. Elige 1 o 2:")
    metodo = int(input())

if metodo == 1:
    print("\nHas elegido LRTA*.\n")

    #Iniciamos el laberinto y el agente LRTA*
    lab=maze.Maze(20)
    #lab.laberinto_estatico()
    lab.generateRandomMaze()
    search=lrta.Lrta()
    goal=lab.get_good_exit()
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
        random_num = random.uniform(0,1)
        if random_num <= 0.05:  # 5% probabilidad
            lab.mover_laberinto()

        # Muestra el estado actual
        print(f"\nPaso {step} → Acción {action} → Nueva posición {pos}")
        lab.update_visual_matrix()
        lab.printMaze()
        time.sleep(0.8)
    else:
        print("\n Límite de pasos alcanzado sin llegar a la meta.")

# funciona maomeno, hay que cambiarlo porque el agente a veces se atasca, considerar entorno dinámico
elif metodo == 2:
    print("\nHas elegido Algoritmo Genético.\n")
    
    # Inicializar laberinto y algoritmo genético
    lab = maze.Maze(20)
    lab.generateRandomMaze()
    ag = genetico.AlgoritmoGenetico(tamaño_poblacion=40, longitud_cromosoma=100)
    
    # Posición inicial del agente
    pos = lab.agent_start_position()
    
    # Crear agente y colocarlo
    agente = agent.Agent()
    agente.position_setter(pos[0], pos[1])
    lab.logical_matrix[pos[0], pos[1]] = 1
    
    lab.update_visual_matrix()
    lab.printMaze()
    print("\n")
    
    # Ejecutar algoritmo genético para encontrar la mejor solución
    mejor_solucion, generaciones = ag.evolucionar(lab, agente, generaciones=30)
    
    if mejor_solucion:
        print(f"Solución encontrada en {generaciones} generaciones. Ejecutando ruta...\n")
        
        # Resetear agente a posición inicial
        lab.logical_matrix[agente.position_getter()[0], agente.position_getter()[1]] = 0
        agente.position_setter(pos[0], pos[1])
        lab.logical_matrix[pos[0], pos[1]] = 1
        current_pos = pos
        
        # Ejecutar cada movimiento del mejor cromosoma paso a paso
        for step, movimiento in enumerate(mejor_solucion):
            # Calcular nueva posición
            dr, dc = genetico.DELTA[movimiento]
            new_r, new_c = current_pos[0] + dr, current_pos[1] + dc
            
            # Verificar si el movimiento es válido
            if (0 <= new_r < lab.n and 0 <= new_c < lab.n and 
                lab.logical_matrix[new_r, new_c] != genetico.WALL):
                
                # Mover agente
                lab.logical_matrix[current_pos[0], current_pos[1]] = 0  # Limpiar posición anterior
                lab.logical_matrix[new_r, new_c] = 1  # Nueva posición
                current_pos = (new_r, new_c)
                agente.position_setter(new_r, new_c)
                
                # Cambiar dinámicamente el laberinto (igual que LRTA*)
                random_num = random.uniform(0,1)
                if random_num <= 0.05:  # 5% probabilidad
                    lab.mover_laberinto()
                
                # Mostrar estado actual
                print(f"Paso {step + 1} → Movimiento {movimiento} → Nueva posición {current_pos}")
                lab.update_visual_matrix()
                lab.printMaze()
                
                # Verificar si llegó a una meta
                cell_value = lab.logical_matrix[new_r, new_c]
                if cell_value == genetico.TRUE_GOAL:
                    print(f"\n¡El agente llegó a la meta verdadera en {step + 1} pasos!")
                    break
                elif cell_value == genetico.FAKE_GOAL:
                    print(f"\nEl agente llegó a una salida falsa en {step + 1} pasos")
                    break
                
                time.sleep(0.8)
            else:
                # Movimiento inválido - se queda en la misma posición
                print(f"Paso {step + 1} → Movimiento {movimiento} → BLOQUEADO, se queda en {current_pos}")
                lab.update_visual_matrix()
                lab.printMaze()
                time.sleep(0.8)
    else:
        print("No se encontró solución")