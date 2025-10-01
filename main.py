import random
import lrta
import maze
import genetico
import agent
from time import sleep
import time
import csv

# opcion 1: lrta*. 
# opción 2: algoritmo genético

print("Elige el método para que el agente resuelva el laberinto:")
print("1: LRTA* (Learning Real-Time A*)")
print("2: Algoritmo Genético")
metodo = int(input())
"""

archivo_csv = "tiempos_gen35.csv" # cambiar nombre del archivo si se usa otro método o cantidad
"""
while metodo not in [1, 2]:
    print("Opción no válida. Elige 1 o 2:")
    metodo = int(input())

if metodo == 1:
    print("\nHas elegido LRTA*.\n")

    #Iniciamos el laberinto y el agente LRTA*
    lab=maze.Maze(25)
    #lab.laberinto_estatico()
    lab.generateRandomMaze()
    search=lrta.Lrta()
    goal=lab.get_good_exit()
    pos = lab.agent_start_position() # Posición inicial del agente
    lab.update_visual_matrix()
    lab.printMaze()
    print("\n")

    #Bucle de LRTA*
    max_steps = 300
    for step in range(max_steps):
        inicio = time.time()
        current_goal = search.find_closest_goal(pos, lab)

        # Verificar si ya llegó a la meta
        if pos == goal:
            print(f"\n El agente llegó a la meta en {step} pasos")
            fin = time.time()
            tiempo_total = fin - inicio
            tiempo_total = round(tiempo_total, 9)
            print(f"Tiempo transcurrido: {tiempo_total} segundos")
            """

            with open(archivo_csv, mode='a', newline='') as archivo:
                escritor_csv = csv.writer(archivo)
                escritor_csv.writerow([tiempo_total])
                """

            break

        # Elegir acción con LRTA*
        decision = search.lrta_agent(pos, lab)
        if decision is None:
            print("\n Sen encerró el agente, no hay acciones posibles.")
            """

            tiempo_total=None
            with open(archivo_csv, mode='a', newline='') as archivo:
                escritor_csv = csv.writer(archivo)
                escritor_csv.writerow([tiempo_total])
                """

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
        if random_num <= 0.45:  # 5% probabilidad
            lab.mover_laberinto()
        
        # Muestra el estado actual
        print(f"\nPaso {step} → Acción {action} → Nueva posición {pos}")
        lab.update_visual_matrix()
        lab.printMaze()
        time.sleep(0.8)
        
    else:
        """

        tiempo_total=None
        with open(archivo_csv, mode='a', newline='') as archivo:
            escritor_csv = csv.writer(archivo)
            escritor_csv.writerow([tiempo_total])
            """

        print("\n Límite de pasos alcanzado sin llegar a la meta.")

# funciona maomeno, hay que cambiarlo porque el agente a veces se atasca, considerar entorno dinámico
elif metodo == 2:
    print("\nHas elegido Algoritmo Genético (online, paso a paso).\n")

    lab = maze.Maze(35)
    lab.generateRandomMaze()

    start = lab.agent_start_position()
    agente = agent.Agent()
    agente.position_setter(start[0], start[1])

    # calculo de distancia
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    # obetener lista de salidas ordenadas de menor a mayor (mas cercana a mas lejana)
    def get_exits_sorted_from_start(lab, start_pos):
        exits = []
        for i in range(lab.n):
            for j in range(lab.n):
                v = lab.logical_matrix[i][j]
                if v == genetico.FAKE_GOAL or v == genetico.TRUE_GOAL:
                    exits.append((i, j))
        exits.sort(key=lambda p: manhattan(start_pos, p))
        return exits
    # evaluar contexto local por si encuentra paredes o se queda encerrado
    def choose_fallback_towards_target(pos, target, lab):
        best = None
        best_dist = None
        for mv in ["N", "S", "E", "O"]:
            dr, dc = genetico.DELTA[mv]
            nr, nc = pos[0] + dr, pos[1] + dc
            if 0 <= nr < lab.n and 0 <= nc < lab.n and lab.logical_matrix[nr][nc] != genetico.WALL:
                d = manhattan((nr, nc), target)
                if best is None or d < best_dist:
                    best = (mv, (nr, nc))
                    best_dist = d
        return best  # puede ser None si está completamente encerrado

    ga = genetico.AlgoritmoGenetico(
        tamaño_poblacion=40,     # pequeño: queremos latencia baja por paso
        longitud_cromosoma=12,   # horizonte corto (12 pasos)
        prob_mutacion=0.10,
        prob_cruce=0.80,
        seed=7
    )

    current_pos = agente.position_getter()
    exit_order = get_exits_sorted_from_start(lab, current_pos)
    if not exit_order:
        print("No hay salidas en el laberinto.")
    else:
        target_idx = 0
        max_steps = 300

        print("\nEstado inicial:")
        lab.update_visual_matrix()
        lab.printMaze()
        time.sleep(0.6)

        for step in range(1, max_steps + 1):
            inicio = time.time()
            # Con cierta probabilidad, el laberinto cambia (dinámico)
            if random.uniform(0, 1) <= 0.05:
                lab.mover_laberinto()

            # Si ya probamos todas las salidas, terminamos
            if target_idx >= len(exit_order):
                print("\nNo quedan salidas por probar.")
                break

            target = exit_order[target_idx]

            # Pedimos al GA SOLO la primera acción desde la posición actual hacia el target actual
            action = ga.plan_one_action(lab, current_pos, target, generations_por_paso=12)

            # Si GA no pudo (raro), usamos fallback directo
            if action is None:
                fb = choose_fallback_towards_target(current_pos, target, lab)
                if fb is None:
                    print(f"Paso {step} → Sin movimiento válido, se queda en {current_pos}")
                    lab.update_visual_matrix()
                    lab.printMaze()
                    time.sleep(0.6)
                    continue
                mv, (nr, nc) = fb
            else:
                # Intentamos la acción propuesta
                dr, dc = genetico.DELTA[action]
                nr, nc = current_pos[0] + dr, current_pos[1] + dc
                # Si es inválida, hacemos fallback hacia el target
                if not (0 <= nr < lab.n and 0 <= nc < lab.n) or lab.logical_matrix[nr][nc] == genetico.WALL:
                    fb = choose_fallback_towards_target(current_pos, target, lab)
                    if fb is None:
                        print(f"Paso {step} → {action} → sin alternativa, se queda en {current_pos}")
                        lab.update_visual_matrix()
                        lab.printMaze()
                        time.sleep(0.6)
                        continue
                    action, (nr, nc) = fb

            # Leer PRIMERO el valor de destino
            cell_value = lab.logical_matrix[nr][nc]

            # Mover agente
            lab.logical_matrix[current_pos[0]][current_pos[1]] = 0
            lab.logical_matrix[nr][nc] = 1
            current_pos = (nr, nc)
            agente.position_setter(nr, nc)

            print(f"Paso {step} → Acción {action} → Nueva posición {current_pos}")
            lab.update_visual_matrix()
            lab.printMaze()

            # Descubrimiento al pisar
            if cell_value == genetico.TRUE_GOAL:
                print(f"\n¡Llegó a la META VERDADERA (O) en {step} pasos!")
                """

                fin = time.time()
                tiempo_total = fin - inicio
                tiempo_total = round(tiempo_total, 9)
                print(f"Tiempo transcurrido: {tiempo_total} segundos")
                with open(archivo_csv, mode='a', newline='') as archivo:
                    escritor_csv = csv.writer(archivo)
                    escritor_csv.writerow([tiempo_total])
                    """

                break
            elif cell_value == genetico.FAKE_GOAL:
                print("\nLlegó a una SALIDA FALSA (X). Cambiando a la siguiente salida más cercana…")
                target_idx += 1  # pasamos a la siguiente candidata
                continue
            """

            if step == max_steps:
                tiempo_total=None
                with open(archivo_csv, mode='a', newline='') as archivo:
                    escritor_csv = csv.writer(archivo)
                    escritor_csv.writerow([tiempo_total])
                    """


            time.sleep(0.6)